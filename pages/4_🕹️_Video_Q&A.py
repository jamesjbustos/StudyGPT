# Import libraries
import streamlit as st
import pandas as pd
import os
import pinecone
from pathlib import Path
from llama_index import (download_loader, LLMPredictor,
                         PromptHelper, ServiceContext, GPTPineconeIndex)
from langchain import OpenAI

# Streamlit page configurations and title
st.set_page_config(
    page_title="StudyGPT",
    page_icon=":mortar_board:",
    initial_sidebar_state = "collapsed"
)
st.title("🕹️ Youtube Q&A")
st.caption("✨ Your personal video assistant - upload and start asking questions!")

index = None

# Load API Key
api_key = st.secrets["OPENAI_API_KEY"]
pinecone_api_key = st.secrets["PINECONE_API_KEY"]
pinecone_enviroment = st.secrets["PINECONE_ENVIRONMENT"]

# ------ Initialize Session State ------
if 'vid_response' not in st.session_state:
    st.session_state.vid_response = ''


# ------ Load and index video ------
video_link = st.text_input("Enter the link to your YouTube video 👇")

if video_link:

    # Load and index video
    YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader")
    loader = YoutubeTranscriptReader()
    documents = loader.load_data(ytlinks=[video_link])

    # Pinecone intialization
    pinecone.init(
        api_key=pinecone_api_key,
        environment=pinecone_enviroment
    )
    pinecone_index = pinecone.Index("studygpt")

    # Display uploaded CSV file as DataFrame
    st.video(video_link)

    # Define llm and index
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
    prompt_helper = PromptHelper(max_input_size=4096, num_output=256, max_chunk_overlap=20)
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    # Create the GPTPineconeIndex
    index = GPTPineconeIndex.from_documents(
        documents,
        pinecone_index=pinecone_index,
        service_context=service_context,
        add_sparse_vector=True,
    )

if index is not None:
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([10, 1])
        user_prompt = col1.text_area(" ", max_chars=2000, key="prompt",
                                      placeholder="Type your question here...", label_visibility="collapsed")
        submitted = col2.form_submit_button("💬")

    if submitted and user_prompt:
        with st.spinner("💭 Waiting for response..."):
            st.session_state.vid_response = index.query(user_prompt)
        response_md = f"🤖 **AI:** {st.session_state.vid_response}\n\n"
        st.markdown(response_md)
