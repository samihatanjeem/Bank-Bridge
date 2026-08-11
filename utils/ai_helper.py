"""Grounded product explanations and the statement-translation prototype."""


def explain_product(product: dict) -> str:
    """Explain a mapped product using only its reviewed evidence record."""
    # Keep explanations deterministic and grounded. The statistical model is
    # responsible only for routing a term to this reviewed evidence record.
    return _fallback_explanation(product)


def explain_statement(file_bytes: bytes, filename: str) -> str:
    """
    Placeholder for the Bank Statement Translator feature.

    A production version needs a privacy/security review as well as a document
    extraction and translation implementation.
    """
    return (
        "Statement translation is not yet connected to an AI model. "
        "Once wired up, this will read the uploaded document and return "
        "a translated, plain-language summary here.\n\n"
        f"(Received file: {filename}, {len(file_bytes)} bytes — placeholder response.)"
    )


def _fallback_explanation(product: dict) -> str:
    """Build a deterministic explanation from a reviewed mapping record."""
    return (
        f"**{product['product_name_local']}** ({product['country']})\n\n"
        f"{product['description']}\n\n"
        f"**Closest US equivalent:** {product['closest_us_equivalent']}\n\n"
        f"**What's similar:** {product['similarity_notes']}\n\n"
        f"**What's different:** {product['difference_notes']}"
    )
