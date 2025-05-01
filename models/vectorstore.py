"""
Vector database operations and management.
"""
import streamlit as st
from langchain_chroma import Chroma

def load_or_create_vectorstore(embeddings, documents=None):
    """
    Load an existing vector store or create a new one with the provided documents.
    
    Args:
        embeddings: Embedding model to use
        documents: List of document chunks to add to the vector store (optional)
        
    Returns:
        Chroma vector store object or None if operation fails
    """
    vectorstore_path = "./chroma_store"
    
    # If documents are provided, add them to the vector store
    if documents and len(documents) > 0:
        try:
            vectorstore = Chroma(
                embedding_function=embeddings,
                persist_directory=vectorstore_path
            )
            
            # Add documents to vectorstore
            vectorstore.add_documents(documents)
            st.success(f"Added {len(documents)} document chunks to the vector database.")
            return vectorstore
        except Exception as vector_error:
            st.error(f"Failed to add documents to vector database: {str(vector_error)}")
            st.info("This might be due to file permission issues or database corruption.")
            return None
    
    # If no documents are provided, load the existing vector store
    else:
        try:
            vectorstore = Chroma(
                embedding_function=embeddings,
                persist_directory=vectorstore_path
            )
            
            # Check if vectorstore has been initialized
            vector_content = vectorstore.get()
            if not vector_content["ids"]:
                st.warning("No documents found in vectorstore. Please upload a PDF.")
                return None
                
            return vectorstore
        except FileNotFoundError:
            st.warning("Vector database not found. Please upload a PDF to initialize.")
            return None
        except Exception as e:
            st.error(f"Failed to load vectorstore: {str(e)}")
            st.info("The vector database might be corrupted. You may need to delete the './chroma_store' directory and upload PDFs again.")
            return None
