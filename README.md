# StudyGPT

StudyGPT is an AI-powered project that aims to provide learners and students with various tools to enhance their learning experience. The application introduces AI usage for non-technical users, specifically targeting learners and students.

## Application Objective:

StudyGPT serves as an AI-powered application designed to address the requirements of learners and students. Its purpose is to empower users with AI-driven solutions, making learning more efficient and effective. The application focuses on providing a range of features tailored to the needs of non-technical individuals.

## Features:

### Main Page:
The main page serves as a directory, providing users with easy access to all available features:

1. **AI Tutor**: Powered by OpenAI's GPT-3.5-turbo LLM, the AI Tutor feature allows users to interact with a tutor system in a chat-based format.

2. **Doc Q & A**: This feature enables users to submit PDF documents and interact with them by asking questions. The application parses the document, splits the text, and utilizes OpenAI embeddings for indexing and responding to queries.

3. **Video Q & A**: Similar to Doc Q & A, this feature accepts YouTube links and uses the video transcript to allow users to interact with the content through queries.

4. **Crash Course**: Utilizing GPT-3.5-turbo and Asynchronous calls, Crash Course generates short, informative modules to teach users the basics of any topic they specify.

## Tech Stack:

- **OpenAI - GPT-3.5-turbo LLM**: The core AI model responsible for powering several features in StudyGPT.

- **Streamlit**: The application is built using Streamlit, a user-friendly Python library for creating interactive web applications.

- **Langchain**: Langchain technology is utilized to handle natural language processing tasks within the application.

- **LlamaIndex**: The LlamaIndex library is used for embedding text and indexing documents in Doc Q & A and Video Q & A features.

- **Pinecone**: Pinecone is a vector database designed for machine learning applications and is a powerful tool for efficient and accurate vector-based search.

## Installation:

To run StudyGPT locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/jamesjbustos/StudyGPT.git
   cd StudyGPT
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `secrets.toml` file under the `.streamlit` folder with the following values:

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY=""
PINECONE_API_KEY=""
PINECONE_ENVIRONMENT=""
```

OpenAI API Key:

- Create an account and register for an API key [here.](https://platform.openai.com/signup)

Pinecone Instructions:

1. Create an account on [Pinecone](https://www.pinecone.io/).

2. Create an index under "Indexes." This project uses the index name "studygpt-index," but you can refactor it for your custom index.

3. When creating the index, ensure the following settings are applied:
   - Dimensions = 1536
   - (Optional) Pod type: S1
   - (Optional) Metric: Cosine

4. Your Pinecone API key will be available in your dashboard, and the pinecone environment is accessible after the index is created.

### Disclaimer
Working streamlit demo is limited to a certain amount of API calls. It's exepensive, sorry.