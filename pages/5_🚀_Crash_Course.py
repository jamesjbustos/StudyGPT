import streamlit as st


# Streamlit page configurations and title
st.set_page_config(
    page_title="StudyGPT",
    page_icon=":mortar_board:"
)
st.title("🚀 Crash Course")
st.caption("🌟 Your ultimate learning companion - choose any topic and accelerate your growth!")


# Load API Key
api_key = st.secrets["OPENAI_API_KEY"]