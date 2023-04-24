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
    "College Explorer"
]
icons = [
    "🤖",
    "🚀",
    "📖",
    "📹",
    "📈",
    "🔍"
]
category_to_page = {
    "AI Tutor": "ai_tutor",
    "Crash Course": "crash_course",
    "Doc Q&A": "doc_q&a",
    "Video Q&A": "video_q&a",
    "CSV Q&A": "csv_q&a",
    "College Explorer": "college_explorer"
}

category = pills("Choose a tool", options, icons, index=None, clearable=True)

# Check if the category is in the dictionary and switch to the appropriate page
if category in category_to_page:
    switch_page(category_to_page[category])
