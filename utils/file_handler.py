"""
Utilities for handling file uploads and processing.
"""
import os
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_core.documents import Document

def extract_metadata(file_obj, file_path, file_type):
    """
    Extract metadata from uploaded files.
    
    Args:
        file_obj: Original uploaded file object
        file_path: Path to the temporary saved file
        file_type: Type of the file (pdf, txt, docx, csv)
        
    Returns:
        Dictionary containing metadata
    """
    metadata = {
        "filename": file_obj.name,
        "file_type": file_type,
        "file_size": file_obj.size,
        "created_at": None,  # Will be populated if available
    }
    
    # Extract file-specific metadata
    try:
        if file_type == "pdf":
            import PyPDF2
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                metadata["page_count"] = len(reader.pages)
                if reader.metadata:
                    metadata["author"] = reader.metadata.author
                    metadata["created_at"] = reader.metadata.creation_date
                    metadata["modified_at"] = reader.metadata.modification_date
        elif file_type == "docx":
            import docx
            doc = docx.Document(file_path)
            metadata["paragraph_count"] = len(doc.paragraphs)
            try:
                metadata["properties"] = {
                    "author": doc.core_properties.author,
                    "created": doc.core_properties.created,
                    "modified": doc.core_properties.modified
                }
            except:
                pass
        elif file_type == "csv":
            import pandas as pd
            df = pd.read_csv(file_path)
            metadata["row_count"] = len(df)
            metadata["column_count"] = len(df.columns)
            metadata["columns"] = list(df.columns)
    except Exception as e:
        st.warning(f"Could not extract all metadata from {file_obj.name}: {str(e)}")
    
    return metadata

def process_uploaded_files(uploaded_files):
    """
    Process uploaded files (PDF, TXT, DOCX, CSV) and convert them to document chunks.
    
    Args:
        uploaded_files: List of uploaded file objects from st.file_uploader
        
    Returns:
        List of document chunks or empty list if no valid documents
    """
    if not uploaded_files:
        return []
    
    documents = []
    temp_files = []
    metadata_summary = []
    
    with st.spinner("Processing uploaded files..."):
        for uploaded_file in uploaded_files:
            try:
                # Determine file type from name
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                file_type = file_extension[1:] if file_extension else "unknown"
                
                # Create a proper temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name
                    temp_files.append(temp_path)
                
                # Extract metadata
                metadata = extract_metadata(uploaded_file, temp_path, file_type)
                metadata_summary.append(metadata)
                
                # Store document metadata in session state
                if 'document_metadata' not in st.session_state:
                    st.session_state['document_metadata'] = {}
                st.session_state['document_metadata'][uploaded_file.name] = metadata
                
                # Load the file based on type with error handling
                try:
                    if file_type == "pdf":
                        loader = PyPDFLoader(temp_path)
                    elif file_type == "txt":
                        loader = TextLoader(temp_path)
                    elif file_type == "docx":
                        loader = UnstructuredWordDocumentLoader(temp_path)
                    elif file_type == "csv":
                        loader = CSVLoader(temp_path)
                    else:
                        # Fallback to unstructured loader for other types
                        try:
                            loader = UnstructuredFileLoader(temp_path)
                        except:
                            st.warning(f"File type '{file_type}' not directly supported. Trying generic loader.")
                            continue
                    
                    docs = loader.load()
                    
                    # Add file metadata to each document
                    for doc in docs:
                        doc.metadata.update({
                            "source_file": uploaded_file.name,
                            "file_type": file_type
                        })
                    
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
        st.error("No valid documents were successfully processed. Please check your files.")
        return []
    
    # Display metadata summary in expandable section
    if metadata_summary:
        with st.expander("Document Metadata Summary", expanded=False):
            for meta in metadata_summary:
                st.subheader(f"{meta['filename']} ({meta['file_type'].upper()})")
                meta_display = {k: v for k, v in meta.items() if k not in ['filename', 'file_type']}
                st.json(meta_display)
    
    st.success(f"Successfully processed {len(documents)} document sections from {len(uploaded_files)} files.")
    
    # Split documents with error handling
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
        st.success(f"Created {len(splits)} document chunks for processing.")
        
        # Store the original chunks in session state for display
        if 'document_chunks' not in st.session_state:
            st.session_state['document_chunks'] = []
        st.session_state['document_chunks'] = splits
        
        return splits
    except Exception as split_error:
        st.error(f"Failed to split documents: {str(split_error)}")
        return []
