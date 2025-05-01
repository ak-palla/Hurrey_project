"""
Vector database operations and management.
"""
import os
import streamlit as st
from langchain_chroma import Chroma
import shutil

def get_vectorstore_path(session_id="default"):
    """
    Get the path for the vector store based on session ID.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Path string for the vector store
    """
    base_path = os.path.join("./chroma_stores", session_id)
    return base_path

def load_or_create_vectorstore(embeddings, documents=None, session_id="default"):
    """
    Load an existing vector store or create a new one with the provided documents.
    
    Args:
        embeddings: Embedding model to use
        documents: List of document chunks to add to the vector store (optional)
        session_id: Session identifier to persist session-specific vector stores
        
    Returns:
        Chroma vector store object or None if operation fails
    """
    # Ensure the parent directory exists
    os.makedirs("./chroma_stores", exist_ok=True)
    
    vectorstore_path = get_vectorstore_path(session_id)
    
    # If documents are provided, add them to the vector store
    if documents and len(documents) > 0:
        try:
            # Check if directory already exists - if so, add to existing store
            if os.path.exists(vectorstore_path):
                vectorstore = Chroma(
                    embedding_function=embeddings,
                    persist_directory=vectorstore_path
                )
                
                # Add documents to vectorstore
                vectorstore.add_documents(documents)
                st.success(f"Added {len(documents)} document chunks to the existing vector database.")
            else:
                # Create new vectorstore 
                # Note: Using from_documents with persist_directory will handle persistence automatically
                vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=embeddings,
                    persist_directory=vectorstore_path
                )
                st.success(f"Created new vector database with {len(documents)} document chunks.")
            
            # Try to persist if the method exists (for backward compatibility)
            try:
                # This might not be required for newer versions but we'll try it safely
                vectorstore.persist()
            except (AttributeError, Exception) as persist_error:
                # If persist fails, it's likely because newer versions handle it automatically
                # Just log it for debugging but don't treat it as an error
                print(f"Note: Manual persistence not required: {str(persist_error)}")
                
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
                st.warning("No documents found in vectorstore. Please upload files.")
                return None
                
            return vectorstore
        except FileNotFoundError:
            st.warning("Vector database not found. Please upload files to initialize.")
            return None
        except Exception as e:
            st.error(f"Failed to load vectorstore: {str(e)}")
            st.info("The vector database might be corrupted. Try uploading files again.")
            return None

def list_available_sessions():
    """
    List all available sessions with vector stores.
    
    Returns:
        List of session IDs
    """
    try:
        if not os.path.exists("./chroma_stores"):
            return []
        
        sessions = [d for d in os.listdir("./chroma_stores") 
                    if os.path.isdir(os.path.join("./chroma_stores", d))]
        return sessions
    except Exception as e:
        st.error(f"Failed to list available sessions: {str(e)}")
        return []

def delete_session_vectorstore(session_id):
    """
    Delete a session's vector store.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Boolean indicating success
    """
    try:
        vectorstore_path = get_vectorstore_path(session_id)
        if os.path.exists(vectorstore_path):
            shutil.rmtree(vectorstore_path)
            return True
        return False
    except Exception as e:
        st.error(f"Failed to delete vector store for session {session_id}: {str(e)}")
        return False
