import html

import streamlit as st

from utils.data_loader import get_countries, get_products_for_country, load_financial_products
from utils.product_classifier import ProductMappingClassifier, classify_product
from utils.ui import apply_theme, brand, page_intro, source_links


st.set_page_config(
    page_title="Product Translator | BankBridge",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()
brand()


@st.cache_resource
def product_catalog():
    return load_financial_products()


@st.cache_resource
def mapping_model(country: str):
    return ProductMappingClassifier(get_products_for_country(product_catalog(), country))


products = product_catalog()
page_intro(
    "Product translator",
    "What did you call it back home?",
    "Enter a product name, abbreviation, or a short description. We'll show the closest US category—and where the comparison stops.",
)

input_col, country_col = st.columns([1.7, 0.8], gap="medium")
with input_col:
    query = st.text_input(
        "Product name or description",
        placeholder="Try “DPS” or “I deposit the same amount every month”",
        label_visibility="visible",
    )
with country_col:
    origin_country = st.selectbox("Home country", get_countries(products))

available_products = get_products_for_country(products, origin_country)
with st.expander("Not sure what to type? Browse familiar terms"):
    known_product = st.selectbox(
        "Known products",
        [""] + [product["product_name_local"] for product in available_products],
        format_func=lambda value: value or "Choose a term",
        label_visibility="collapsed",
    )

find_match = st.button("Find my closest US match", type="primary", use_container_width=False)

if find_match:
    submitted_term = query.strip() or known_product
    if not submitted_term:
        st.warning("Add a term or choose one from the list to continue.")
    else:
        result = classify_product(
            products,
            origin_country,
            submitted_term,
            classifier=mapping_model(origin_country),
        )

        if result.product is None:
            st.markdown('<div class="section-label">We need a little more detail</div>', unsafe_allow_html=True)
            st.info(
                "Describe how the account works—for example, whether you add money once "
                "or monthly, can withdraw anytime, or use it to make payments."
            )
            if result.alternatives:
                st.caption(
                    "You might mean: "
                    + " · ".join(product["product_name_local"] for product in result.alternatives)
                )
        else:
            product = result.product
            display_equivalent = product["closest_us_equivalent"]
            result_status = "CLOSEST US MATCH"
            if display_equivalent.startswith("Goal-based recurring savings"):
                display_equivalent = "Automatic goal-based savings"
                result_status = "NO DIRECT US EQUIVALENT"
            st.markdown('<div class="section-label">Your closest match</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="result-card">'
                f'<span class="status-pill">{result_status}</span>'
                f'<div class="quiet" style="margin-top:1.2rem;">{html.escape(product["country"])} · {html.escape(product["product_name_local"])}</div>'
                f'<div class="result-name">{html.escape(display_equivalent)}</div>'
                f'<p class="result-detail">{html.escape(product["description"])}</p>'
                '</div>',
                unsafe_allow_html=True,
            )

            same_col, different_col = st.columns(2, gap="medium")
            with same_col:
                st.markdown("### What carries over")
                st.write(product["similarity_notes"])
            with different_col:
                st.markdown("### What changes in the US")
                st.write(product["difference_notes"])

            st.markdown("### Features used for this match")
            st.markdown(
                "".join(
                    f'<span class="tag">{html.escape(feature)}</span>'
                    for feature in product["key_features"]
                ),
                unsafe_allow_html=True,
            )

            with st.expander("Why BankBridge chose this match"):
                match_type = "Exact term match" if result.method == "exact" else "Text model match"
                st.write(
                    f"**{match_type}.** The app compared your words with reviewed product "
                    "names, aliases, descriptions, and account mechanics."
                )
                if result.method == "model":
                    st.progress(result.confidence, text=f"Match strength: {result.confidence:.0%}")
                st.caption("Match strength helps route the answer; it is not a financial probability.")

            with st.expander("View sources"):
                source_links(product.get("sources", []))

st.markdown("---")
st.caption(
    "Educational guidance, not financial advice. Always confirm rates, fees, insurance, "
    "tax treatment, and withdrawal rules with the institution."
)
