"""
Bank Bridge — main app entry point.

Run with: streamlit run Home.py
"""

import streamlit as st

st.set_page_config(
    page_title="Bank Bridge",
    page_icon="🏦",
    layout="centered",
)

st.title("🏦 Bank Bridge")
st.subheader("Understand your money the moment you land")

st.markdown(
    """
Bank Bridge helps newcomers translate their home country's financial
products and banking process into their closest US equivalent — and
translates bank statements for visa, loan, or apartment applications.

**Get started using the sidebar:**
- **Term Translator** — look up a financial product from home and see its
  closest US match
- **Process Comparison** — compare account-opening steps between your home
  country and the US
- **Statement Translator** — upload a bank statement for translation
  *(feature in progress)*

---
"""
)

st.info(
    "⚠️ This app currently uses a **dummy dataset** covering Bangladesh, "
    "India, and the Philippines with a small number of sample products. "
    "Expand `data/financial_products.json` and "
    "`data/account_opening_process.json` with verified data before the demo."
)

st.markdown(
    """
### For the team

- **Person A:** expand the datasets in `/data` — see `DATASET_NOTES.md`
- **Person B:** wire up the real AI calls in `utils/ai_helper.py` — look for
  the `TODO` comments

Both of you can work independently: the front-end pages already work against
the dummy data and a rule-based placeholder explanation, so nothing blocks
either of you from testing your part right now.
"""
)
