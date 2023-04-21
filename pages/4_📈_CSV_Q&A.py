# Import libraries
import pandas as pd
import os

# Llama Index & Langchain libraries
from llama_index import download_loader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
from llama_index import download_loader
from pathlib import Path

# Streamlit page configurations and title
st.set_page_config(
    page_title="StudyGPT",
    page_icon=":mortar_board:"
)
st.title("📈 CSV Q&A")
st.caption("🌟 Your personal CSV data assistant - upload and start asking questions!")

# Path to documents and index file
doc_path = './CSVdata/'
index_file = 'CSVindex.json'

index = None

# Load API Key

api_key = st.secrets["OPENAI_API_KEY"]


# ------ Initialize Session State ------
if 'csv_response' not in st.session_state:
    st.session_state.csv_response = ''
    
    
# ------ Load and index document ------
uploaded_file = st.file_uploader(" ", accept_multiple_files=False, label_visibility='collapsed')

if uploaded_file is not None:
    # Clear existing documents
    for doc_file in os.listdir(doc_path):
        os.remove(os.path.join(doc_path, doc_file))
    
    # Save uploaded file to doc_path
    with open(os.path.join(doc_path, uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.read())

    # Load and index document
    uploaded_file_path = os.path.join(doc_path, uploaded_file.name)
    SimpleCSVReader = download_loader("SimpleCSVReader")
    loader = SimpleCSVReader()
    documents = loader.load_data(file=Path(uploaded_file_path))
    
    # Display uploaded CSV file as DataFrame (new lines added)
    df = pd.read_csv(uploaded_file_path)
    st.dataframe(df)
    
    # Define llm and index
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
    prompt_helper = PromptHelper(max_input_size=4096, num_output=256, max_chunk_overlap=20)
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
    
    # Save index to file
    index.save_to_disk(index_file)

elif os.path.exists(index_file):
    index = GPTSimpleVectorIndex.load_from_disk(index_file)
    
    SimpleCSVReader = download_loader("SimpleCSVReader")
    loader = SimpleCSVReader()
    uploaded_file_path = os.path.join(doc_path, os.listdir(doc_path)[0])
    documents = loader.load_data(file=Path(uploaded_file_path))

if index is not None:
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([10, 1])
        user_prompt = col1.text_area(" ", max_chars=2000, key="prompt", placeholder="Type your question here...", label_visibility="collapsed")
        submitted = col2.form_submit_button("💬")

    if submitted and user_prompt:
        st.session_state.csv_response = index.query(user_prompt)
        response_md = f"🤖 **AI:** {st.session_state.csv_response}\n\n---"
        st.markdown(response_md)

