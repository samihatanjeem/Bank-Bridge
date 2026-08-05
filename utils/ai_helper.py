"""
AI reasoning layer for Bank Bridge.

IMPORTANT FOR PERSON B:
This module currently has a rule-based fallback (`_fallback_explanation`) so the
front-end is fully testable without an API key. Your job is to wire up
`explain_product()` and `explain_statement()` to a real LLM call (Claude or
OpenAI) and have it use the fallback text as *context*, not replace the
grounding data with free generation.

Suggested prompt pattern for explain_product():

    You are explaining a financial product to a newcomer to the US.
    Here is verified reference data about the product (do not invent details
    beyond this): {product_json}
    Write a short, plain-language explanation covering:
    1. What this product is
    2. How it compares to {closest_us_equivalent}
    3. The most important difference a newcomer should know
    Keep it under 150 words. Do not give financial advice or recommendations.
"""

import os


def explain_product(product: dict) -> str:
    """
    Return a plain-language explanation of a financial product, grounded in
    the provided reference data.

    Currently rule-based. Replace the body of this function with a real LLM
    call once an API key is available — keep the same input/output signature
    so the front-end doesn't need to change.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return _fallback_explanation(product)

    # TODO (Person B): replace this with a real API call, e.g.:
    #
    # import anthropic
    # client = anthropic.Anthropic()
    # response = client.messages.create(
    #     model="claude-sonnet-4-6",
    #     max_tokens=300,
    #     messages=[{"role": "user", "content": _build_prompt(product)}],
    # )
    # return response.content[0].text
    #
    return _fallback_explanation(product)


def explain_statement(file_bytes: bytes, filename: str) -> str:
    """
    Placeholder for the Bank Statement Translator feature.

    Person B: wire this up to a vision-capable model call (Claude/GPT-4 class)
    that accepts the uploaded file directly and returns a translated,
    plain-language summary. No OCR pipeline needed — pass the file straight
    to the model.
    """
    return (
        "Statement translation is not yet connected to an AI model. "
        "Once wired up, this will read the uploaded document and return "
        "a translated, plain-language summary here.\n\n"
        f"(Received file: {filename}, {len(file_bytes)} bytes — placeholder response.)"
    )


def _fallback_explanation(product: dict) -> str:
    """Simple template-based explanation, used until the real AI call is wired up."""
    return (
        f"**{product['product_name_local']}** ({product['country']})\n\n"
        f"{product['description']}\n\n"
        f"**Closest US equivalent:** {product['closest_us_equivalent']}\n\n"
        f"**What's similar:** {product['similarity_notes']}\n\n"
        f"**What's different:** {product['difference_notes']}\n\n"
        f"_This is a placeholder explanation built directly from the reference "
        f"data. Once the AI model is connected, this will be rewritten as a "
        f"more natural, conversational explanation._"
    )


def _build_prompt(product: dict) -> str:
    """Helper to build the LLM prompt from a product dict. Fill in when wiring up the API."""
    return (
        "You are explaining a financial product to a newcomer to the US. "
        "Here is verified reference data about the product (do not invent "
        f"details beyond this): {product}\n\n"
        "Write a short, plain-language explanation covering: "
        "1) what this product is, 2) how it compares to the closest US "
        "equivalent, 3) the most important difference a newcomer should know. "
        "Keep it under 150 words. Do not give financial advice or recommendations."
    )
