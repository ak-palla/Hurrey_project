"""
Utilities for handling file uploads and processing.
"""
import os
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_uploaded_files(uploaded_files):
    """
    Process uploaded PDF files and convert them to document chunks.
    
    Args:
        uploaded_files: List of uploaded file objects from st.file_uploader
        
    Returns:
        List of document chunks or empty list if no valid documents
    """
    if not uploaded_files:
        return []
    
    documents = []
    temp_files = []
    
    with st.spinner("Processing uploaded files..."):
        for uploaded_file in uploaded_files:
            try:
                # Create a proper temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name
                    temp_files.append(temp_path)
                
                # Load the PDF with error handling
                try:
                    loader = PyPDFLoader(temp_path)
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    st.error(f"Error processing file '{uploaded_file.name}': {str(e)}")
                    continue
            except Exception as upload_error:
                st.error(f"Failed to process file '{uploaded_file.name}': {str(upload_error)}")
    
    # Clean up temporary files
    for temp_path in temp_files:
        try:
            os.unlink(temp_path)
        except Exception:
            pass  # Silently continue if temp file deletion fails
    
    if not documents:
        st.error("No valid documents were successfully processed. Please check your PDF files.")
        return []
    
    st.success(f"Successfully processed {len(documents)} document sections from {len(uploaded_files)} files.")
    
    # Split documents with error handling
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
        st.success(f"Created {len(splits)} document chunks for processing.")
        return splits
    except Exception as split_error:
        st.error(f"Failed to split documents: {str(split_error)}")
        return []
