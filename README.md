# Individualized Chatbot with RAG Personalization

A sophisticated chatbot that dynamically adapts its responses based on user-defined parameters and augments answers using user-uploaded documents via a Retrieval-Augmented Generation (RAG) mechanism.

## Core Features

- **Personalized Responses**: Customize how the chatbot responds through multiple dimensions:
  - **Tone**: Formal, Friendly, Humorous, Professional, Empathetic
  - **Goal**: Educate, Summarize, Advise, Entertain, Explain
  - **Length**: Very Short, Short, Medium, Detailed, Comprehensive
  - **Style**: Straightforward, Storytelling, Bullet Points, Step-by-Step, Analytical
  - **Language**: English, Spanish, French, German, Chinese, Japanese
  - **Persona**: Beginner, Intermediate, Expert, Academic, Professional, Student

- **Document Integration**: Upload files in various formats (PDF, TXT, DOCX, CSV) to provide context for the chatbot.

- **Persona Management**: Save, load, and switch between different personas during conversations.

- **Mood Overrides**: Temporarily modify the tone based on specific moods.

- **Document Analysis**: Visualize metadata and content insights from uploaded documents.

- **Session Management**: Create and switch between multiple named conversation sessions.

## Technical Architecture

- **RAG Implementation**: Uses LangChain's retrieval and generation components to integrate document knowledge.

- **Vectorization**: Converts document chunks into embeddings stored in a Chroma vector database.

- **Context-Aware Retrieval**: Questions are reformulated based on chat history to maintain context.

- **Modular Design**: Clean separation of components for UI, document processing, and chat functionality.

## Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key (for embeddings)
- Groq API key (for LLM access)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ak-palla/Hurrey_project
   cd Hurrey_project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   VECTOR_STORE_DIR=./chroma_stores
   USER_DATA_DIR=./user_data
   LOG_LEVEL=INFO
   MAX_TOKENS=1024
   EMBEDDING_MODEL=text-embedding-ada-002
   LLM_MODEL=Gemma2-9b-It
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Access the interface**:
   Open your browser and navigate to `http://localhost:8501`

## Usage Guide

### Personalizing Responses

1. Use the sidebar to select your preferred tone, goal, length, style, language, and expertise level.
2. Save frequently used configurations as personas through the Persona Management menu.
3. Apply mood overrides to temporarily modify tone for specific interactions.

### Document Upload and Processing

1. Upload documents through the file uploader (supports PDF, TXT, DOCX, CSV).
2. Explore document metadata and content insights through the Document Analysis Dashboard.
3. View which document chunks influenced each response in the "View Retrieved Context" section.

### Multi-Session Support

1. Create new sessions by entering a unique Session ID.
2. Switch between saved sessions to maintain separate conversations.
3. Clear chat history when needed to start fresh.

## Project Structure

The project follows a modular design with clear separation of concerns:

- `app.py`: Main application entry point
- `chains/`: LangChain configuration for RAG and retrieval
- `components/`: UI components and interfaces
- `models/`: Model initialization for embeddings, LLM, and vector storage
- `utils/`: Utility functions for file handling, session management, and user authentication

## Extending the Project

### Adding New Document Types

1. Update `utils/file_handler.py` with a new document loader
2. Add the file extension to the accepted types in `app.py`

### Implementing New Personalization Dimensions

1. Add the new dimension to the sidebar UI in `components/sidebar.py`
2. Update the system prompt template in `chains/rag_chain.py`

## Troubleshooting

- **API Key Issues**: Verify your API keys in the `.env` file
- **Document Processing Errors**: Check file permissions and formats
- **Vector Store Not Found**: Upload documents before asking questions
- **Session State Errors**: Ensure unique keys for widgets and session state variables

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for the RAG framework
- [Streamlit](https://streamlit.io/) for the web interface
- [Groq](https://groq.com/) for the LLM API
- [OpenAI](https://openai.com/) for embeddings
