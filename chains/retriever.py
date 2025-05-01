"""
Retriever configuration and setup.
"""
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever

def create_history_aware_retriever_chain(llm, vectorstore):
    """
    Create a history-aware retriever that reformulates questions based on chat history.
    
    Args:
        llm: Language model to use for question reformulation
        vectorstore: Vector store to use as the base retriever
        
    Returns:
        History-aware retriever or None if creation fails
    """
    try:
        # Get base retriever
        retriever = vectorstore.as_retriever()
        
        # History-aware prompt for question reformulation
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        
        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )
        
        return history_aware_retriever
    except Exception as e:
        st.error(f"Failed to create history-aware retriever: {str(e)}")
        return None
