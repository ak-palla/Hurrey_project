# Individualized Chatbot with RAG Personalization

A Streamlit application that allows users to upload PDF documents and chat with their content using Retrieval Augmented Generation (RAG). The chatbot provides personalized responses based on user-defined communication preferences.

## Features

- **Document Upload & Processing**: Upload and process PDF files to create a knowledge base
- **Personalized Responses**: Customize the chatbot's tone, style, length, and other communication parameters
- **Conversation History**: Track and maintain chat history for context-aware responses
- **Session Management**: Support for multiple independent chat sessions
- **Error Handling**: Robust error handling and user feedback throughout the application

## Personalization Options

The chatbot can be customized with the following parameters:

- **Tone**: Formal, Friendly, Humorous, Professional, Empathetic
- **Communication Goal**: Educate, Summarize, Advise, Entertain, Explain
- **Response Length**: Very Short, Short, Medium, Detailed, Comprehensive
- **Response Style**: Straightforward, Storytelling, Bullet Points, Step-by-Step, Analytical
- **Language**: English, Spanish, French, German, Chinese, Japanese
- **User Persona**: Beginner, Intermediate, Expert, Academic, Professional, Student

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Groq API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rag-personalization-chatbot.git
   cd rag-personalization-chatbot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory with your API keys:
   ```
   OPENAI_API_KEY=your-openai-api-key
   GROQ_API_KEY=your-groq-api-key
   ```

### Running the Application

Start the Streamlit server:
```
streamlit run app.py
```

The application will be available at `http://localhost:8501` in your web browser.

## Usage

1. Enter a session ID (or use the default)
2. Upload one or more PDF files
3. Use the sidebar to set your personalization preferences
4. Ask questions about the content of your uploaded documents
5. View the chat history in the expandable section

## Project Structure

```
├── app.py                  # Main application entry point
├── chains/                 # RAG chain components
│   ├── __init__.py
│   ├── rag_chain.py        # Conversational RAG chain setup
│   └── retriever.py        # History-aware retriever
├── components/             # UI components
│   ├── __init__.py
│   ├── chat_interface.py   # Chat display components
│   ├── settings_display.py # Personalization display
│   └── sidebar.py          # Sidebar UI for settings
├── models/                 # Model initialization
│   ├── __init__.py
│   ├── embeddings.py       # OpenAI embeddings setup
│   ├── llm.py              # Groq LLM setup
│   └── vectorstore.py      # Chroma vector database
└── utils/                  # Utility functions
    ├── __init__.py
    ├── file_handler.py     # PDF processing
    └── session_manager.py  # Chat history management
```

## Technical Implementation

- **LLM**: Uses Groq's Gemma2-9b-It model for generating responses
- **Embeddings**: OpenAI embeddings for document vectorization
- **Vector Database**: ChromaDB for storing and retrieving document vectors
- **RAG Implementation**: LangChain for creating the RAG pipeline
- **Frontend**: Streamlit for the user interface

## Limitations

- Currently only supports PDF file format
- Response quality depends on the underlying LLM model
- Vector database is stored locally and not persisted between sessions

## Future Improvements

- Support for additional file formats (DOCX, TXT, etc.)
- User authentication and cloud-based vector database
- Advanced document analysis and metadata extraction
- Improved error handling and recovery mechanisms
- Performance optimizations for large document collections


## Acknowledgements

- [LangChain](https://www.langchain.com/) for the RAG framework
- [Streamlit](https://streamlit.io/) for the web interface
- [OpenAI](https://openai.com/) for embeddings
- [Groq](https://groq.com/) for LLM access
- [ChromaDB](https://www.trychroma.com/) for vector storage
