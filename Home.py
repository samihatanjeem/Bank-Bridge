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
    "The product mapper uses a small, sourced dataset covering Bangladesh, "
    "India, and the Philippines. It can classify a local name or short product "
    "description, and it declines low-confidence matches."
)

st.markdown(
    """
### How mappings are made

- Product names, aliases, descriptions, and mechanics are drawn from the
  cited regulator and provider pages in the dataset.
- An explainable text classifier routes the input to a reviewed US category.
- The displayed comparison comes from the matching evidence record rather
  than being generated freely.

Mappings are educational analogies, not claims that products are legally or
financially identical.
"""
)
