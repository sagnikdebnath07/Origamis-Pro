from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, embeddings
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph import START, MessagesState, StateGraph
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
import streamlit as st
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

openai_api_key=st.secrets["OPENAI_API_KEY"]
embedding=embeddings.OpenAIEmbeddings(api_key=openai_api_key,model="text-embedding-3-large")

def vectorStoreMaker(url:str):
    loader = WebBaseLoader(url)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    vectorstore = FAISS.from_documents(documents=all_splits, embedding=embedding)
    return vectorstore

def createAgent(url:str):
    vectorstore = vectorStoreMaker(url)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    llm=ChatOpenAI(model="gpt-4o-mini")
    system_prompt =''' You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If answer does not require context, use your own judgement to answer. Keep the answer concise.
    Context: {context}
    Question: {question}  
    Answer:
    '''
    prompt = ChatPromptTemplate.from_template(
            system_prompt
        )
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(vectorstore.as_retriever(), combine_docs_chain)

    workflow = StateGraph(state_schema=MessagesState)

    def call_model(state: MessagesState):
        messages = state["messages"]
        response = rag_chain.invoke({"role": "user", "content":messages[0].content,"input": messages[0].content, "question": messages[0].content})
        return {"messages": response}

    workflow.add_node("model", call_model)
    workflow.add_edge(START, "model")

    app = workflow.compile()
    config={"configurable": {"thread_id": "1"}}

    return app,config

def handle_chat(query,app,config):
    messages = HumanMessage(content=query)
    response = app.invoke({"messages": messages}, config=config)
    return response["messages"][1].additional_kwargs['answer']
#print(handle_chat("What is reverse diffusion?"))
