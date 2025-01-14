import os
import json
from typing import List, Dict, Any
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
    
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def process_query(process_input) -> Dict[str, Any]:
    try:
        # Parse JSON data
        try:
            texts = parse_json_data(process_input["college_file_path"])
        except json.JSONDecodeError as e:
            return {
                "output_text": f"Error parsing JSON: {str(e)}",
                "source": "Error",
                "status": "failed"
            }
        except Exception as e:
            return {
                "output_text": f"Error loading JSON data: {str(e)}",
                "source": "Error",
                "status": "failed"
            }

        # Create vector store
        try:
            vector_store = create_vector_store(texts)
        except Exception as e:
            return {
                "output_text": f"Error creating vector store: {str(e)}",
                "source": "Error",
                "status": "failed"
            }

        # Perform similarity search
        try:
            docs = vector_store.similarity_search(process_input["user_question"])
        except Exception as e:
            return {
                "output_text": f"Error performing similarity search: {str(e)}",
                "source": "Error",
                "status": "failed"
            }

        # Create RAG chain and get response
        try:
            chain = get_conversational_chain()
            response = chain({"input_documents": docs, "question": process_input["user_question"]}, return_only_outputs=True)
        except Exception as e:
            return {
                "output_text": f"Error creating RAG chain or getting response: {str(e)}",
                "source": "Error",
                "status": "failed"
            }

        rag_output = response.get('output_text', "answer is not available in the context")

        print("rag_output: ", rag_output)
        image_urls = re.findall(r'(https?://[^\s]+)', rag_output)
        return {
            "output_text": rag_output,
            "image_urls": image_urls,
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