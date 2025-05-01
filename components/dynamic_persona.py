"""
Component for dynamic personalization switching during conversation.
"""
import streamlit as st

def initialize_persona_state():
    """
    Initialize session state for dynamic persona switching.
    """
    if 'saved_personas' not in st.session_state:
        st.session_state.saved_personas = {}
    
    if 'current_persona' not in st.session_state:
        st.session_state.current_persona = "default"
    
    if 'mood_override' not in st.session_state:
        st.session_state.mood_override = None

def save_current_persona(name, personalization):
    """
    Save the current personalization settings as a named persona.
    
    Args:
        name: Name for the persona
        personalization: Dictionary of personalization settings
    """
    st.session_state.saved_personas[name] = personalization.copy()
    st.session_state.current_persona = name

def load_persona(name):
    """
    Load a saved persona.
    
    Args:
        name: Name of the saved persona
        
    Returns:
        Dictionary with personalization settings or None if not found
    """
    if name in st.session_state.saved_personas:
        st.session_state.current_persona = name
        return st.session_state.saved_personas[name]
    return None

def set_mood_override(mood):
    """
    Set a temporary mood override that modifies the tone.
    
    Args:
        mood: Mood to set (serious, motivational, sarcastic, etc.)
    """
    mood_mapping = {
        "serious": "Formal",
        "motivational": "Empathetic",
        "sarcastic": "Humorous",
        "excited": "Friendly",
        "analytical": "Professional",
        None: None  # Reset to default persona tone
    }
    
    st.session_state.mood_override = mood
    
    # Return the mapped tone for immediate use
    return mood_mapping.get(mood)

def get_current_persona_with_mood():
    """
    Get the current persona settings with any mood overrides applied.
    
    Returns:
        Dictionary of personalization settings with mood override applied
    """
    current_settings = {}
    
    # Get base settings from current persona
    if st.session_state.current_persona in st.session_state.saved_personas:
        current_settings = st.session_state.saved_personas[st.session_state.current_persona].copy()
    
    # Apply mood override if set
    if st.session_state.mood_override:
        mood_tone = set_mood_override(st.session_state.mood_override)
        if mood_tone:
            current_settings["tone"] = mood_tone
    
    return current_settings

def render_persona_management():
    """
    Render UI components for persona management in the sidebar.
    
    Returns:
        Dictionary with current personalization settings after considering persona/mood
    """
    initialize_persona_state()
    
    with st.sidebar.expander("Persona Management", expanded=False):
        # Save current settings as persona
        persona_name = st.text_input("Save current settings as persona:", key="save_persona_name")
        if st.button("Save Persona"):
            if persona_name:
                # Get the current personalization settings from sidebar
                current_settings = {
                    "tone": st.session_state.get("tone", "Formal"),
                    "goal": st.session_state.get("goal", "Educate"),
                    "length": st.session_state.get("length", "Medium"),
                    "style": st.session_state.get("style", "Straightforward"),
                    "language": st.session_state.get("language", "English"),
                    "persona": st.session_state.get("persona", "Intermediate")
                }
                save_current_persona(persona_name, current_settings)
                st.success(f"Saved persona: {persona_name}")
            else:
                st.error("Please enter a name for the persona")
        
        # Load saved persona
        saved_personas = list(st.session_state.saved_personas.keys())
        if saved_personas:
            selected_persona = st.selectbox(
                "Load saved persona:", 
                options=[""] + saved_personas,
                index=0,
                key="load_persona_select"
            )
            
            if selected_persona and st.button("Load Persona"):
                persona_settings = load_persona(selected_persona)
                if persona_settings:
                    # Update session state to reflect loaded persona
                    for key, value in persona_settings.items():
                        st.session_state[key] = value
                    st.success(f"Loaded persona: {selected_persona}")
                    # Force a rerun to update the UI
                    st.rerun()
        else:
            st.info("No saved personas yet. Save your current settings first.")
        
        # Mood override section
        st.subheader("Mood Override")
        mood_options = [None, "serious", "motivational", "sarcastic", "excited", "analytical"]
        selected_mood = st.selectbox(
            "Temporarily change tone based on mood:",
            options=mood_options,
            index=0,
            key="mood_override"
        )
        
        if st.button("Apply Mood"):
            tone_override = set_mood_override(selected_mood)
            if selected_mood:
                st.success(f"Applied {selected_mood} mood (tone: {tone_override})")
            else:
                st.success("Reset to default persona tone")
    
    # Get final personalization with any overrides applied
    return get_current_persona_with_mood()

def inject_dynamic_persona_instructions(original_prompt, personalization):
    """
    Modify the original prompt to include dynamic persona switching instructions.
    
    Args:
        original_prompt: Original system prompt
        personalization: Dictionary of personalization settings
        
    Returns:
        Modified prompt with persona switching instructions
    """
    persona_context = ""
    
    # Add info about current persona
    if st.session_state.current_persona != "default":
        persona_context += f"\nYou are currently using the '{st.session_state.current_persona}' persona. "
    
    # Add info about mood override
    if st.session_state.mood_override:
        persona_context += f"\nThe user has requested you adopt a {st.session_state.mood_override} mood for this response. "
    
    # Insert the context after the first sentence
    if persona_context:
        parts = original_prompt.split(".", 1)
        if len(parts) > 1:
            modified_prompt = parts[0] + "." + persona_context + parts[1]
            return modified_prompt
    
    return original_prompt
