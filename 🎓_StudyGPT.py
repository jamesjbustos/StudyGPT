# Import necessary libraries
import streamlit as st
from streamlit_pills import pills
from streamlit_extras.switch_page_button import switch_page

# Create a Streamlit page config
st.set_page_config(
    page_title="StudyGPT",
    page_icon=":mortar_board:",
    initial_sidebar_state = "collapsed"
)

# Title
st.title("🎓StudyGPT")
st.subheader("Powered by :blue[OpenAI] + :blue[Streamlit] + :blue[Langchain] + :blue[LlamaIndex]")
    
#Define tools
options = [
    "AI Tutor",
    "Crash Course",
    "Doc Q&A",
    "Video Q&A",
    "CSV Q&A",
    "Nexus"
]
icons = [
    "🤖",
    "🚀",
    "📖",
    "🕹️",
    "📈",
    "🔗"
]
category_to_page = {
    "AI Tutor": "ai_tutor",
    "Crash Course": "crash_course",
    "Doc Q&A": "doc_q&a",
    "Video Q&A": "video_q&a",
    "CSV Q&A": "csv_q&a",
    "Nexus": "nexus"
}

category = pills("Select a tool", options, icons, index=None, clearable=True)

# Check if the category is in the dictionary and switch to the appropriate page
if category in category_to_page:
    switch_page(category_to_page[category])

st.write('---')

# Description
st.markdown('''##### 🤖 AI Tutor
Learn from an advanced AI tutor. Ask questions, get explanations and interact with the tutor in a chat-based format.''')

st.markdown('''##### 🚀 Crash Course
Quickly learn any topic with a AI-powered Crash Course feature. Enter a topic and receive a personalized crash course in just under a minute.''')

st.markdown('''##### 📖 Doc Q&A
Get quick answers to your PDF-related questions with a easy-to-use Doc Q&A feature. Simply upload your PDF, ask your questions and receive instant responses.''')

st.markdown('''##### 🕹️ Video Q&A 
Get quick answers to your video-related questions with a easy-to-use Video Q&A feature. Simply upload your video, ask your questions and receive instant responses.''')

st.markdown('''##### 📈 CSV Q&A
Get quick answers to your CSV-related questions with our easy-to-use CSV Q&A feature. Simply upload your CSV file, ask your questions and receive instant responses.''')

st.write('---')
