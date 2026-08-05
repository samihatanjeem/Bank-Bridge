import streamlit as st
from utils.data_loader import load_financial_products, get_countries, get_products_for_country
from utils.ai_helper import explain_product

st.set_page_config(page_title="Term Translator | Bank Bridge", page_icon="🔎")

st.title("🔎 Financial Term Translator")
st.write(
    "Pick your home country and a financial product to see its closest "
    "US equivalent, explained in plain language."
)

products = load_financial_products()
countries = get_countries(products)

col1, col2 = st.columns(2)
with col1:
    origin_country = st.selectbox("Origin country", countries)
with col2:
    st.selectbox("Destination country", ["United States"], disabled=True)

available_products = get_products_for_country(products, origin_country)
product_labels = [p["product_name_local"] for p in available_products]

if not product_labels:
    st.warning("No products in the dataset yet for this country. Add some to `data/financial_products.json`.")
else:
    selected_label = st.selectbox("Financial product", product_labels)
    selected_product = next(p for p in available_products if p["product_name_local"] == selected_label)

    if st.button("Explain this product", type="primary"):
        with st.spinner("Looking this up..."):
            explanation = explain_product(selected_product)
        st.markdown("---")
        st.markdown(explanation)

        with st.expander("Show raw reference data (for debugging)"):
            st.json(selected_product)

st.markdown("---")
st.caption(
    "Data source: dummy dataset for development. Not verified for accuracy — "
    "do not use for real financial decisions yet."
)
