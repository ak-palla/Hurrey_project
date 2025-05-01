"""
Sidebar component for personalization settings.
"""
import streamlit as st

def render_sidebar():
    """
    Render the sidebar with personalization options.
    
    Returns:
        Dictionary containing all personalization settings
    """
    with st.sidebar:
        st.header("Personalization Settings")
        
        # Tone selection
        tone_options = ["Formal", "Friendly", "Humorous", "Professional", "Empathetic"]
        tone = st.selectbox("Select Tone", tone_options)
        
        # Communication goal
        goal_options = ["Educate", "Summarize", "Advise", "Entertain", "Explain"]
        goal = st.selectbox("Communication Goal", goal_options)
        
        # Response length preference
        length_options = ["Very Short", "Short", "Medium", "Detailed", "Comprehensive"]
        length = st.selectbox("Response Length", length_options)
        
        # Response style
        style_options = ["Straightforward", "Storytelling", "Bullet Points", "Step-by-Step", "Analytical"]
        style = st.selectbox("Response Style", style_options)
        
        # Language preference
        language_options = ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
        language = st.selectbox("Language", language_options)
        
        # User persona traits
        persona_options = ["Beginner", "Intermediate", "Expert", "Academic", "Professional", "Student"]
        persona = st.selectbox("User Persona", persona_options)
    
    # Return all personalization settings as a dictionary
    return {
        "tone": tone,
        "goal": goal,
        "length": length,
        "style": style,
        "language": language,
        "persona": persona
    }
