import os
from typing import List, Dict, Any
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document

# Load environment variables
load_dotenv()

# Configure Google API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API key not found in environment variables")

genai.configure(api_key=api_key)

def load_data_source(file_path: str) -> str:
    """Load data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return ""
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return ""

def get_text_chunks(text: str, chunk_size: int = 10000, chunk_overlap: int = 1000) -> List[str]:
    """Split text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)

def get_vector_store(text_chunks: List[str]) -> None:
    """Create and save vector store from text chunks."""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
    except Exception as e:
        st.error(f"Error creating vector store: {e}")

def get_conversational_chain():
    """Create a conversational chain for question answering."""
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not in the provided context, just say, "answer is not available in the context".
    
    Context:
    {context}
    
    Question: 
    {question}
    
    Answer:
    """
    
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def user_input(user_question: str) -> Dict[str, Any]:
    """Process user input and generate response."""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        
        # Perform similarity search
        docs = new_db.similarity_search(user_question)
        
        # Create conversational chain
        chain = get_conversational_chain()
        
        # Get response
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )
        
        return {
            "output_text": response.get('output_text', 'No response generated'),
            "status": "success"
        }
    
    except Exception as e:
        return {
            "output_text": f"Error processing question: {str(e)}",
            "status": "error"
        }