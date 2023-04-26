# Import libraries
import streamlit as st
import pandas as pd
import os
from langchain import OpenAI
from langchain.agents import create_csv_agent

# Streamlit page configurations and title
st.set_page_config(
    page_title="StudyGPT",
    page_icon=":mortar_board:"
)
st.title("📈 CSV Q&A")
st.caption("✨ Your personal CSV data assistant - upload and start asking questions!")

# Load API Key
api_key = st.secrets["OPENAI_API_KEY"]

# ------ Initialize Session State ------
if 'csv_response' not in st.session_state:
    st.session_state.csv_response = ''

# ------ Helper functions ------
def save_uploaded_file(uploadedfile):
    with open(os.path.join("data", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

# ------ Load and index document ------
uploaded_file = st.file_uploader(" ", accept_multiple_files=False,
                                  label_visibility='collapsed', type=['csv'])

# ------ Create agent and chat ------
if uploaded_file is not None:
    # Create data folder if it doesn't exist
    if not os.path.exists('./data'):
        os.mkdir('./data')

    # Save uploaded file to data folder
    save_uploaded_file(uploaded_file)

    # Load and index document
    uploaded_file_path = os.path.join('data', uploaded_file.name)
    
    # Create agent
    agent = create_csv_agent(OpenAI(temperature=0), uploaded_file_path, verbose=True)

    # Display uploaded CSV file as DataFrame
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([10, 1])
        user_prompt = col1.text_area(" ", max_chars=2000, key="prompt",
                                      placeholder="Type your question here...", label_visibility="collapsed")
        submitted = col2.form_submit_button("💬")

    if submitted and user_prompt:
        with st.spinner("💭 Waiting for response..."):
            st.session_state.csv_response = agent.run(user_prompt)
        response_md = f"🤖 **AI:** {st.session_state.csv_response}\n\n"
        st.markdown(response_md)
        