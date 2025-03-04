# Chatbot with Retrieval Augmented Generation (RAG)

This project is a Streamlit-based chatbot application that leverages retrieval-augmented generation to answer user questions based on content extracted from a provided URL. By using LangChain, FAISS, and custom prompt engineering, the chatbot retrieves relevant context from web content and uses an OpenAI model to generate concise responses.

## Features

- **Dynamic Context Retrieval:**  
  Input any URL to load and index web content. The application extracts, splits, and stores content in a FAISS vector store for efficient retrieval.

- **Retrieval-Augmented Generation:**  
  Combines retrieved context with a custom prompt to generate accurate and concise answers using an OpenAI model.

- **Interactive Chat Interface:**  
  Built with Streamlit, the interface supports a live conversation history and user-friendly message input.

- **Stateful Conversation:**  
  Maintains chat history across interactions using Streamlit's session state.

## Project Structure

- **app.py:**  
  Implements the Streamlit frontend, including user input handling, conversation state management, and integration with the chat backend.

- **chain.py:**  
  Contains the core logic for content retrieval and response generation. It:
  - Loads web content via a URL.
  - Splits the text using a recursive character text splitter.
  - Builds a FAISS vector store for context retrieval.
  - Creates a retrieval chain with a custom prompt template.
  - Manages a state graph workflow to generate answers.

## Requirements

- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://github.com/hwchase17/langchain) and its dependencies:
  - langchain_core
  - langchain_openai
  - langchain_text_splitters
  - langchain_community
  - langchain_graph
- [FAISS](https://github.com/facebookresearch/faiss)
- An OpenAI API key (set in Streamlit secrets)

Install the required dependencies (assuming a `requirements.txt` file is provided):

```bash
pip install -r requirements.txt
```

## Setup

- Clone the repository
  
  ```bash
  git clone <repository-url>
  cd <repository-directory>
  ```
- Configure the api key
  Create a .streamlit/secrets.toml file (or use your environment variables) with the following content:
  
  ```toml
  [OPENAI_API_KEY]
  OPENAI_API_KEY = "your_openai_api_key_here"
  ```

## Running the application

Launch the chatbot using streamlit

```bash
streamlit run app.py
```

This will open the application in your default web browser.

## Usage Instruction

- Enter the url
    - In the sidebar, provide the URL of a web page from which you want to extract context.
    - Click the Submit button to load the content.
    - **Example:**
      - Open the chatbot interface.
      - Locate the sidebar input field labeled **"Enter your URL"**.
      - Type in a URL (e.g., `https://example.com`).
      - Click the **Submit** button.
- Chat interaction
    - Once the chatbot is ready, type your questions in the text input field.
    - The chatbot will retrieve context from the URL and generate a concise answer.
    - **Example:**
      - Type: `What is the main topic of this article?`
      - The chatbot will respond with a summary based on the retrieved content.
- Exiting the Chat:
    - To end the conversation, type "quit" or "exit".
    - **Example:**
      - User: `exit`
      - Chatbot: `"Goodbye!"`
## Code Overview

- **Frontend(app.py):**
   - Initializes the chat interface using Streamlit. Manages session state for conversation history, handles user inputs, and displays chat messages in a formatted layout.
- **Backend(chain.py):**
   - **Content Loading & Vector Store Creation:**
     <br>
      Uses WebBaseLoader to load web content and a recursive text splitter to process it, storing the result in a FAISS vector store.
   - **Agent Creation & Retrieval Chain:**
     <br>
     Builds a custom retrieval chain using a tailored prompt and integrates with a ChatOpenAI model.
   - **StateGraph Workflow:**
     <br>
     Defines and compiles a state graph workflow that processes incoming messages and returns generated responses.
