"""
Main application file for the Conversational RAG Q&A Chatbot.
This file serves as the entry point for the Streamlit application.
"""
import streamlit as st
import traceback
from dotenv import load_dotenv
import os

# Import modularized components
from utils.session_manager import get_session_history, initialize_session_state, clear_session_history
from utils.file_handler import process_uploaded_files
from utils.user_auth import render_auth_ui, save_user_settings

from models.embeddings import initialize_embeddings
from models.llm import initialize_llm
from models.vectorstore import load_or_create_vectorstore, list_available_sessions, delete_session_vectorstore

from chains.rag_chain import create_conversational_rag_chain, display_retrieved_context
from chains.retriever import create_history_aware_retriever_chain

from components.sidebar import render_sidebar
from components.settings_display import display_settings
from components.chat_interface import display_chat_history
from components.dynamic_persona import render_persona_management
from components.document_analysis import display_document_analysis

# Load environment variables
load_dotenv()

def main():
    """Main application function"""
    # Set up Streamlit UI
    st.title("Individualized Chatbot with RAG Personalization")
    st.write("Upload files and chat with their content using your preferred style")
    
    # Initialize session state
    initialize_session_state()
    
    # Handle user authentication
    is_logged_in = render_auth_ui()
    
    # Get personalization settings from sidebar
    base_personalization = render_sidebar()
    
    # Get dynamic persona settings (if logged in)
    if is_logged_in:
        # Render persona management UI and get any overrides
        persona_overrides = render_persona_management()
        
        # Merge base settings with any persona/mood overrides
        personalization = {**base_personalization, **persona_overrides}
    else:
        personalization = base_personalization
    
    # Session ID management
    session_col1, session_col2 = st.columns([3, 1])
    
    with session_col1:
        default_session = st.session_state.current_user + "_default" if st.session_state.get('current_user') else "default_session"
        session_id = st.text_input("Session ID", value=default_session, key="session_id")
    
    with session_col2:
        if st.button("Clear Chat History"):
            clear_session_history(session_id)
            st.success(f"Chat history cleared for session {session_id}")
            st.rerun()
    
    # Initialize embedding model
    embeddings = initialize_embeddings()
    if embeddings is None:
        st.stop()
        
    # Initialize LLM
    llm = initialize_llm()
    if llm is None:
        st.stop()
    
    # Process uploaded files - now supporting multiple formats
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, TXT, DOCX, CSV)", 
        type=["pdf", "txt", "docx", "csv"],
        accept_multiple_files=True
    )
    documents = process_uploaded_files(uploaded_files)
    
    # Display document analysis if documents are uploaded
    if documents:
        display_document_analysis()
        
    # Load or create vectorstore with session persistence
    vectorstore = load_or_create_vectorstore(embeddings, documents, session_id)
    if vectorstore is None:
        st.stop()
    
    # Display available sessions for switching (if logged in)
    sessions_tab = None
    if is_logged_in:
        # Create sessions tab but don't populate it yet
        sessions_tab = st.expander("Saved Sessions", expanded=False)
    
    # Create the conversational RAG chain
    conversational_rag_chain = create_conversational_rag_chain(
        llm, 
        vectorstore, 
        get_session_history
    )
    if conversational_rag_chain is None:
        st.stop()
    
    # Now populate the sessions tab if it exists
    # This ensures it's not nested within any other UI elements
    if sessions_tab is not None:
        with sessions_tab:
            available_sessions = list_available_sessions()
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected_session = st.selectbox(
                    "Switch to saved session:",
                    options=[""] + available_sessions,
                    index=0
                )
                
            with col2:
                st.write("")
                st.write("")
                if selected_session and st.button("Switch Session"):
                    st.session_state.session_id = selected_session
                    # Save current settings before switching
                    save_user_settings()
                    st.success(f"Switched to session: {selected_session}")
                    st.rerun()
    
    # Display current personalization settings
    display_settings(personalization)
    
    # Create tabs for interaction and history
    interaction_tab, history_tab = st.tabs(["Chat", "History"])
    
    with interaction_tab:
        # User question input
        user_input = st.text_input("Your question:")
        
        # Process user input
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
                    
                    # Create a container for the response
                    response_container = st.container()
                    with response_container:
                        # Handle different response formats
                        # Some models return a string, others return a dict with 'answer' key
                        if isinstance(response, dict) and 'answer' in response:
                            answer_text = response['answer']
                        elif isinstance(response, str):
                            answer_text = response
                        else:
                            # Try to extract the response in other ways
                            try:
                                answer_text = str(response)
                            except:
                                answer_text = "Sorry, I couldn't generate a proper response."
                        
                        # Display response
                        st.markdown(f"**Assistant:** {answer_text}")
                        
                        # Display retrieved context (new feature) in a separate tab
                        context_tab = st.expander("View Retrieved Context", expanded=False)
                        with context_tab:
                            if 'retrieved_documents' in st.session_state and st.session_state['retrieved_documents']:
                                # Create a tab for each retrieved document
                                if len(st.session_state['retrieved_documents']) > 1:
                                    tabs = st.tabs([f"Source {i+1}" for i in range(len(st.session_state['retrieved_documents']))])
                                    
                                    for i, (tab, doc) in enumerate(zip(tabs, st.session_state['retrieved_documents'])):
                                        with tab:
                                            st.markdown(f"### {doc.metadata.get('source_file', 'Unknown source')}")
                                            if 'page' in doc.metadata:
                                                st.markdown(f"**Page:** {doc.metadata['page'] + 1}")  # Add 1 as pages are 0-indexed
                                            if 'chunk' in doc.metadata:
                                                st.markdown(f"**Chunk:** {doc.metadata['chunk']}")
                                            
                                            # Display the text content
                                            st.markdown("**Content:**")
                                            st.markdown(f"```\n{doc.page_content[:500]}{'...' if len(doc.page_content) > 500 else ''}\n```")
                                else:
                                    # Single document case
                                    doc = st.session_state['retrieved_documents'][0]
                                    st.markdown(f"### Source: {doc.metadata.get('source_file', 'Unknown source')}")
                                    if 'page' in doc.metadata:
                                        st.markdown(f"**Page:** {doc.metadata['page'] + 1}")  # Add 1 as pages are 0-indexed
                                    if 'chunk' in doc.metadata:
                                        st.markdown(f"**Chunk:** {doc.metadata['chunk']}")
                                    
                                    # Display the text content
                                    st.markdown("**Content:**")
                                    st.markdown(f"```\n{doc.page_content[:500]}{'...' if len(doc.page_content) > 500 else ''}\n```")
                            else:
                                st.info("No context was retrieved for this question.")
                    
                    # Save settings for logged-in users
                    if is_logged_in:
                        save_user_settings()
                    
                except Exception as response_error:
                    st.error("An error occurred while processing your question:")
                    st.error(str(response_error))
                    with st.expander("Error Details"):
                        st.code(traceback.format_exc())
                    st.info("You may want to try a simpler question or check if your question is relevant to the uploaded documents.")
    
    # Display chat history in the history tab to avoid nesting expanders
    with history_tab:
        if session_id in st.session_state.store:
            messages = get_session_history(session_id).messages
            if not messages:
                st.info("No conversation history yet.")
            else:
                for msg in messages:
                    role = "User" if msg.type == "human" else "Assistant"
                    st.markdown(f"**{role}:** {msg.content}")
                    st.divider()
        else:
            st.info("No conversation history for this session.")

if __name__ == "__main__":
    main()
