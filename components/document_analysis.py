"""
Component for advanced document analysis and metadata extraction.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import re
from collections import Counter

# Import NLTK with proper error handling
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    
    # Download required NLTK data - correct resource names
    nltk_resources = ['punkt', 'stopwords']
    for resource in nltk_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource)
    
    nltk_available = True
except ImportError:
    nltk_available = False
    st.warning("NLTK library not available. Some document analysis features will be limited.")
except Exception as e:
    nltk_available = False
    st.warning(f"Error initializing NLTK: {str(e)}. Some document analysis features will be limited.")

def analyze_document_metadata(container):
    """
    Analyze metadata from documents and display insights.
    
    Args:
        container: Streamlit container to render content within
    """
    if 'document_metadata' not in st.session_state or not st.session_state['document_metadata']:
        container.info("No documents have been uploaded yet.")
        return
    
    metadata = st.session_state['document_metadata']
    
    container.subheader("Document Overview")
    
    # Count by file type
    file_types = [meta['file_type'] for meta in metadata.values()]
    file_type_counts = Counter(file_types)
    
    # Create a simple bar chart
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(file_type_counts.keys(), file_type_counts.values())
        ax.set_title('Document Types')
        ax.set_xlabel('File Type')
        ax.set_ylabel('Count')
        
        # Save the plot to a buffer
        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        
        # Display the image
        container.image(buf.getvalue())
    except Exception as plot_error:
        container.error(f"Error creating document type chart: {str(plot_error)}")
    
    # Display file metadata in a table
    container.subheader("Document Metadata")
    
    # Create a DataFrame for display
    meta_data = []
    for filename, meta in metadata.items():
        row = {
            'Filename': filename,
            'Type': meta.get('file_type', '').upper(),
            'Size (KB)': round(meta.get('file_size', 0) / 1024, 2)
        }
        
        # Add file-specific metadata
        if 'page_count' in meta:
            row['Pages'] = meta['page_count']
        if 'paragraph_count' in meta:
            row['Paragraphs'] = meta['paragraph_count']
        if 'row_count' in meta:
            row['Rows'] = meta['row_count']
        if 'column_count' in meta:
            row['Columns'] = meta['column_count']
        if 'author' in meta:
            row['Author'] = meta['author']
        
        meta_data.append(row)
    
    if meta_data:
        df = pd.DataFrame(meta_data)
        container.dataframe(df)
    else:
        container.info("No metadata available for display.")

def analyze_document_content(container):
    """
    Analyze the content of documents and display insights.
    
    Args:
        container: Streamlit container to render content within
    """
    if 'document_chunks' not in st.session_state or not st.session_state['document_chunks']:
        container.info("No documents have been processed yet.")
        return
    
    chunks = st.session_state['document_chunks']
    
    container.subheader("Text Analysis")
    
    # Combine all text
    all_text = " ".join([chunk.page_content for chunk in chunks])
    
    # Basic statistics using regex for word count (more reliable than NLTK dependency)
    word_count = len(re.findall(r'\b\w+\b', all_text))
    
    # For sentence count, use a simple approximation if NLTK is not available
    if nltk_available:
        try:
            sentence_count = len(sent_tokenize(all_text))
        except Exception:
            # Fallback to simple period counting if NLTK fails
            sentence_count = len(re.findall(r'[.!?]+', all_text))
    else:
        # Simple approximation of sentences by counting periods, exclamation points, and question marks
        sentence_count = len(re.findall(r'[.!?]+', all_text))
    
    col1, col2, col3 = container.columns(3)
    col1.metric("Total Words", word_count)
    col2.metric("Total Sentences", sentence_count)
    col3.metric("Chunks", len(chunks))
    
    # Word frequency analysis
    if word_count > 0:
        container.subheader("Word Frequency Analysis")
        
        # Use NLTK if available, otherwise use regex
        if nltk_available:
            try:
                # Tokenize and process
                words = word_tokenize(all_text.lower())
                stop_words = set(stopwords.words('english'))
                filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
            except Exception as nltk_error:
                container.warning(f"Error using NLTK for word tokenization: {str(nltk_error)}")
                # Fallback to simple word extraction
                words = re.findall(r'\b[a-z]+\b', all_text.lower())
                # Simple stopwords
                stop_words = {'the', 'a', 'an', 'and', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'is', 'are'}
                filtered_words = [word for word in words if word not in stop_words]
        else:
            # Simple word extraction without NLTK
            words = re.findall(r'\b[a-z]+\b', all_text.lower())
            # Simple stopwords
            stop_words = {'the', 'a', 'an', 'and', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'is', 'are'}
            filtered_words = [word for word in words if word not in stop_words]
        
        # Get most common words
        word_freq = Counter(filtered_words).most_common(20)
        
        if word_freq:
            try:
                # Create bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                words, counts = zip(*word_freq)
                ax.barh(list(reversed(words)), list(reversed(counts)))
                ax.set_title('Top 20 Words')
                ax.set_xlabel('Frequency')
                
                # Save the plot to a buffer
                buf = BytesIO()
                plt.savefig(buf, format="png")
                plt.close(fig)
                
                # Display the image
                container.image(buf.getvalue())
            except Exception as plot_error:
                container.error(f"Error creating word frequency chart: {str(plot_error)}")
                # Display as text instead
                container.write("Top 20 words:")
                for word, count in word_freq:
                    container.write(f"- {word}: {count}")
        else:
            container.info("Could not extract word frequencies.")
    
    # Document source analysis
    container.subheader("Content by Source")
    
    # Group chunks by source
    sources = {}
    for chunk in chunks:
        source = chunk.metadata.get('source_file', 'Unknown')
        if source not in sources:
            sources[source] = []
        sources[source].append(chunk)
    
    # Create a pie chart of content distribution
    labels = list(sources.keys())
    sizes = [len(chunks) for chunks in sources.values()]
    
    if labels and sizes:
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title('Content Distribution by Source')
            
            # Save the plot to a buffer
            buf = BytesIO()
            plt.savefig(buf, format="png")
            plt.close(fig)
            
            # Display the image
            container.image(buf.getvalue())
        except Exception as plot_error:
            container.error(f"Error creating source distribution chart: {str(plot_error)}")
            # Display as text instead
            container.write("Content distribution by source:")
            for source, chunks_list in sources.items():
                percentage = (len(chunks_list) / len(chunks)) * 100
                container.write(f"- {source}: {len(chunks_list)} chunks ({percentage:.1f}%)")

def display_document_analysis():
    """
    Display comprehensive document analysis.
    """
    # Use a single expander for the entire dashboard
    with st.expander("Document Analysis Dashboard", expanded=False):
        st.write("This dashboard provides insights into your uploaded documents.")
        
        # Use tabs inside the expander instead of nested expanders
        tab1, tab2 = st.tabs(["Metadata Analysis", "Content Analysis"])
        
        with tab1:
            # Pass the tab container to the analysis functions
            analyze_document_metadata(tab1)
        
        with tab2:
            # Pass the tab container to the analysis functions
            analyze_document_content(tab2)
