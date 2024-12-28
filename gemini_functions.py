# import os
# import json
# from typing import List, Dict, Any
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate

# # Load environment variables
# load_dotenv()

# # Configure Google API
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     raise ValueError("Google API key not found in environment variables")

# genai.configure(api_key=api_key)

# def parse_json_data(file_path: str) -> List[str]:
#     """
#     Robustly parse JSON data and extract text content.
#     Handles various JSON structures.
#     """
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             data = json.load(file)
        
#         # Function to extract text from different possible structures
#         def extract_text(item):
#             # If item is a dictionary, try to get 'content' or convert to string
#             if isinstance(item, dict):
#                 return str(item.get('content', item.get('text', str(item))))
#             # If item is already a string, return it
#             elif isinstance(item, str):
#                 return item
#             # Convert other types to string
#             return str(item)
        
#         # Handle different JSON structures
#         if isinstance(data, list):
#             # List of items
#             texts = [extract_text(item) for item in data]
#         elif isinstance(data, dict):
#             # Single dictionary or nested structure
#             texts = [extract_text(data)]
#         else:
#             # Fallback: convert to string
#             texts = [str(data)]
        
#         # Filter out empty strings
#         texts = [text for text in texts if text.strip()]
        
#         if not texts:
#             raise ValueError("No valid text content found in the JSON file")
        
#         return texts
    
#     except json.JSONDecodeError:
#         raise ValueError(f"Invalid JSON format in {file_path}")
#     except Exception as e:
#         raise ValueError(f"Error parsing JSON: {str(e)}")

# def create_vector_store(texts: List[str]):
#     """Create and save vector store from texts."""
#     try:
#         embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         vector_store = FAISS.from_texts(texts, embedding=embeddings)
#         vector_store.save_local("faiss_index")
#         return vector_store
#     except Exception as e:
#         raise ValueError(f"Error creating vector store: {e}")

# def get_conversational_chain():
#     """Create a conversational chain for question answering."""
    
#     prompt_template = """
#     Answer the question as detailed as possible from the provided context.
#     If the answer is not in the provided context, just say, "answer is not available in the context".
    
#     Context:
#     {context}
    
#     Question: 
#     {question}
    
#     Answer:
#     """
    
#     model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
#     prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
#     return load_qa_chain(model, chain_type="stuff", prompt=prompt)

# def process_query(user_question: str, json_path: str = "output.json") -> Dict[str, Any]:
#     """Process user input using RAG and generate a response."""
#     # Parse JSON data
#     texts = parse_json_data(json_path)
    
#     # Initialize embeddings model
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
#     # Create vector store
#     vector_store = create_vector_store(texts)
    
#     # Perform similarity search
#     docs = vector_store.similarity_search(user_question)
    
#     # Create conversational chain
#     chain = get_conversational_chain()
    
#     # Get response
#     response = chain(
#         {"input_documents": docs, "question": user_question},
#         return_only_outputs=True
#     )
    
#     return {
#         "output_text": response.get('output_text', 'No response generated'),
#         "status": "success"
#         }

        # else:
        #     model = genai.GenerativeModel("gemini-pro")
        #     response = model.generate_content(user_question)
        #     return {
        #         "output_text": response.text,
        #         "source": "Gemini General Capabilities",
        #         "status": "success"
        #     }


import os
import json
from typing import List, Dict, Any
import streamlit as st
import re
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Configure Google API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API key not found in environment variables")

genai.configure(api_key=api_key)

def parse_json_data(file_path: str) -> List[str]:
    """
    Robustly parse JSON data and extract text content.
    Handles various JSON structures.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        def extract_text(item):
            if isinstance(item, dict):
                return str(item.get('content', item.get('text', str(item))))
            elif isinstance(item, str):
                return item
            return str(item)
        
        if isinstance(data, list):
            texts = [extract_text(item) for item in data]
        elif isinstance(data, dict):
            texts = [extract_text(data)]
        else:
            texts = [str(data)]
        
        texts = [text for text in texts if text.strip()]
        
        if not texts:
            raise ValueError("No valid text content found in the JSON file")
        
        return texts
    
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {file_path}")
    except Exception as e:
        raise ValueError(f"Error parsing JSON: {str(e)}")

def create_vector_store(texts: List[str]):
    """Create and save vector store from texts."""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(texts, embedding=embeddings)
        vector_store.save_local("faiss_index")
        return vector_store
    except Exception as e:
        raise ValueError(f"Error creating vector store: {e}")

def get_conversational_chain():
    """Create a conversational chain for question answering."""
    
    prompt_template = """
    Answer the question as detailed as possible from the provided context
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

def process_query(user_question: str, json_path: str = "output.json") -> Dict[str, Any]:
    """Process user input using RAG method and fallback to Gemini API if needed."""
    try:
        # Parse JSON data
        texts = parse_json_data(json_path)

        # Create vector store
        vector_store = create_vector_store(texts)

        # Perform similarity search
        docs = vector_store.similarity_search(user_question)
        
        # Create RAG chain and get response
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

        rag_output = response.get('output_text', "answer is not available in the context")
        
        # if "answer is not available in the context" in rag_output.lower():

        #     # Fallback to Gemini API for general questions
        #     model = genai.GenerativeModel("gemini-pro")
        #     response = model.generate_content(user_question)
        #     return {
        #         "output_text": response.text,
        #         "source": "Gemini General Capabilities",
        #         "status": "success",
        #         "context": "not found"
        #     }
        print("rag_output: ", rag_output)
        image_urls = re.findall(r'(https?://[^\s]+)', rag_output)
        return {
            "output_text": rag_output,
            "image_urls":image_urls,
            "source": "JSON-based RAG",
            "status": "success",
            "context": "found"
        }
    except Exception as e:
        return {
            "output_text": str(e),
            "source": "Error",
            "status": "failed"
        }

