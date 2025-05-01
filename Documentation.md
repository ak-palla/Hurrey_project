# Individualized Chatbot with RAG Personalization: Technical Overview

## Personalization System

The chatbot implements a multi-dimensional personalization system that dynamically adapts responses based on user preferences. This system works through several interconnected components:

### 1. Personalization Parameters

The chatbot captures six key personalization dimensions:

- **Tone**: Controls the emotional quality and formality level (Formal, Friendly, Humorous, Professional, Empathetic)
- **Goal**: Defines the purpose of the response (Educate, Summarize, Advise, Entertain, Explain)
- **Length**: Determines the verbosity of responses (Very Short, Short, Medium, Detailed, Comprehensive)
- **Style**: Specifies the structural format (Straightforward, Storytelling, Bullet Points, Step-by-Step, Analytical)
- **Language**: Sets the output language (English, Spanish, French, German, Chinese, Japanese)
- **Persona**: Adjusts the complexity level based on user expertise (Beginner, Intermediate, Expert, Academic, Professional, Student)

### 2. Dynamic Persona Management

Beyond basic personalization, the system implements a sophisticated persona management framework:

- **Persistent Personas**: Users can save their current personalization settings as named personas for future use
- **Persona Switching**: Seamlessly switch between different personas during a conversation
- **Mood Overrides**: Temporarily modify the tone based on specific moods (serious, motivational, sarcastic, excited, analytical)

### 3. Technical Implementation

The personalization system is implemented through:

```python
# System prompt template with personalization parameters
system_prompt = (
    "You are an assistant with a {tone} tone. Your goal is to {goal}. "
    "Provide {length} responses in a {style} format. "
    "The user is a {persona} level individual. "
    "Respond in {language}. "
    "Use the following pieces of retrieved context to answer "
    "the question: \n\n{context}"
)
```

This template is populated with the user's personalization parameters and combined with retrieved context to create fully customized responses. The implementation ensures all parameters are properly mapped and validated before being integrated into the prompt.

## Document Retrieval and RAG Implementation

The chatbot employs a sophisticated Retrieval-Augmented Generation (RAG) pipeline to enhance responses with information from user-uploaded documents.

### 1. Document Processing Pipeline

The document handling workflow consists of:

1. **Upload and Parsing**: Users can upload multiple document formats (PDF, TXT, DOCX, CSV)
2. **Metadata Extraction**: The system extracts and stores metadata (pages, paragraphs, authors, etc.)
3. **Chunking**: Documents are split into smaller, semantically coherent chunks using recursive character splitting
4. **Embedding**: Chunks are converted into vector embeddings using OpenAI's embedding model
5. **Storage**: Embeddings are stored in a Chroma vector database with session persistence

### 2. Context-Aware Retrieval

The retrieval system implements advanced techniques:

- **History-Aware Retrieval**: Questions are reformulated based on chat history to maintain context
- **Query Reformulation**: The system transforms ambiguous or referential questions into standalone queries
- **Relevance Retrieval**: The most semantically similar document chunks are retrieved for each query
- **Context Integration**: Retrieved chunks are integrated into the prompt template alongside personalization parameters

### 3. Technical Implementation

The RAG pipeline is implemented with LangChain components:

```python
# Create history-aware retriever
retriever_chain = create_history_aware_retriever_chain(llm, vectorstore)

# Create personalized QA chain with system prompt
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}")
])

# Create the complete RAG chain
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = preprocessing | retriever_chain | question_answer_chain
```

For transparency, the system displays retrieved document chunks, showing users which information sources contributed to each response.

## Setting Up and Running the Chatbot

### Prerequisites

- Python 3.10 or higher
- OpenAI API key (for embeddings)
- Groq API key (for LLM access)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/individualized-chatbot-rag.git
   cd individualized-chatbot-rag
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
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Access the interface**:
   Open your browser and navigate to `http://localhost:8501`

### Using the Chatbot

1. **Personalization**:
   - Use the sidebar to select your preferred tone, goal, length, style, language, and persona level
   - Save frequently used configurations as personas through the Persona Management menu
   - Apply mood overrides to temporarily modify tone

2. **Document Upload**:
   - Upload documents through the file uploader (supports PDF, TXT, DOCX, CSV)
   - View document analysis insights through the expandable dashboard
   - Documents are automatically processed and made available for retrieval

3. **Conversation**:
   - Enter questions in the chat input field
   - View responses with the applied personalization settings
   - Examine retrieved context for transparency into information sources
   - Switch between saved sessions or create new ones

4. **Session Management**:
   - Create multiple chat sessions with different documents
   - Switch between sessions through the Saved Sessions expander
   - Clear chat history when needed

By following these steps, you'll have a fully functional personalized RAG chatbot running locally with customizable settings and document integration capabilities.
