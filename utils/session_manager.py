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
        print("Session state initialized")

def get_session_history(session: str) -> BaseChatMessageHistory:
    """
    Get or create a chat message history for a specific session.
    
    Args:
        session: Session identifier
        
    Returns:
        ChatMessageHistory object for the specified session
    """
    if 'store' not in st.session_state:
        st.session_state.store = {}
        print(f"Created new store for {session}")
    
    if session not in st.session_state.store:
        st.session_state.store[session] = ChatMessageHistory()
        print(f"Created new chat history for session: {session}")
    
    # Debug print
    history = st.session_state.store[session]
    print(f"Current history for session {session} has {len(history.messages)} messages")
    
    return history

def clear_session_history(session: str = None):
    """
    Clear chat history for a specific session or all sessions.
    
    Args:
        session: Session identifier. If None, clears all session histories.
    """
    if session is None:
        st.session_state.store = {}
        print("Cleared ALL session histories")
    elif session in st.session_state.store:
        st.session_state.store[session] = ChatMessageHistory()
        print(f"Cleared chat history for session: {session}")
    else:
        print(f"No history found for session: {session} - nothing to clear")

def print_all_session_histories():
    """
    Debugging function to print all session histories.
    """
    print("\n--- DEBUGGING: ALL SESSION HISTORIES ---")
    if 'store' not in st.session_state:
        print("No store found in session state!")
        return
    
    if not st.session_state.store:
        print("Session store exists but is empty!")
        return
    
    for session_id, history in st.session_state.store.items():
        print(f"Session: {session_id} - {len(history.messages)} messages")
        for i, msg in enumerate(history.messages):
            print(f"  Message {i+1}: {msg.type} - {msg.content[:30]}...")
    
    print("--- END DEBUGGING ---\n")
