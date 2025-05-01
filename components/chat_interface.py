"""
Component for displaying chat history and interface.
"""
import streamlit as st
from langchain_core.chat_history import BaseChatMessageHistory

def display_chat_history(chat_history: BaseChatMessageHistory):
    """
    Display the chat history in an expander.
    
    Args:
        chat_history: ChatMessageHistory object containing messages
    """
    with st.expander("Chat History", expanded=False):
        for msg in chat_history.messages:
            role = "User" if msg.type == "human" else "Assistant"
            st.markdown(f"**{role}:** {msg.content}")

def display_chat_input():
    """
    Display the chat input box and return the user's input.
    
    Returns:
        User input string or None if no input
    """
    return st.text_input("Your question:")

def display_assistant_response(response):
    """
    Display the assistant's response.
    
    Args:
        response: Response text from the assistant
    """
    st.markdown(f"**Assistant:** {response}")
