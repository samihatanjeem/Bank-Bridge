import html

import streamlit as st

from utils.data_loader import get_countries, get_products_for_country, load_financial_products
from utils.product_classifier import (
    ProductMappingClassifier,
    category_summary,
    classify_product,
    find_destination_product,
)
from utils.ui import apply_theme, brand, page_intro, source_links


st.set_page_config(
    page_title="Product Translator | BankBridge",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()
brand()


products = load_financial_products()


def mapping_model(country: str):
    return ProductMappingClassifier(get_products_for_country(products, country))


page_intro(
    "Product translator",
    "What did you call it back home?",
    "Enter a product name, abbreviation, or short description, then choose where you're going. We'll find the closest reviewed local product—and show where the comparison stops.",
)

input_col, origin_col, destination_col = st.columns([1.5, 0.7, 0.7], gap="medium")
with input_col:
    query = st.text_input(
        "Product name or description",
        placeholder="Try “DPS” or “I deposit the same amount every month”",
        label_visibility="visible",
    )
with origin_col:
    origin_country = st.selectbox("Home country", get_countries(products))
with destination_col:
    all_countries = get_countries(products, exclude_us=False)
    destination_options = [country for country in all_countries if country != origin_country]
    default_destination = (
        destination_options.index("United States")
        if "United States" in destination_options
        else 0
    )
    destination_country = st.selectbox(
        "Destination", destination_options, index=default_destination
    )
st.caption(f"{len(all_countries)} supported markets · Choose any destination except your home country")

available_products = get_products_for_country(products, origin_country)
with st.expander("Not sure what to type? Browse familiar terms"):
    known_product = st.selectbox(
        "Known products",
        [""] + [product["product_name_local"] for product in available_products],
        format_func=lambda value: value or "Choose a term",
        label_visibility="collapsed",
    )

find_match = st.button("Find my destination match", type="primary", use_container_width=False)

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
            destination_match = find_destination_product(
                products, product, destination_country
            )
            destination_product = destination_match.product
            if destination_product is None:
                st.warning(
                    f"We identified {product['product_name_local']}, but the reviewed "
                    f"catalog does not yet contain a safe {destination_country} match."
                )
                st.stop()

            result_status = f"CLOSEST {destination_country.upper()} MATCH"
            if not destination_match.direct_category:
                result_status = "NEAREST FUNCTIONAL MATCH"
            st.markdown('<div class="section-label">Your closest match</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="result-card">'
                f'<span class="status-pill">{html.escape(result_status)}</span>'
                f'<div class="quiet" style="margin-top:1.2rem;">{html.escape(product["product_name_local"])} · {html.escape(origin_country)} → {html.escape(destination_country)}</div>'
                f'<div class="result-name">{html.escape(destination_product["product_name_local"])}</div>'
                f'<p class="result-detail">{html.escape(destination_product["description"])}</p>'
                '</div>',
                unsafe_allow_html=True,
            )

            same_col, different_col = st.columns(2, gap="medium")
            with same_col:
                st.markdown("### What carries over")
                st.write(category_summary(destination_match.category))
            with different_col:
                st.markdown(f"### What changes in {destination_country}")
                if destination_country == "United States":
                    st.write(product["difference_notes"])
                else:
                    st.write(
                        "Rates, fees, access rules, tax treatment, deposit protection, "
                        "and the legal contract follow the destination country's rules. "
                        "The shared purpose does not make the products identical."
                    )

            origin_features, destination_features = st.columns(2, gap="medium")
            with origin_features:
                st.markdown(f"### {origin_country} features")
                st.markdown(
                    "".join(f'<span class="tag">{html.escape(feature)}</span>' for feature in product["key_features"]),
                    unsafe_allow_html=True,
                )
            with destination_features:
                st.markdown(f"### {destination_country} features")
                st.markdown(
                    "".join(f'<span class="tag">{html.escape(feature)}</span>' for feature in destination_product["key_features"]),
                    unsafe_allow_html=True,
                )

            with st.expander("Why BankBridge chose this match"):
                match_type = "Exact term match" if result.method == "exact" else "Text model match"
                st.write(
                    f"**{match_type}.** The app compared your words with reviewed product "
                    "names, aliases, and mechanics, then matched the category to a reviewed "
                    f"product in {destination_country}."
                )
                if result.method == "model":
                    st.progress(result.confidence, text=f"Match strength: {result.confidence:.0%}")
                st.caption("Match strength helps route the answer; it is not a financial probability.")

            with st.expander("View sources"):
                st.markdown(f"**{origin_country} source**")
                source_links(product.get("sources", []))
                st.markdown(f"**{destination_country} source**")
                source_links(destination_product.get("sources", []))

st.markdown("---")
st.caption(
    "Educational guidance, not financial advice. Always confirm rates, fees, insurance, "
    "tax treatment, and withdrawal rules with the institution."
)
