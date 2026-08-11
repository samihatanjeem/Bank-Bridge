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
countries = sorted(process["country"] for process in processes if process["country"] != "United States")

page_intro(
    "Account-opening guide",
    "Know what to expect before you apply.",
    "Compare the familiar process at home with a typical US bank journey. Requirements vary, but the right documents make the first visit easier.",
)

country_col, blank_col = st.columns([0.8, 1.2])
with country_col:
    origin_country = st.selectbox("Compare with", countries)

origin_process = get_process_for_country(processes, origin_country)
us_process = get_process_for_country(processes, "United States")

st.markdown('<div class="section-label">Side-by-side journey</div>', unsafe_allow_html=True)
home_col, us_col = st.columns(2, gap="large")

with home_col:
    st.markdown(f"## {origin_country}")
    st.caption("A typical personal account journey")
    steps(origin_process["steps"] if origin_process else [])
    st.markdown("### Documents and details")
    tags(origin_process["typical_requirements"] if origin_process else [])

with us_col:
    st.markdown("## United States")
    st.caption("What many banks or credit unions ask for")
    steps(us_process["steps"] if us_process else [])
    st.markdown("### Documents and details")
    tags(us_process["typical_requirements"] if us_process else [])

st.markdown('<div class="section-label">The part worth knowing</div>', unsafe_allow_html=True)
note_col, action_col = st.columns([1.35, 0.65], gap="large")
with note_col:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown("### Your ID options may be broader than you think")
    if origin_process:
        st.write(origin_process["notes"])
    if us_process:
        st.write(us_process["notes"])
    st.markdown("</div>", unsafe_allow_html=True)
with action_col:
    st.markdown("### Before you visit")
    st.write("Call the institution and ask which IDs it accepts, whether you need an appointment, and what minimum deposit applies to the exact account.")

with st.expander("Sources and methodology"):
    if origin_process:
        st.markdown(f"**{origin_country}**")
        source_links(origin_process.get("sources", []))
    if us_process:
        st.markdown("**United States**")
        source_links(us_process.get("sources", []))

st.markdown("---")
st.caption(
    "This is a preparation guide, not a universal checklist. Banks may request more "
    "information based on the account, application channel, and customer profile."
)
