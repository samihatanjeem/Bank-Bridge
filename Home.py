"""BankBridge landing page. Run with: streamlit run Home.py"""

import streamlit as st

from utils.ui import apply_theme, brand


st.set_page_config(
    page_title="BankBridge | Your banking guide in the US",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()
brand()

left, right = st.columns([1.3, 0.7], gap="large")
with left:
    st.markdown('<div class="eyebrow">Built for your next chapter</div>', unsafe_allow_html=True)
    st.markdown("# Banking shouldn't feel <span class='accent'>foreign.</span>", unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-copy">Understand US banking through the products and '
        'processes you already know. Clear comparisons, practical steps, and '
        'sources you can trust.</div>',
        unsafe_allow_html=True,
    )
    cta, secondary = st.columns([1, 1.15])
    with cta:
        st.page_link("pages/1_Term_Translator.py", label="Translate a banking term", icon=None)
    with secondary:
        st.page_link("pages/2_Process_Comparison.py", label="Compare account opening", icon=None)
    st.markdown(
        '<div class="trust-row"><span class="trust-item">10 home countries</span>'
        '<span class="trust-item">Sources included</span>'
        '<span class="trust-item">No sign-up</span></div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="result-card" style="margin-top:2.2rem;padding:2rem;">
          <span class="status-pill">EXAMPLE MATCH</span>
          <div class="quiet" style="margin-top:1.4rem;">Bangladesh · Fixed Deposit Receipt</div>
          <div class="result-name">FDR</div>
          <div style="height:1px;background:rgba(15,35,60,.10);margin:1.3rem 0;"></div>
          <div class="quiet">Closest US equivalent</div>
          <div style="font-size:1.3rem;font-weight:740;margin-top:.25rem;">Certificate of Deposit</div>
          <p class="result-detail" style="margin-top:.8rem;">Same fixed-term idea. Different insurance, tax, and renewal rules.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-label">Start with what you need</div>', unsafe_allow_html=True)
card_columns = st.columns(3, gap="medium")
cards = [
    (
        "01",
        "Translate a product",
        "Type a familiar term like FDR, DPS, or BSBDA and see the closest US category.",
        "pages/1_Term_Translator.py",
        "Find a match",
    ),
    (
        "02",
        "Open your first account",
        "Compare the documents and steps at home with what a US bank may ask for.",
        "pages/2_Process_Comparison.py",
        "Compare the process",
    ),
    (
        "03",
        "Read a statement",
        "Learn what common statement sections mean before sharing a financial document.",
        "pages/3_Statement_Guide.py",
        "Open statement guide",
    ),
]
for column, (number, title, copy, page, link_label) in zip(card_columns, cards):
    with column:
        st.markdown(
            f'<div class="feature-card"><div class="number">{number}</div>'
            f'<h3>{title}</h3><p>{copy}</p></div>',
            unsafe_allow_html=True,
        )
        st.page_link(page, label=link_label, icon=None)

st.markdown('<div class="section-label">Designed for clarity</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="result-card">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1.4rem;">
        <div><div class="result-kicker">Grounded</div><h3>Evidence with every answer</h3><p class="result-detail">Regulator and provider sources stay one click away.</p></div>
        <div><div class="result-kicker">Honest</div><h3>Differences stay visible</h3><p class="result-detail">A close match is never presented as an identical product.</p></div>
        <div><div class="result-kicker">Private by default</div><h3>Explore without an account</h3><p class="result-detail">The core product and process guides require no personal data.</p></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
