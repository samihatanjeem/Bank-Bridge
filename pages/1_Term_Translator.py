import streamlit as st

from utils.ai_helper import explain_product
from utils.data_loader import get_countries, get_products_for_country, load_financial_products
from utils.product_classifier import classify_product


st.set_page_config(page_title="Term Translator | Bank Bridge", page_icon="🔎")

st.title("🔎 Financial Term Translator")
st.write(
    "Enter the name or describe a financial product from home. Bank Bridge "
    "will map it to the closest reviewed US category."
)

products = load_financial_products()
countries = get_countries(products)

col1, col2 = st.columns(2)
with col1:
    origin_country = st.selectbox("Origin country", countries)
with col2:
    st.selectbox("Destination country", ["United States"], disabled=True)

available_products = get_products_for_country(products, origin_country)
product_labels = [product["product_name_local"] for product in available_products]

query = st.text_input(
    "Product name or description",
    placeholder="For example: DPS, current account, or monthly fixed savings plan",
)
known_product = st.selectbox(
    "Or browse a reviewed product",
    [""] + product_labels,
    format_func=lambda value: value or "Select a product",
)

if st.button("Find the US equivalent", type="primary"):
    submitted_term = query.strip() or known_product
    if not submitted_term:
        st.warning("Enter a product term or choose a reviewed product.")
    else:
        with st.spinner("Classifying from reviewed product data..."):
            result = classify_product(products, origin_country, submitted_term)

        if result.product is None:
            st.warning(
                "I couldn't map that confidently. Try a product name, abbreviation, "
                "or a short description of how deposits and withdrawals work."
            )
            if result.alternatives:
                st.write(
                    "Possible reviewed terms: "
                    + ", ".join(product["product_name_local"] for product in result.alternatives)
                )
        else:
            st.markdown("---")
            if result.method == "model":
                st.caption(
                    f"Model routing confidence: {result.confidence:.0%}. "
                    "This score is a routing aid, not a guarantee of equivalence."
                )
            st.markdown(explain_product(result.product))

            sources = result.product.get("sources", [])
            if sources:
                with st.expander("Sources and mapping evidence"):
                    for source in sources:
                        st.markdown(f"- [{source['title']}]({source['url']})")
                    st.caption(
                        "The model is trained from the names, aliases, descriptions, "
                        "and features in the reviewed dataset."
                    )

st.markdown("---")
st.caption(
    "Informational and educational only—not financial advice. Product terms "
    "vary by institution; verify details with the provider before acting."
)
