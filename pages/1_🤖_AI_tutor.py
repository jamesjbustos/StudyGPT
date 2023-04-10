# Import necessary libraries
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from streamlit_chat import message

# Create a Streamlit page config
st.set_page_config(
    page_title="StudyGPT",
    page_icon=":mortar_board:"
)

#Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []


api_key = st.secrets["api_secret"]

st.title("🤖 AI Tutor")

def load_chain():
    """Logic for loading the chain"""
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=api_key,
        model_name="gpt-3.5-turbo",
        verbose=False
    )
    return llm

llm = load_chain()

#Create conversation memory
if 'entity_memory' not in st.session_state:
    st.session_state.entity_memory = ConversationEntityMemory(llm = llm, k = 10)
    
#Create conversation chain
Conversation = ConversationChain (
    llm = llm,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=st.session_state.entity_memory,
)

#Define function to get user input
def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text 


user_input = get_text()

if user_input:
    output = Conversation.run(input = user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

