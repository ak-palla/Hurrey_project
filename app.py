"""
Main application file for the Conversational RAG Q&A Chatbot.
This file serves as the entry point for the Streamlit application.
"""
import streamlit as st
import traceback
from dotenv import load_dotenv

# Import modularized components
from utils.session_manager import get_session_history, initialize_session_state
from utils.file_handler import process_uploaded_files
from models.embeddings import initialize_embeddings
from models.llm import initialize_llm
from models.vectorstore import load_or_create_vectorstore
from chains.rag_chain import create_conversational_rag_chain
from components.sidebar import render_sidebar
from components.settings_display import display_settings
from components.chat_interface import display_chat_history

# Load environment variables
load_dotenv()

def main():
    """Main application function"""
    # Set up Streamlit UI
    st.title("Individualized Chatbot with RAG Personalization")
    st.write("Upload PDFs and chat with their content using your preferred style")
    
    # Initialize session state
    initialize_session_state()
    
    # Get personalization settings from sidebar
    personalization = render_sidebar()
    
    # Session ID input
    session_id = st.text_input("Session ID", value="default_session")
    
    # Initialize embedding model
    embeddings = initialize_embeddings()
    if embeddings is None:
        st.stop()
        
    # Initialize LLM
    llm = initialize_llm()
    if llm is None:
        st.stop()
    
    # Process uploaded files
    uploaded_files = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)
    documents = process_uploaded_files(uploaded_files)
        
    # Load or create vectorstore
    vectorstore = load_or_create_vectorstore(embeddings, documents)
    if vectorstore is None:
        st.stop()
    
    # Create the conversational RAG chain
    conversational_rag_chain = create_conversational_rag_chain(
        llm, 
        vectorstore, 
        get_session_history
    )
    if conversational_rag_chain is None:
        st.stop()
    
    # Display current personalization settings
    display_settings(personalization)
    
    # User question input
    user_input = st.text_input("Your question:")
    if user_input:
        # Show thinking spinner
        with st.spinner("Thinking..."):
            try:
                # Add personalization parameters to the input
                personalized_input = {
                    "input": user_input,
                    **{k: v.lower() for k, v in personalization.items()}
                }
                
                # Invoke chain with error handling
                response = conversational_rag_chain.invoke(
                    personalized_input,
                    config={"configurable": {"session_id": session_id}},
                )
                
                # Display response
                st.markdown(f"**Assistant:** {response['answer']}")
                
                # Display chat history
                display_chat_history(get_session_history(session_id))
                
            except Exception as response_error:
                st.error("An error occurred while processing your question:")
                st.error(str(response_error))
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())
                st.info("You may want to try a simpler question or check if your question is relevant to the uploaded documents.")

if __name__ == "__main__":
    main()
