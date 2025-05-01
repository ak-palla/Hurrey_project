"""
RAG chain setup and configuration.
Updated for maximum compatibility with the latest LangChain versions.
"""
import streamlit as st
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from chains.retriever import create_history_aware_retriever_chain
from components.dynamic_persona import inject_dynamic_persona_instructions

def create_conversational_rag_chain(llm, vectorstore, get_session_history_fn):
    """
    Create a conversational RAG chain with message history support.
    
    Args:
        llm: Language model to use for chain
        vectorstore: Vector store for retrieval
        get_session_history_fn: Function to get session-specific chat history
        
    Returns:
        Conversational RAG chain or None if creation fails
    """
    try:
        # Create history-aware retriever
        retriever_chain = create_history_aware_retriever_chain(llm, vectorstore)
        if retriever_chain is None:
            raise ValueError("Failed to create retriever chain")
        
        # Personalized QA Prompt with system prompt
        system_prompt = (
            "You are an assistant with a {tone} tone. Your goal is to {goal}. "
            "Provide {length} responses in a {style} format. "
            "The user is a {persona} level individual. "
            "Respond in {language}. "
            "Use the following pieces of retrieved context to answer "
            "the question: \n\n{context}"
        )
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}")
        ])
        
        # Create the QA chain
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        
        # Map the personalization parameters
        def map_personalization_params(input_dict):
            # Make sure all expected variables are present in input_dict
            tone = input_dict.get("tone", "friendly").lower()
            goal = input_dict.get("goal", "educate").lower()
            length = input_dict.get("length", "medium").lower()
            style = input_dict.get("style", "straightforward").lower()
            language = input_dict.get("language", "english").lower()
            persona = input_dict.get("persona", "intermediate").lower()
            
            # Log the variables for debugging
            print(f"Personalization parameters: tone={tone}, goal={goal}, length={length}, style={style}, language={language}, persona={persona}")
            
            # Return the input dict with all parameters properly set
            return {
                "input": input_dict.get("input", ""),
                "tone": tone,
                "goal": goal,
                "length": length,
                "style": style,
                "language": language,
                "persona": persona,
                "chat_history": input_dict.get("chat_history", [])
            }
        
        # Add a preprocessing step to ensure all variables are available
        preprocessing = RunnableLambda(map_personalization_params)
        
        # Create a modern chain that uses the retriever and question-answer components
        rag_chain = preprocessing | retriever_chain | question_answer_chain
        
        # Create conversational chain with message history
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history_fn,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
        
        st.success("Successfully created RAG chain with history-aware retrieval")
        return conversational_rag_chain
    except Exception as e:
        st.error(f"Failed to create advanced conversational RAG chain: {str(e)}")
        st.info("Trying simplified RAG chain...")
        
        # Fallback to a simpler implementation
        try:
            # Get base retriever
            retriever = vectorstore.as_retriever()
            
            # Personalized QA Prompt with system prompt
            system_prompt = (
                "You are an assistant with a {tone} tone. Your goal is to {goal}. "
                "Provide {length} responses in a {style} format. "
                "The user is a {persona} level individual. "
                "Respond in {language}. "
                "Use the following pieces of retrieved context to answer "
                "the question: \n\n{context}"
            )
            
            qa_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])
            
            # Define mapping function to ensure all variables are passed through
            def map_inputs(input_dict):
                return {
                    "context": input_dict.get("context", []),
                    "input": input_dict.get("input", ""),
                    "tone": input_dict.get("tone", "friendly").lower(),
                    "goal": input_dict.get("goal", "educate").lower(),
                    "length": input_dict.get("length", "medium").lower(),
                    "style": input_dict.get("style", "straightforward").lower(),
                    "language": input_dict.get("language", "english").lower(),
                    "persona": input_dict.get("persona", "intermediate").lower(),
                    "chat_history": input_dict.get("chat_history", [])
                }
            
            # Ensure all variables are properly mapped
            input_mapper = RunnableLambda(map_inputs)
            
            # Create the QA chain - basic version
            question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
            
            # Create basic retrieval chain
            retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)
            
            # Create the complete chain with input mapping
            rag_chain = input_mapper | retrieval_chain
            
            # Create conversational chain with message history
            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                get_session_history_fn,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )
            
            st.success("Created simplified RAG chain (without advanced retrieval)")
            return conversational_rag_chain
            
        except Exception as fallback_error:
            st.error(f"Failed to create even simplified RAG chain: {str(fallback_error)}")
            st.warning("Will attempt to use language model directly without retrieval")
            
            # Fallback to just using the LLM directly as a last resort
            try:
                # Create a simple prompt template
                simple_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant. Answer the user's question to the best of your ability."),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}")
                ])
                
                # Create a simple chain
                simple_chain = simple_prompt | llm
                
                # Create conversational chain with message history
                conversational_chain = RunnableWithMessageHistory(
                    simple_chain,
                    get_session_history_fn,
                    input_messages_key="input",
                    history_messages_key="chat_history",
                    output_messages_key="answer"
                )
                
                st.warning("Using LLM without document retrieval as fallback")
                return conversational_chain
            except Exception as e:
                st.error(f"All fallback attempts failed: {str(e)}")
                return None

def display_retrieved_context():
    """
    Display the documents retrieved for the current query.
    """
    if 'retrieved_documents' in st.session_state and st.session_state['retrieved_documents']:
        # Use tabs for displaying retrieved documents
        with st.expander("View Retrieved Context", expanded=False):
            # Display reformulated question if available
            if 'last_reformulated_question' in st.session_state:
                st.markdown(f"**Reformulated question:** {st.session_state['last_reformulated_question']}")
                st.divider()
            
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
