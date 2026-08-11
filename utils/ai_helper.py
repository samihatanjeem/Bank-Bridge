"""Grounded product explanations."""


def explain_product(product: dict) -> str:
    """Explain a mapped product using only its reviewed evidence record."""
    # Keep explanations deterministic and grounded. The statistical model is
    # responsible only for routing a term to this reviewed evidence record.
    return _fallback_explanation(product)
def _fallback_explanation(product: dict) -> str:
    """Build a deterministic explanation from a reviewed mapping record."""
    return (
        f"**{product['product_name_local']}** ({product['country']})\n\n"
        f"{product['description']}\n\n"
        f"**Closest US equivalent:** {product['closest_us_equivalent']}\n\n"
        f"**What's similar:** {product['similarity_notes']}\n\n"
        f"**What's different:** {product['difference_notes']}"
    )
