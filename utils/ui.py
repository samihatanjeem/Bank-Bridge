"""Shared presentation helpers for the Streamlit experience."""

import html
from typing import Iterable

import streamlit as st


THEME_CSS = """
<style>
    :root {
        --ink: #0b1628;
        --muted: #5c6879;
        --line: rgba(15, 35, 60, 0.11);
        --surface: rgba(255, 255, 255, 0.84);
        --navy: #08182e;
        --teal: #13b8a6;
        --blue: #2f6df6;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(47, 109, 246, 0.10), transparent 28rem),
            radial-gradient(circle at 92% 8%, rgba(19, 184, 166, 0.10), transparent 26rem),
            #f6f8fb;
        color: var(--ink);
    }
    .block-container {max-width: 1120px; padding-top: 2.2rem; padding-bottom: 5rem;}
    [data-testid="stSidebar"] {background: #071426; border-right: 1px solid rgba(255,255,255,.07);}
    [data-testid="stSidebar"] * {color: #dbe8f7;}
    [data-testid="stSidebarNav"] span {font-weight: 560;}
    [data-testid="stHeader"] {background: transparent;}

    h1, h2, h3 {color: var(--ink); letter-spacing: -0.035em;}
    h1 {font-size: clamp(2.45rem, 6vw, 4.7rem) !important; line-height: 0.99 !important;}
    p {line-height: 1.65;}

    .brand {display:flex; align-items:center; gap:.7rem; margin-bottom: 4.2rem; font-weight:760; color:var(--navy);}
    .brand-mark {width:28px; height:28px; border-radius:9px; background:linear-gradient(135deg,var(--blue),var(--teal)); box-shadow:0 7px 20px rgba(47,109,246,.25);}
    .eyebrow {font-size:.72rem; font-weight:760; letter-spacing:.16em; text-transform:uppercase; color:#167f76; margin-bottom:.8rem;}
    .hero-copy {font-size:1.18rem; color:var(--muted); max-width:680px; margin:.9rem 0 2rem;}
    .accent {background:linear-gradient(110deg,var(--blue),var(--teal)); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
    .section-label {font-size:.75rem; font-weight:740; letter-spacing:.12em; text-transform:uppercase; color:#657387; margin:3.5rem 0 1rem;}

    .feature-card, .result-card, .step-card, .source-panel {
        background:var(--surface); border:1px solid var(--line); border-radius:20px;
        box-shadow:0 16px 44px rgba(22,42,72,.07); backdrop-filter:blur(14px);
    }
    .feature-card {padding:1.45rem; min-height:205px;}
    .feature-card .number {font-size:.72rem; font-weight:760; color:#167f76; letter-spacing:.12em;}
    .feature-card h3 {font-size:1.3rem; margin:.8rem 0 .45rem;}
    .feature-card p {font-size:.93rem; color:var(--muted); margin:0;}
    .feature-card .arrow {display:block; margin-top:1.2rem; color:var(--blue); font-weight:700;}
    .result-card {padding:1.65rem 1.75rem; margin:1rem 0;}
    .result-kicker {font-size:.72rem; color:#167f76; font-weight:760; letter-spacing:.12em; text-transform:uppercase;}
    .result-name {font-size:1.8rem; color:var(--ink); font-weight:760; letter-spacing:-.035em; margin:.35rem 0;}
    .result-detail {color:var(--muted); margin:0;}
    .step-card {padding:1.2rem 1.35rem; margin:.65rem 0; min-height:96px; display:flex; gap:1rem; align-items:flex-start;}
    .step-number {min-width:30px; height:30px; border-radius:10px; background:#eaf0ff; color:var(--blue); font-size:.78rem; font-weight:780; display:flex; align-items:center; justify-content:center;}
    .step-text {font-size:.94rem; color:#344156; padding-top:.18rem;}
    .tag {display:inline-block; padding:.4rem .65rem; margin:.2rem .25rem .2rem 0; border:1px solid var(--line); border-radius:999px; background:white; color:#465469; font-size:.78rem;}
    .trust-row {display:flex; flex-wrap:wrap; gap:1.4rem; color:#657387; font-size:.78rem; margin-top:2.2rem;}
    .trust-item:before {content:'✓'; color:var(--teal); font-weight:800; margin-right:.4rem;}
    .status-pill {display:inline-block; background:#e8f8f5; color:#0f756b; border-radius:999px; padding:.38rem .66rem; font-size:.72rem; font-weight:760;}
    .beta-pill {display:inline-block; background:#edf1ff; color:#365fce; border-radius:999px; padding:.38rem .66rem; font-size:.72rem; font-weight:760;}
    .quiet {font-size:.82rem; color:#718095;}

    .stButton > button, [data-testid="stPageLink"], [data-testid="stPageLink"] a {
        border-radius:12px !important; font-weight:700 !important; min-height:2.8rem;
        transition:transform .15s ease, box-shadow .15s ease;
    }
    [data-testid="stPageLink"] {border:1px solid var(--line); background:rgba(255,255,255,.76); padding:0 .25rem;}
    .stButton > button[kind="primary"] {background:linear-gradient(110deg,var(--blue),#285bd1); border:0; box-shadow:0 9px 22px rgba(47,109,246,.23);}
    .stButton > button:hover, [data-testid="stPageLink"] a:hover {transform:translateY(-1px);}
    [data-baseweb="select"] > div, .stTextInput input, [data-testid="stFileUploaderDropzone"] {
        border-radius:13px !important; border-color:rgba(22,42,72,.14) !important; background:rgba(255,255,255,.88) !important;
    }
    [data-testid="stExpander"] {border:1px solid var(--line); border-radius:14px; background:rgba(255,255,255,.64);}
    .stAlert {border-radius:14px;}
    [data-testid="stToolbarActions"], [data-testid="stAppDeployButton"], #MainMenu, footer {display:none;}

    @media (max-width: 700px) {
        .block-container {padding-top:1.4rem;}
        .brand {margin-bottom:2.8rem;}
        .feature-card {min-height:auto;}
    }
</style>
"""


def apply_theme() -> None:
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def brand() -> None:
    st.markdown(
        '<div class="brand"><span class="brand-mark"></span><span>BankBridge</span></div>',
        unsafe_allow_html=True,
    )


def page_intro(eyebrow: str, title: str, description: str) -> None:
    st.markdown(f'<div class="eyebrow">{html.escape(eyebrow)}</div>', unsafe_allow_html=True)
    st.markdown(f"# {title}")
    st.markdown(f'<div class="hero-copy">{html.escape(description)}</div>', unsafe_allow_html=True)


def steps(items: Iterable[str]) -> None:
    cards = "".join(
        '<div class="step-card"><div class="step-number">{}</div>'
        '<div class="step-text">{}</div></div>'.format(index, html.escape(item))
        for index, item in enumerate(items, 1)
    )
    st.markdown(cards, unsafe_allow_html=True)


def tags(items: Iterable[str]) -> None:
    markup = "".join(f'<span class="tag">{html.escape(item)}</span>' for item in items)
    st.markdown(markup, unsafe_allow_html=True)


def source_links(sources: Iterable[dict]) -> None:
    for source in sources:
        st.markdown(f"[{source['title']}]({source['url']})")
