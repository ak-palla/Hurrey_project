"""
Utilities for handling session state and chat history.
"""
import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

def initialize_session_state():
    """
    Initialize session state variables for the application.
    This ensures only the current session's chat history is maintained.
    """
    if 'app_initialized' not in st.session_state:
        st.session_state.store = {}
        st.session_state.app_initialized = True

def get_session_history(session: str) -> BaseChatMessageHistory:
    """
    Get or create a chat message history for a specific session.
    
    Args:
        session: Session identifier
        
    Returns:
        ChatMessageHistory object for the specified session
    """
    if session not in st.session_state.store:
        st.session_state.store[session] = ChatMessageHistory()
    return st.session_state.store[session]

def clear_session_history(session: str = None):
    """
    Clear chat history for a specific session or all sessions.
    
    Args:
        session: Session identifier. If None, clears all session histories.
    """
    if session is None:
        st.session_state.store = {}
    elif session in st.session_state.store:
        st.session_state.store[session] = ChatMessageHistory()
