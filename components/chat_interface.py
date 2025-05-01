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
    # First print debug information
    print(f"Displaying chat history with {len(chat_history.messages)} messages")
    
    # Display messages directly without an expander
    if not chat_history.messages:
        st.info("No conversation history yet.")
        return
    
    # Display each message with proper formatting
    for i, msg in enumerate(chat_history.messages):
        role = "User" if msg.type == "human" else "Assistant"
        st.markdown(f"**Message {i+1} - {role}:** {msg.content}")
        st.divider()

def display_chat_history_in_tab(chat_history: BaseChatMessageHistory, tab):
    """
    Display the chat history within a specified tab.
    
    Args:
        chat_history: ChatMessageHistory object containing messages
        tab: Streamlit tab to render within
    """
    # Print debug information
    print(f"Displaying chat history in tab with {len(chat_history.messages)} messages")
    
    if not chat_history.messages:
        tab.info("No conversation history yet.")
    else:
        # Add a refresh button to update the history display
        if tab.button("Refresh History", key="refresh_history_tab"):
            st.rerun()
            
        # Display each message with proper formatting
        for i, msg in enumerate(chat_history.messages):
            role = "User" if msg.type == "human" else "Assistant"
            tab.markdown(f"**Message {i+1} - {role}:** {msg.content}")
            tab.divider()

def display_chat_input():
    """
    Display the chat input box and return the user's input.
    
    Returns:
        User input string or None if no input
    """
    return st.text_input("Your question:")

def display_assistant_response(response, chat_history=None, session_id=None):
    """
    Display the assistant's response and optionally add it to chat history.
    
    Args:
        response: Response text from the assistant
        chat_history: Optional ChatMessageHistory object to update
        session_id: Optional session ID for logging
    """
    # Display the response
    st.markdown(f"**Assistant:** {response}")
    
    # Add to chat history if provided
    if chat_history is not None:
        print(f"Adding assistant response to chat history for session {session_id}")
        chat_history.add_ai_message(response)
        print(f"Chat history now has {len(chat_history.messages)} messages")
