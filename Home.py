"""BankBridge landing page. Run with: streamlit run Home.py"""

import streamlit as st

from utils.data_loader import get_countries, load_financial_products
from utils.ui import apply_theme, brand, tags


st.set_page_config(
    page_title="BankBridge | Your cross-border banking guide",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()
brand()
supported_markets = get_countries(load_financial_products(), exclude_us=False)

left, right = st.columns([1.3, 0.7], gap="large")
with left:
    st.markdown('<div class="eyebrow">Financial inclusion for newcomers</div>', unsafe_allow_html=True)
    st.markdown("# Your financial history shouldn't <span class='accent'>reset.</span>", unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-copy">Turn a redacted financial document into a privacy-minimized '
        'evidence profile and a sourced 30-day access plan for your destination—without '
        'inventing a credit score.</div>',
        unsafe_allow_html=True,
    )
    cta, secondary = st.columns([1, 1.15])
    with cta:
        st.page_link("pages/3_Financial_Passport.py", label="Build my Financial Passport", icon=None)
    with secondary:
        st.page_link("pages/1_Term_Translator.py", label="Explore banking terms", icon=None)
    st.markdown(
        '<div class="trust-row"><span class="trust-item">Privacy-minimized output</span>'
        '<span class="trust-item">11 markets</span>'
        '<span class="trust-item">No black-box score</span></div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="result-card" style="margin-top:2.2rem;padding:2rem;">
          <span class="status-pill">FINANCIAL PASSPORT</span>
          <div class="quiet" style="margin-top:1.4rem;">India → United States</div>
          <div class="result-name">Evidence, translated.</div>
          <div style="height:1px;background:rgba(15,35,60,.10);margin:1.3rem 0;"></div>
          <div class="quiet">Privacy-safe signals</div>
          <div style="font-size:1.15rem;font-weight:740;margin-top:.25rem;">Income pattern · Balance continuity · Document readiness</div>
          <p class="result-detail" style="margin-top:.8rem;">A concrete access plan—not a credit score or lending decision.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-label">Start with what you need</div>', unsafe_allow_html=True)
card_columns = st.columns(3, gap="medium")
cards = [
    (
        "01",
        "Build your Passport",
        "Extract safe evidence from a fictional or redacted document and leave with a portable 30-day plan.",
        "pages/3_Financial_Passport.py",
        "Start the safe demo",
    ),
    (
        "02",
        "Translate a product",
        "Type FDR, DPS, BSBDA, or describe how an account works to find its closest destination match.",
        "pages/1_Term_Translator.py",
        "Find a match",
    ),
    (
        "03",
        "Open the right account",
        "Choose checking, savings, high-yield, fixed-term, or basic and get a local opening checklist.",
        "pages/2_Process_Comparison.py",
        "Compare the process",
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

st.markdown('<div class="section-label">11 supported markets</div>', unsafe_allow_html=True)
tags(supported_markets)

st.markdown('<div class="section-label">Designed for clarity</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="result-card">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1.4rem;">
        <div><div class="result-kicker">Substantive AI</div><h3>Documents become structured evidence</h3><p class="result-detail">Vision and strict extraction do real work while direct identifiers stay out of the output.</p></div>
        <div><div class="result-kicker">Explainable</div><h3>No mystery score</h3><p class="result-detail">Every signal shows what the document supports and how confident the extraction is.</p></div>
        <div><div class="result-kicker">Actionable</div><h3>Evidence becomes a plan</h3><p class="result-detail">Users leave with local terminology, required documents, next steps, and sources.</p></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
