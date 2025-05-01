"""
Retriever configuration and setup.
Updated for compatibility with the latest LangChain versions.
"""
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.chains.conversational_retrieval.base import _get_chat_history

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
        
        # Create a simple chain to reformulate the question based on chat history
        contextualize_question_chain = contextualize_q_prompt | llm | StrOutputParser()
        
        # Define a wrapper function for the retriever that uses the question chain
        def get_context_and_question(input_dict):
            # Preserve all personalization variables
            result = input_dict.copy()
            
            # Convert the chat history to a format expected by LangChain
            if "chat_history" in input_dict and input_dict["chat_history"]:
                chat_history_str = _get_chat_history(input_dict["chat_history"])
            else:
                chat_history_str = ""
            
            # Reformulate the question based on chat history
            reformulated_question = contextualize_question_chain.invoke({
                "input": input_dict["input"],
                "chat_history": input_dict.get("chat_history", [])
            })
            
            # Log for debugging
            st.session_state['last_reformulated_question'] = reformulated_question
            
            # Use the reformulated question for retrieval
            context = retriever.get_relevant_documents(reformulated_question)
            
            # Store retrieved documents in session state for display
            if 'retrieved_documents' not in st.session_state:
                st.session_state['retrieved_documents'] = []
            st.session_state['retrieved_documents'] = context
            
            # Update result with context and question
            result["context"] = context
            result["question"] = input_dict["input"]
            
            return result
        
        # Create a RunnableLambda for the retriever function
        retriever_chain = RunnableLambda(get_context_and_question)
        
        return retriever_chain
    except Exception as e:
        st.error(f"Failed to create history-aware retriever: {str(e)}")
        
        # Create a simpler fallback retriever if the advanced one fails
        try:
            # Get base retriever
            simple_retriever = vectorstore.as_retriever()
            
            # Create a simple wrapper that just returns the documents
            def simple_retrieval(input_dict):
                # Preserve all personalization variables
                result = input_dict.copy()
                
                question = input_dict["input"]
                documents = simple_retriever.get_relevant_documents(question)
                
                # Store for display
                if 'retrieved_documents' not in st.session_state:
                    st.session_state['retrieved_documents'] = []
                st.session_state['retrieved_documents'] = documents
                
                # Add context and question to the result
                result["context"] = documents
                result["question"] = question
                
                return result
            
            # Create a RunnableLambda for the simple retriever
            simple_retriever_chain = RunnableLambda(simple_retrieval)
            
            st.warning("Using simplified retriever without chat history awareness")
            return simple_retriever_chain
        except Exception as fallback_error:
            st.error(f"Failed to create even simple retriever: {str(fallback_error)}")
            return None
