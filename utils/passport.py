"""Privacy-aware financial document extraction and newcomer access planning."""

import base64
import json
import mimetypes
import os
from typing import Dict, List, Optional

from utils.data_loader import get_process_for_country
from utils.product_classifier import find_product_for_category


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

PASSPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "document_type": {
            "type": "string",
            "enum": ["bank_statement", "pay_slip", "credit_report", "other"],
        },
        "institution_name": {"type": ["string", "null"]},
        "country_hint": {"type": ["string", "null"]},
        "currency": {"type": ["string", "null"]},
        "statement_period": {"type": ["string", "null"]},
        "holder_name_visible": {"type": "boolean"},
        "account_identifier_visible": {"type": "boolean"},
        "opening_balance": {"type": ["number", "null"]},
        "closing_balance": {"type": ["number", "null"]},
        "recurring_income_detected": {"type": "boolean"},
        "recurring_income_amount": {"type": ["number", "null"]},
        "income_frequency": {"type": ["string", "null"]},
        "recurring_obligation_categories": {
            "type": "array",
            "items": {"type": "string"},
        },
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "value": {"type": "string"},
                    "confidence": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                    },
                    "evidence_note": {"type": "string"},
                },
                "required": ["field", "value", "confidence", "evidence_note"],
                "additionalProperties": False,
            },
        },
        "readiness_flags": {"type": "array", "items": {"type": "string"}},
        "redaction_warnings": {"type": "array", "items": {"type": "string"}},
        "plain_summary": {"type": "string"},
    },
    "required": [
        "document_type",
        "institution_name",
        "country_hint",
        "currency",
        "statement_period",
        "holder_name_visible",
        "account_identifier_visible",
        "opening_balance",
        "closing_balance",
        "recurring_income_detected",
        "recurring_income_amount",
        "income_frequency",
        "recurring_obligation_categories",
        "evidence",
        "readiness_flags",
        "redaction_warnings",
        "plain_summary",
    ],
    "additionalProperties": False,
}

EXTRACTION_PROMPT = """
You extract a privacy-minimized financial evidence profile from one user-provided
document. Report only what is visibly supported. Never output a person's name,
address, account number, card number, tax ID, document ID, or transaction-level
merchant name. For those fields, return only the requested visibility booleans.
Group recurring obligations into broad categories such as housing, utilities,
debt payment, insurance, or transfers. Do not assess creditworthiness, calculate
a credit score, recommend a lender, or make an eligibility decision. Use null
for unknown numeric or text values. Keep evidence notes short and auditable.
""".strip()

GOAL_PROFILES = {
    "Open my first account": {
        "category": "transactions",
        "outcome": "Establish a safe account for deposits, payments, and transfers.",
        "habit": "Review the first statement for unexpected fees and confirm alerts are on.",
    },
    "Build an emergency fund": {
        "category": "savings",
        "outcome": "Create a separate, accessible place for emergency savings.",
        "habit": "Set a small recurring transfer and adjust it after the first month.",
    },
    "Start building credit": {
        "category": "basic_account",
        "outcome": "Build the banking foundation needed before comparing credit-building paths.",
        "habit": "Check statements and payment dates; never treat this Passport as a credit score.",
    },
    "Prepare for a financial application": {
        "category": "savings",
        "outcome": "Organize consistent, verifiable evidence for a future application.",
        "habit": "Keep original monthly statements together and document any requested translations.",
    },
}


def goal_options() -> List[str]:
    return list(GOAL_PROFILES)


def demo_extraction(origin_country: str = "India") -> dict:
    """Return a fictional, deterministic record for a zero-data demo."""
    return {
        "document_type": "bank_statement",
        "institution_name": "Naya Bank (fictional demo)",
        "country_hint": origin_country,
        "currency": "INR" if origin_country == "India" else "Local currency",
        "statement_period": "1–31 July 2026",
        "holder_name_visible": True,
        "account_identifier_visible": True,
        "opening_balance": 184250.00,
        "closing_balance": 226840.00,
        "recurring_income_detected": True,
        "recurring_income_amount": 95000.00,
        "income_frequency": "monthly",
        "recurring_obligation_categories": ["housing", "utilities", "transfers"],
        "evidence": [
            {
                "field": "Income pattern",
                "value": "One recurring monthly deposit",
                "confidence": "high",
                "evidence_note": "A similarly labeled credit appears in the demo period.",
            },
            {
                "field": "Balance continuity",
                "value": "Opening and closing balances are visible",
                "confidence": "high",
                "evidence_note": "Both summary balances appear on the fictional statement.",
            },
            {
                "field": "Recurring obligations",
                "value": "Housing, utilities, and transfers",
                "confidence": "medium",
                "evidence_note": "Broad categories only; merchant names are intentionally omitted.",
            },
        ],
        "readiness_flags": [
            "Institution name visible",
            "Statement period visible",
            "Currency visible",
            "Holder name appears visible",
        ],
        "redaction_warnings": [
            "An account identifier appears visible—redact it unless the recipient requires it.",
        ],
        "plain_summary": (
            "This fictional statement shows a complete monthly period, visible balance "
            "continuity, and a recurring income pattern. It is evidence, not a credit score."
        ),
    }


