"""
LLM model initialization and configuration.
"""
import os
import streamlit as st
from langchain_groq import ChatGroq

def initialize_llm():
    """
    Initialize the Groq LLM with API key validation.
    
    Returns:
        ChatGroq object or None if initialization fails
    """
    # Get API key from environment variable
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    # Validate API key
    if not groq_api_key:
        st.error("GROQ_API_KEY not found in environment variables. Please add it to your .env file.")
        return None
    elif len(groq_api_key.strip()) < 10:  # Simple validation to ensure key isn't empty or malformed
        st.error("GROQ_API_KEY appears to be invalid. Please check your .env file for the correct key.")
        return None
    
    # Initialize LLM with error handling
    try:
        llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")
        return llm
    except Exception as e:
        st.error(f"Failed to initialize the Groq LLM: {str(e)}")
        st.info("This may be due to an invalid API key, network issues, or the model being unavailable.")
        return None
