import streamlit as st
from utils.data_loader import load_account_opening_process, get_process_for_country

st.set_page_config(page_title="Process Comparison | Bank Bridge", page_icon="📋")

st.title("📋 Account-Opening Process Comparison")
st.write(
    "See how opening a bank account back home compares to opening one in "
    "the US — same steps highlighted, different steps flagged."
)

processes = load_account_opening_process()
countries = sorted({p["country"] for p in processes if p["country"] != "United States"})

origin_country = st.selectbox("Your home country", countries)

origin_process = get_process_for_country(processes, origin_country)
us_process = get_process_for_country(processes, "United States")

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🏠 {origin_country}")
    if origin_process:
        for i, step in enumerate(origin_process["steps"], 1):
            st.write(f"{i}. {step}")
        st.markdown("**Typical requirements:**")
        for req in origin_process["typical_requirements"]:
            st.write(f"- {req}")
    else:
        st.warning("No data yet for this country.")

with col2:
    st.subheader("🇺🇸 United States")
    if us_process:
        for i, step in enumerate(us_process["steps"], 1):
            st.write(f"{i}. {step}")
        st.markdown("**Typical requirements:**")
        for req in us_process["typical_requirements"]:
            st.write(f"- {req}")
    else:
        st.warning("No US data found.")

if origin_process:
    st.markdown("---")
    st.subheader("💡 Notes")
    st.write(origin_process.get("notes", "No additional notes."))
    if us_process:
        st.write(us_process.get("notes", ""))

    with st.expander("Sources"):
        for process in [origin_process, us_process]:
            if not process:
                continue
            st.markdown(f"**{process['country']}**")
            for source in process.get("sources", []):
                st.markdown(f"- [{source['title']}]({source['url']})")

st.markdown("---")
st.caption(
    "Informational overview only. Requirements vary by bank and customer; "
    "confirm the current process with the institution."
)
