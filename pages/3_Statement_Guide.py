import html

import streamlit as st

from utils.ui import apply_theme, brand, page_intro, tags


st.set_page_config(
    page_title="Statement Guide | BankBridge",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()
brand()

page_intro(
    "Statement guide",
    "Share the right document—with less guesswork.",
    "Understand the sections reviewers look for, check whether your file is ready, and learn what to hide before sending a statement to someone else.",
)

purpose = st.segmented_control(
    "What are you trying to do?",
    ["Understand my statement", "Prepare an application", "Share it safely"],
    default="Understand my statement",
)

if purpose == "Understand my statement":
    st.markdown('<div class="section-label">Common statement language</div>', unsafe_allow_html=True)
    terms = [
        ("Statement period", "The start and end dates covered by this document."),
        ("Opening balance", "The amount in the account at the beginning of the period."),
        ("Credits / deposits", "Money added to the account, including transfers or salary."),
        ("Debits / withdrawals", "Money leaving the account through payments, cash, fees, or transfers."),
        ("Closing balance", "The recorded balance at the end of the statement period."),
        ("Available balance", "What the bank says is available now; pending activity can make this differ from the closing balance."),
    ]
    left, right = st.columns(2, gap="medium")
    for index, (term, meaning) in enumerate(terms):
        with left if index % 2 == 0 else right:
            st.markdown(
                f'<div class="feature-card" style="min-height:145px;margin-bottom:1rem;">'
                f'<div class="result-kicker">{html.escape(term)}</div>'
                f'<p style="margin-top:.7rem;color:#465469;">{html.escape(meaning)}</p></div>',
                unsafe_allow_html=True,
            )

elif purpose == "Prepare an application":
    st.markdown('<div class="section-label">A reviewer usually needs</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="result-card">
          <div class="result-name" style="font-size:1.45rem;">Make the document easy to verify</div>
          <p class="result-detail">Requirements differ for rentals, loans, visas, and schools. Ask for the exact date range and whether a translation or bank stamp is required.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    tags(
        [
            "Account holder name visible",
            "Bank name visible",
            "Statement period visible",
            "All requested pages included",
            "Currency identified",
            "Official translation if required",
        ]
    )
    st.info("Do not edit transaction amounts or balances. If redaction is allowed, keep an unmodified original for your records.")

else:
    st.markdown('<div class="section-label">Redact before you send</div>', unsafe_allow_html=True)
    hide_col, keep_col = st.columns(2, gap="large")
    with hide_col:
        st.markdown("### Usually safe to hide")
        tags(["Full account number", "QR codes", "Login details", "Card number", "Unrelated personal identifiers"])
    with keep_col:
        st.markdown("### Usually needed for verification")
        tags(["Your name", "Bank name", "Statement dates", "Relevant balances", "Requested transactions", "Currency"])
    st.warning("Confirm redaction rules with the recipient first. Visa, loan, and legal processes may reject altered documents.")

st.markdown('<div class="section-label">Optional file readiness check</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Choose a PDF or image",
    type=["pdf", "png", "jpg", "jpeg"],
    help="The MVP checks format and size only. It does not read, upload onward, or store your document.",
)

if uploaded_file is not None:
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > 10:
        st.error(f"This file is {size_mb:.1f} MB. Reduce it to 10 MB or less before sharing.")
    else:
        st.success(f"{uploaded_file.name} is in a supported format and ready for review ({size_mb:.1f} MB).")
        st.caption("BankBridge has not read or translated the document. The file remains in this session's memory only.")

st.markdown("---")
st.caption(
    "Privacy first: never upload a real financial document to a service unless you "
    "understand how it stores, processes, and deletes your data."
)
