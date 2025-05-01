# Individualized Chatbot with RAG Personalization

A personalized chatbot that dynamically adapts its responses based on user-defined parameters and augments answers using user-uploaded documents via a Retrieval-Augmented Generation (RAG) mechanism.

## Features

- **Personalized Responses**: Customize tone, goal, length, style, language, and user persona level
- **Document Integration**: Upload PDFs, TXT, DOCX, and CSV files for context-enhanced answers
- **Persona Management**: Save, load, and switch between different personas
- **Mood Overrides**: Temporarily change tone based on specific moods
- **Document Analysis**: Visualize metadata and content insights from uploaded documents
- **User Authentication**: Save preferences across sessions and manage multiple chat histories
- **Multi-Session Support**: Create and switch between named conversation sessions


## Installation

### Prerequisites

- Python 3.10 or higher
- [Pip](https://pip.pypa.io/en/stable/installation/)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/individualized-chatbot-rag.git
   cd individualized-chatbot-rag
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Use the sidebar to customize your personalization settings

4. Upload documents using the file uploader

5. Start chatting with the personalized RAG assistant

## Personalization Options

| Parameter | Description | Options |
|-----------|-------------|---------|
| Tone | How the chatbot communicates | Formal, Friendly, Humorous, Professional, Empathetic |
| Goal | Purpose of the response | Educate, Summarize, Advise, Entertain, Explain |
| Length | Detail level of responses | Very Short, Short, Medium, Detailed, Comprehensive |
| Style | Format of the response | Straightforward, Storytelling, Bullet Points, Step-by-Step, Analytical |
| Language | Response language | English, Spanish, French, German, Chinese, Japanese |
| Persona | User expertise level | Beginner, Intermediate, Expert, Academic, Professional, Student |

## Persona Management

- **Save Persona**: Save current settings as a named persona
- **Load Persona**: Switch between saved personas
- **Mood Override**: Temporarily change tone based on mood (serious, motivational, sarcastic, etc.)

## Document Support

The application supports uploading the following document types:
- PDF (.pdf)
- Text (.txt)
- Word Documents (.docx)
- CSV Files (.csv)

## Advanced Features

### Document Analysis Dashboard

Access the document analysis dashboard to:
- View document metadata (file types, pages, etc.)
- Explore content statistics (word frequency, distribution)
- Visualize content distribution by source

### Context Transparency

View the retrieved context for any response to understand:
- Which document chunks influenced the answer
- How questions are reformulated based on chat history
- Source attribution for information

## Project Structure

```
individualized-chatbot-rag/
├── app.py                  # Main application file
├── chains/                 # LangChain configuration
│   ├── __init__.py
│   ├── rag_chain.py        # RAG chain setup
│   └── retriever.py        # Retrieval configuration
├── components/             # UI components
│   ├── __init__.py
│   ├── chat_interface.py   # Chat display
│   ├── document_analysis.py# Document insights
│   ├── dynamic_persona.py  # Persona management
│   ├── settings_display.py # Settings visualization
│   └── sidebar.py          # Personalization controls
├── models/                 # Model initialization
│   ├── __init__.py
│   ├── embeddings.py       # Embedding setup
│   ├── llm.py              # LLM configuration
│   └── vectorstore.py      # Vector database operations
└── utils/                  # Utility functions
    ├── __init__.py
    ├── file_handler.py     # Document processing
    ├── session_manager.py  # Chat history management
    └── user_auth.py        # User authentication
```

## Troubleshooting

### Common Issues

**Error: API key not found**
- Ensure your `.env` file contains valid API keys
- Check if the environment variables are being loaded correctly

**Error: Session state modification**
- This can occur if you try to modify Streamlit session state variables after widgets with the same keys are instantiated
- Ensure unique keys are used for widgets and session state variables

**Error: Vector store not found**
- Upload documents before asking questions
- Check if the Chroma directory has proper permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for the RAG framework
- [Streamlit](https://streamlit.io/) for the web interface
- [Groq](https://groq.com/) for the LLM API
- [OpenAI](https://openai.com/) for embeddings
