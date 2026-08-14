import html

import streamlit as st

from utils.account_guidance import account_profile, account_type_options, tailored_steps
from utils.data_loader import (
    get_process_for_country,
    load_account_opening_process,
    load_financial_products,
)
from utils.product_classifier import find_product_for_category
from utils.ui import apply_theme, brand, page_intro, source_links, steps, tags


st.set_page_config(
    page_title="Account Guide | BankBridge",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()
brand()


processes = load_account_opening_process()
products = load_financial_products()
countries = sorted(process["country"] for process in processes)

page_intro(
    "Account-opening guide",
    "Open the right account, step by step.",
    "Choose the account you need and where you're going. We'll show its local name, the likely opening journey, and what to check before you apply.",
)

account_col, origin_col, destination_col = st.columns([1.15, 0.7, 0.7])
with account_col:
    account_type = st.selectbox("What do you want to open?", account_type_options())
with origin_col:
    origin_country = st.selectbox("Home country", countries)
with destination_col:
    destination_options = [country for country in countries if country != origin_country]
    default_destination = (
        destination_options.index("United States")
        if "United States" in destination_options
        else 0
    )
    destination_country = st.selectbox(
        "Destination", destination_options, index=default_destination
    )
st.caption(f"{len(countries)} supported markets · Account guidance updates with your selection")

origin_process = get_process_for_country(processes, origin_country)
destination_process = get_process_for_country(processes, destination_country)
profile = account_profile(account_type)
origin_match = find_product_for_category(products, origin_country, profile["category"])
destination_match = find_product_for_category(
    products, destination_country, profile["category"]
)
origin_product = origin_match.product
destination_product = destination_match.product
origin_name = origin_product["product_name_local"] if origin_product else profile["plain_name"]
destination_name = (
    destination_product["product_name_local"]
    if destination_product
    else profile["plain_name"]
)

st.markdown('<div class="section-label">Your account plan</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="result-card">'
    '<span class="status-pill">DESTINATION PRODUCT</span>'
    f'<div class="quiet" style="margin-top:1.2rem;">{html.escape(account_type)} · {html.escape(destination_country)}</div>'
    f'<div class="result-name">{html.escape(destination_name)}</div>'
    f'<p class="result-detail">{html.escape(profile["purpose"])}</p>'
    '</div>',
    unsafe_allow_html=True,
)
if profile.get("notice"):
    st.info(profile["notice"])
if not destination_match.direct_category:
    st.warning(
        f"The reviewed catalog does not contain a dedicated {profile['plain_name']} "
        f"for {destination_country}, so this guide uses the closest everyday account: "
        f"{destination_name}. Confirm availability with the institution."
    )

st.markdown('<div class="section-label">Your opening checklist</div>', unsafe_allow_html=True)
home_col, destination_process_col = st.columns(2, gap="large")

with home_col:
    st.markdown(f"## {origin_country}")
    st.caption(f"Known at home as: {origin_name}")
    steps(tailored_steps(origin_process, account_type, origin_name))
    st.markdown("### Documents and details")
    tags(origin_process["typical_requirements"] if origin_process else [])

with destination_process_col:
    st.markdown(f"## {destination_country}")
    st.caption(f"Look for: {destination_name}")
    steps(tailored_steps(destination_process, account_type, destination_name))
    st.markdown("### Documents and details")
    tags(destination_process["typical_requirements"] if destination_process else [])

st.markdown('<div class="section-label">The part worth knowing</div>', unsafe_allow_html=True)
note_col, action_col = st.columns([1.35, 0.65], gap="large")
with note_col:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown("### What changes between the two")
    if origin_process:
        st.write(origin_process["notes"])
    if destination_process:
        st.write(destination_process["notes"])
    st.markdown("</div>", unsafe_allow_html=True)
with action_col:
    st.markdown("### Before you visit")
    st.write(
        f"Ask for the exact terms of the {destination_name}: accepted IDs, eligibility, "
        "opening channel, minimum deposit, fees, rate, and withdrawal rules."
    )

with st.expander("Sources and methodology"):
    if origin_process:
        st.markdown(f"**{origin_country}**")
        source_links(origin_process.get("sources", []))
        if origin_product:
            source_links(origin_product.get("sources", []))
    if destination_process:
        st.markdown(f"**{destination_country}**")
        source_links(destination_process.get("sources", []))
        if destination_product:
            source_links(destination_product.get("sources", []))

st.markdown("---")
st.caption(
    "This is a preparation guide, not a universal checklist. Banks may request more "
    "information based on the account, application channel, and customer profile."
)
