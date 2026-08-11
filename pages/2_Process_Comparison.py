import streamlit as st

from utils.data_loader import load_account_opening_process, get_process_for_country
from utils.ui import apply_theme, brand, page_intro, source_links, steps, tags


st.set_page_config(
    page_title="Account Guide | BankBridge",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()
brand()


@st.cache_resource
def process_catalog():
    return load_account_opening_process()


processes = process_catalog()
countries = sorted(process["country"] for process in processes)

page_intro(
    "Account-opening guide",
    "Know what to expect before you apply.",
    "Compare the familiar process at home with your destination. Requirements vary, but knowing the likely steps and documents makes the first visit easier.",
)

origin_col, destination_col, blank_col = st.columns([0.7, 0.7, 0.6])
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

origin_process = get_process_for_country(processes, origin_country)
destination_process = get_process_for_country(processes, destination_country)

st.markdown('<div class="section-label">Side-by-side journey</div>', unsafe_allow_html=True)
home_col, destination_process_col = st.columns(2, gap="large")

with home_col:
    st.markdown(f"## {origin_country}")
    st.caption("A typical personal account journey")
    steps(origin_process["steps"] if origin_process else [])
    st.markdown("### Documents and details")
    tags(origin_process["typical_requirements"] if origin_process else [])

with destination_process_col:
    st.markdown(f"## {destination_country}")
    st.caption("A typical destination account journey")
    steps(destination_process["steps"] if destination_process else [])
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
    st.write("Call the institution and ask which IDs it accepts, whether you need an appointment, and what minimum deposit applies to the exact account.")

with st.expander("Sources and methodology"):
    if origin_process:
        st.markdown(f"**{origin_country}**")
        source_links(origin_process.get("sources", []))
    if destination_process:
        st.markdown(f"**{destination_country}**")
        source_links(destination_process.get("sources", []))

st.markdown("---")
st.caption(
    "This is a preparation guide, not a universal checklist. Banks may request more "
    "information based on the account, application channel, and customer profile."
)
