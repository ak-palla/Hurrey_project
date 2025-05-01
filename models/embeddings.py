"""
Embeddings model initialization and configuration.
"""
import os
import streamlit as st
from langchain_openai import OpenAIEmbeddings

def initialize_embeddings():
    """
    Initialize the OpenAI embeddings model with API key validation.
    
    Returns:
        OpenAIEmbeddings object or None if initialization fails
    """
    # Get API key from environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Validate API key
    if not openai_api_key:
        st.error("OPENAI_API_KEY not found in environment variables. Please add it to your .env file.")
        return None
    elif not openai_api_key.startswith("sk-"):  # Basic format validation for OpenAI keys
        st.error("OPENAI_API_KEY appears to be in the wrong format. OpenAI keys typically start with 'sk-'.")
        return None
    
    # Initialize embeddings with error handling
    try:
        embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        return embeddings
    except Exception as e:
        st.error(f"Failed to initialize OpenAI embeddings: {str(e)}")
        st.info("This could be due to an invalid API key or network connectivity issues.")
        return None
