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
    # Initialize active_persona_settings if not present
    if 'active_persona_settings' not in st.session_state:
        st.session_state.active_persona_settings = {
            "tone": "Friendly",
            "goal": "Educate",
            "length": "Medium",
            "style": "Straightforward",
            "language": "English",
            "persona": "Intermediate"
        }
    
    # Get defaults from active_persona_settings
    active_settings = st.session_state.active_persona_settings
    
    with st.sidebar:
        st.header("Personalization Settings")
        
        # Tone selection - use default from active settings
        tone_options = ["Formal", "Friendly", "Humorous", "Professional", "Empathetic"]
        default_index = tone_options.index(active_settings.get("tone", "Friendly")) if active_settings.get("tone") in tone_options else 1
        tone = st.selectbox("Select Tone", tone_options, index=default_index, key="tone")
        
        # Communication goal
        goal_options = ["Educate", "Summarize", "Advise", "Entertain", "Explain"]
        default_index = goal_options.index(active_settings.get("goal", "Educate")) if active_settings.get("goal") in goal_options else 0
        goal = st.selectbox("Communication Goal", goal_options, index=default_index, key="goal")
        
        # Response length preference
        length_options = ["Very Short", "Short", "Medium", "Detailed", "Comprehensive"]
        default_index = length_options.index(active_settings.get("length", "Medium")) if active_settings.get("length") in length_options else 2
        length = st.selectbox("Response Length", length_options, index=default_index, key="length")
        
        # Response style
        style_options = ["Straightforward", "Storytelling", "Bullet Points", "Step-by-Step", "Analytical"]
        default_index = style_options.index(active_settings.get("style", "Straightforward")) if active_settings.get("style") in style_options else 0
        style = st.selectbox("Response Style", style_options, index=default_index, key="style")
        
        # Language preference
        language_options = ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
        default_index = language_options.index(active_settings.get("language", "English")) if active_settings.get("language") in language_options else 0
        language = st.selectbox("Language", language_options, index=default_index, key="language")
        
        # User persona traits
        persona_options = ["Beginner", "Intermediate", "Expert", "Academic", "Professional", "Student"]
        default_index = persona_options.index(active_settings.get("persona", "Intermediate")) if active_settings.get("persona") in persona_options else 1
        persona = st.selectbox("User Persona", persona_options, index=default_index, key="persona")
    
    # Update active_persona_settings with current widget values
    # This will be used to set defaults next time and for personalization in responses
    st.session_state.active_persona_settings = {
        "tone": tone,
        "goal": goal,
        "length": length,
        "style": style,
        "language": language,
        "persona": persona
    }
    
    # Return all personalization settings as a dictionary
    return {
        "tone": tone,
        "goal": goal,
        "length": length,
        "style": style,
        "language": language,
        "persona": persona
    }
