"""
RAG chain setup and configuration.
"""
import streamlit as st
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from chains.retriever import create_history_aware_retriever_chain

def create_conversational_rag_chain(llm, vectorstore, get_session_history_fn):
    """
    Create a conversational RAG chain with message history support.
    
    Args:
        llm: Language model to use for chain
        vectorstore: Vector store for retrieval
        get_session_history_fn: Function to get session-specific chat history
        
    Returns:
        Conversational RAG chain or None if creation fails
    """
    try:
        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever_chain(llm, vectorstore)
        if history_aware_retriever is None:
            return None
        
        # Personalized QA Prompt with system prompt
        system_prompt = (
            "You are an assistant with a {tone} tone. Your goal is to {goal}. "
            "Provide {length} responses in a {style} format. "
            "The user is a {persona} level individual. "
            "Respond in {language}. "
            "Use the following pieces of retrieved context to answer "
            "the question: \n\n{context}"
        )
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        
        # Create the QA chain
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        
        # Create the base RAG chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        
        # Create conversational chain with message history
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history_fn,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
        
        return conversational_rag_chain
    except Exception as e:
        st.error(f"Failed to create conversational RAG chain: {str(e)}")
        return None
