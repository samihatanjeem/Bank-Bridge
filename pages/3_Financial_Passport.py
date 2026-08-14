import html
import os
from pathlib import Path

import streamlit as st

from utils.data_loader import (
    get_countries,
    load_account_opening_process,
    load_financial_products,
)
from utils.passport import (
    analyze_document,
    build_access_plan,
    demo_extraction,
    goal_options,
    passport_markdown,
)
from utils.ui import apply_theme, brand, page_intro, source_links, steps, tags


st.set_page_config(
    page_title="Financial Passport | BankBridge",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()
brand()

products = load_financial_products()
processes = load_account_opening_process()
countries = get_countries(products, exclude_us=False)
demo_file = Path(__file__).parent.parent / "data" / "demo_statement.txt"


def api_key():
    configured = os.getenv("OPENAI_API_KEY")
    if configured:
        return configured
    try:
        return st.secrets.get("OPENAI_API_KEY")
    except (FileNotFoundError, KeyError):
        return None


page_intro(
    "BankBridge Passport",
    "Your financial history shouldn't reset at the border.",
    "Turn a redacted financial document into a privacy-minimized evidence profile and a sourced 30-day plan for your destination—without inventing a credit score.",
)

st.markdown(
    '<div class="trust-row"><span class="trust-item">No identity fields in the output</span>'
    '<span class="trust-item">Not a lending decision</span>'
    '<span class="trust-item">Every pathway is sourced</span></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">1 · Set your destination</div>', unsafe_allow_html=True)
origin_col, destination_col, goal_col = st.columns([0.75, 0.75, 1.2], gap="medium")
with origin_col:
    origin_options = [country for country in countries if country != "United States"]
    default_origin = origin_options.index("India") if "India" in origin_options else 0
    origin_country = st.selectbox("Financial history from", origin_options, index=default_origin)
with destination_col:
    destination_options = [country for country in countries if country != origin_country]
    default_destination = destination_options.index("United States")
    destination_country = st.selectbox(
        "Moving to", destination_options, index=default_destination
    )
with goal_col:
    goal = st.selectbox("What do you want to accomplish?", goal_options())

st.markdown('<div class="section-label">2 · Add safe evidence</div>', unsafe_allow_html=True)
mode = st.radio(
    "Evidence mode",
    ["Try the fictional demo", "Use a redacted document"],
    index=0,
    horizontal=True,
    label_visibility="collapsed",
)

uploaded_file = None
confirmed_safe = True
if mode == "Try the fictional demo":
    st.markdown(
        '<div class="result-card"><div class="result-kicker">Zero-data demo</div>'
        '<div class="result-name" style="font-size:1.35rem;">Fictional Naya Bank statement</div>'
        '<p class="result-detail">A synthetic monthly statement demonstrates the extraction and planning workflow without exposing anyone’s finances.</p></div>',
        unsafe_allow_html=True,
    )
else:
    uploaded_file = st.file_uploader(
        "Upload a redacted PDF or image",
        type=["pdf", "png", "jpg", "jpeg", "webp", "txt"],
        help="Use synthetic or redacted data only. The app does not persist the file.",
    )
    confirmed_safe = st.checkbox(
        "I confirm this document is synthetic or redacted and contains no unnecessary sensitive data."
    )
    st.download_button(
        "Download the fictional sample",
        data=demo_file.read_bytes(),
        file_name="bankbridge_demo_statement.txt",
        mime="text/plain",
    )

configured_key = api_key()
if configured_key:
    st.caption("AI extraction is ready · OpenAI Responses API · output storage disabled")
else:
    st.info(
        "This environment has no OpenAI API key, so the fictional example runs in transparent demo mode. "
        "Add OPENAI_API_KEY to Streamlit secrets to activate document extraction."
    )

current_signature = (
    origin_country,
    destination_country,
    goal,
    mode,
    uploaded_file.name if uploaded_file else None,
    uploaded_file.size if uploaded_file else None,
)
can_build = mode == "Try the fictional demo" or (
    uploaded_file is not None and confirmed_safe and configured_key
)
build = st.button(
    "Build my Financial Passport",
    type="primary",
    use_container_width=True,
    disabled=not can_build,
)

if build:
    if mode == "Use a redacted document" and uploaded_file.size > 10 * 1024 * 1024:
        st.error("Keep the document at 10 MB or less for this privacy-first MVP.")
        st.stop()
    try:
        with st.spinner("Reading evidence, minimizing sensitive fields, and building your plan…"):
            if mode == "Try the fictional demo" and configured_key:
                extraction = analyze_document(
                    demo_file.read_bytes(),
                    demo_file.name,
                    "text/plain",
                    origin_country,
                    api_key=configured_key,
                )
                provenance = "AI-EXTRACTED FICTIONAL DOCUMENT"
            elif mode == "Try the fictional demo":
                extraction = demo_extraction(origin_country)
                provenance = "DETERMINISTIC FICTIONAL DEMO"
            else:
                extraction = analyze_document(
                    uploaded_file.getvalue(),
                    uploaded_file.name,
                    uploaded_file.type,
                    origin_country,
                    api_key=configured_key,
                )
                provenance = "AI-EXTRACTED REDACTED DOCUMENT"

            plan = build_access_plan(
                extraction,
                origin_country,
                destination_country,
                goal,
                products,
                processes,
            )
            st.session_state["passport_result"] = {
                "extraction": extraction,
                "plan": plan,
                "provenance": provenance,
                "signature": current_signature,
            }
    except Exception as exc:
        st.error(f"Passport generation could not finish: {exc}")

result = st.session_state.get("passport_result")
if result and result.get("signature") != current_signature:
    result = None
    st.caption("Your selections changed. Build again to create an updated Passport.")
if result:
    extraction = result["extraction"]
    plan = result["plan"]

    st.markdown('<div class="section-label">Your Financial Passport</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="result-card passport-hero">'
        f'<span class="status-pill">{html.escape(result["provenance"])}</span>'
        f'<div class="quiet" style="margin-top:1.2rem;">{html.escape(plan["origin_country"])} → {html.escape(plan["destination_country"])}</div>'
        f'<div class="result-name">{html.escape(plan["local_product_name"])}</div>'
        f'<p class="result-detail">{html.escape(plan["outcome"])}</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric("Document", extraction["document_type"].replace("_", " ").title())
    metric_columns[1].metric("Period", extraction.get("statement_period") or "Not found")
    metric_columns[2].metric("Currency", extraction.get("currency") or "Not found")
    metric_columns[3].metric(
        "Readiness",
        f"{plan['readiness_complete']} / {plan['readiness_total']}",
        help="Checks institution, period, currency, and whether a holder name is visible. This is not a credit score.",
    )

    evidence_col, privacy_col = st.columns([1.3, 0.7], gap="large")
    with evidence_col:
        st.markdown("### Evidence the document supports")
        st.write(extraction["plain_summary"])
        for item in extraction.get("evidence", []):
            st.markdown(
                '<div class="evidence-row">'
                f'<div><strong>{html.escape(item["field"])}</strong><br>'
                f'<span>{html.escape(item["value"])}</span></div>'
                f'<span class="confidence-{html.escape(item["confidence"])}">{html.escape(item["confidence"]).upper()}</span>'
                '</div>',
                unsafe_allow_html=True,
            )
    with privacy_col:
        st.markdown("### Safe to share?")
        tags(extraction.get("readiness_flags", []))
        for warning in extraction.get("redaction_warnings", []):
            st.warning(warning)
        st.caption("BankBridge never includes a detected name or account identifier in the Passport output.")

    st.markdown('<div class="section-label">Your 30-day access plan</div>', unsafe_allow_html=True)
    steps(plan["steps"])

    document_col, source_col = st.columns(2, gap="large")
    with document_col:
        st.markdown("### Documents to confirm")
        tags(plan["requirements"])
    with source_col:
        st.markdown("### Grounded in destination guidance")
        source_links(plan["sources"])

    artifact = passport_markdown(extraction, plan)
    st.download_button(
        "Download my privacy-minimized Passport",
        data=artifact,
        file_name="bankbridge_financial_passport.md",
        mime="text/markdown",
        type="primary",
    )

    with st.expander("What the AI did—and did not do"):
        st.markdown(
            "**Did:** read the supplied document, extract a strict evidence schema, "
            "suppress direct identity fields, and connect the evidence to reviewed destination guidance.\n\n"
            "**Did not:** create a credit score, decide eligibility, recommend a lender, "
            "or claim that the destination institution will accept the document."
        )

st.markdown("---")
st.caption(
    "Educational preparation only—not financial, credit, legal, tax, or immigration advice. "
    "Confirm requirements directly with the receiving institution."
)
