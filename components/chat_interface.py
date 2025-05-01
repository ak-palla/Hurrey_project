"""
Component for displaying chat history and interface.
"""
import streamlit as st
from langchain_core.chat_history import BaseChatMessageHistory

def display_chat_history(chat_history: BaseChatMessageHistory):
    """
    Display the chat history directly in a container.
    
    Args:
        chat_history: ChatMessageHistory object containing messages
    """
    # Display messages directly without an expander
    for msg in chat_history.messages:
        role = "User" if msg.type == "human" else "Assistant"
        st.markdown(f"**{role}:** {msg.content}")
        st.divider()

def display_chat_history_in_tab(chat_history: BaseChatMessageHistory, tab):
    """
    Display the chat history within a specified tab.
    
    Args:
        chat_history: ChatMessageHistory object containing messages
        tab: Streamlit tab to render within
    """
    if not chat_history.messages:
        tab.info("No conversation history yet.")
    else:
        for msg in chat_history.messages:
            role = "User" if msg.type == "human" else "Assistant"
            tab.markdown(f"**{role}:** {msg.content}")
            tab.divider()

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
