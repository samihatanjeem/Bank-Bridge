import streamlit as st
from utils.ai_helper import explain_statement

st.set_page_config(page_title="Statement Translator | Bank Bridge", page_icon="📄")

st.title("📄 Bank Statement Translator")
st.write(
    "Upload a bank statement from your home country to get a translated, "
    "plain-language summary — useful for visa, loan, or apartment applications."
)

st.warning(
    "🚧 **Feature in progress.** The upload works, but the AI translation "
    "call isn't wired up yet — see `utils/ai_helper.py`."
)

uploaded_file = st.file_uploader(
    "Upload a bank statement (PDF or image)",
    type=["pdf", "png", "jpg", "jpeg"],
)

if uploaded_file is not None:
    st.success(f"Received: {uploaded_file.name}")

    if st.button("Translate this statement", type="primary"):
        with st.spinner("Processing..."):
            file_bytes = uploaded_file.read()
            result = explain_statement(file_bytes, uploaded_file.name)
        st.markdown("---")
        st.markdown(result)

st.markdown("---")
st.caption(
    "⚠️ Do not upload real personal financial documents while this feature "
    "is still in development / not yet security-reviewed. Use a sample or "
    "redacted statement for testing."
)