def document_content(file_bytes: bytes, filename: str, mime_type: Optional[str]) -> dict:
    """Build a direct Responses API content item without persisting the file."""
    detected_type = mime_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    data_url = f"data:{detected_type};base64,{encoded}"
    if detected_type.startswith("image/"):
        return {"type": "input_image", "image_url": data_url, "detail": "high"}
    item = {
        "type": "input_file",
        "filename": filename,
        "file_data": data_url,
    }
    if detected_type == "application/pdf":
        item["detail"] = "high"
    return item


def analyze_document(
    file_bytes: bytes,
    filename: str,
    mime_type: Optional[str],
    origin_country: str,
    api_key: Optional[str] = None,
    client=None,
) -> dict:
    """Extract a privacy-minimized profile with the OpenAI Responses API."""
    if client is None:
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the openai package to analyze documents") from exc
        client = OpenAI(api_key=api_key)

    content = [
        document_content(file_bytes, filename, mime_type),
        {
            "type": "input_text",
            "text": (
                f"The user says this document is from {origin_country}. "
                "Extract the financial evidence profile using the required schema."
            ),
        },
    ]
    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=EXTRACTION_PROMPT,
        input=[{"role": "user", "content": content}],
        text={
            "format": {
                "type": "json_schema",
                "name": "financial_evidence_passport",
                "strict": True,
                "schema": PASSPORT_SCHEMA,
            }
        },
        reasoning={"effort": "low"},
        max_output_tokens=1800,
        store=False,
    )
    if getattr(response, "status", "completed") != "completed":
        raise RuntimeError("The document analysis did not complete")
    try:
        result = json.loads(response.output_text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("The document analysis returned invalid structured data") from exc
    _validate_extraction(result)
    return result


def _validate_extraction(result: dict) -> None:
    missing = set(PASSPORT_SCHEMA["required"]) - set(result)
    if missing:
        raise RuntimeError("Document analysis omitted required fields: " + ", ".join(sorted(missing)))


def build_access_plan(
    extraction: dict,
    origin_country: str,
    destination_country: str,
    goal: str,
    products: List[dict],
    processes: List[dict],
) -> dict:
    """Create a deterministic, sourced action plan from extracted evidence."""
    profile = GOAL_PROFILES[goal]
    process = get_process_for_country(processes, destination_country)
    match = find_product_for_category(products, destination_country, profile["category"])
    local_product = match.product
    product_name = local_product["product_name_local"] if local_product else "deposit account"
    requirements = process.get("typical_requirements", []) if process else []

    steps = [
        (
            "Today — protect your evidence: keep the original file, create a redacted "
            "copy, and confirm exactly which pages the recipient needs."
        ),
        (
            f"Within 7 days — gather the {destination_country} identity and contact "
            f"documents listed below, then ask an institution about {product_name}."
        ),
        (
            f"Within 14 days — compare the exact fees, minimums, access rules, and "
            f"deposit protection before applying for the {product_name}."
        ),
        f"By day 30 — {profile['habit']}",
    ]
    readiness_checks = [
        bool(extraction.get("institution_name")),
        bool(extraction.get("statement_period")),
        bool(extraction.get("currency")),
        bool(extraction.get("holder_name_visible")),
    ]
    sources = []
    seen_urls = set()
    for source in (process or {}).get("sources", []) + (local_product or {}).get("sources", []):
        if source["url"] not in seen_urls:
            seen_urls.add(source["url"])
            sources.append(source)

    return {
        "goal": goal,
        "outcome": profile["outcome"],
        "origin_country": origin_country,
        "destination_country": destination_country,
        "local_product_name": product_name,
        "direct_product_match": match.direct_category,
        "steps": steps,
        "requirements": requirements,
        "sources": sources,
        "readiness_complete": sum(readiness_checks),
        "readiness_total": len(readiness_checks),
    }


def passport_markdown(extraction: dict, plan: dict) -> str:
    """Create a portable text artifact without raw identity or account numbers."""
    evidence_lines = "\n".join(
        f"- **{item['field']}:** {item['value']} ({item['confidence']} confidence)"
        for item in extraction.get("evidence", [])
    ) or "- No reliable evidence extracted"
    step_lines = "\n".join(
        f"{index}. {step}" for index, step in enumerate(plan["steps"], 1)
    )
    requirement_lines = "\n".join(
        f"- {requirement}" for requirement in plan.get("requirements", [])
    )
    source_lines = "\n".join(
        f"- [{source['title']}]({source['url']})" for source in plan.get("sources", [])
    )
    return f"""# BankBridge Financial Passport

**Journey:** {plan['origin_country']} → {plan['destination_country']}  
**Goal:** {plan['goal']}  
**Closest local pathway:** {plan['local_product_name']}

## Privacy-minimized evidence

{extraction['plain_summary']}

{evidence_lines}

## 30-day access plan

{step_lines}

## Documents to confirm

{requirement_lines}

## Sources

{source_lines}

---

This Passport is educational preparation, not a credit score, lending decision,
eligibility determination, or financial advice. Confirm requirements directly
with the institution. It intentionally excludes names and account identifiers.
"""
