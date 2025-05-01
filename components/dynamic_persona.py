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
    
    # Use a different variable name to avoid conflict with the widget key
    if 'current_mood_override' not in st.session_state:
        st.session_state.current_mood_override = None
        
    # Initialize a separate session state variable to store the active persona settings
    # This avoids conflicts with widget keys
    if 'active_persona_settings' not in st.session_state:
        st.session_state.active_persona_settings = {
            "tone": "Friendly",
            "goal": "Educate",
            "length": "Medium",
            "style": "Straightforward",
            "language": "English",
            "persona": "Intermediate"
        }

def save_current_persona(name, personalization):
    """
    Save the current personalization settings as a named persona.
    
    Args:
        name: Name for the persona
        personalization: Dictionary of personalization settings
    """
    st.session_state.saved_personas[name] = personalization.copy()
    st.session_state.current_persona = name
    
    # Store the settings in the active_persona_settings
    # This avoids conflicts with widget keys
    st.session_state.active_persona_settings = personalization.copy()
    
    # Debug print to verify what's being saved
    print(f"Saved persona '{name}' with settings: {personalization}")
    print(f"Active settings after save: {st.session_state.active_persona_settings}")

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
        persona_settings = st.session_state.saved_personas[name].copy()
        
        # Store the settings in the active_persona_settings
        # This avoids conflicts with widget keys
        st.session_state.active_persona_settings = persona_settings.copy()
        
        # Debug print to verify what's being loaded
        print(f"Loaded persona '{name}' with settings: {persona_settings}")
        print(f"Active settings after load: {st.session_state.active_persona_settings}")
            
        return persona_settings
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
    
    # Use the different variable name to avoid conflict
    st.session_state.current_mood_override = mood
    
    # If we have a mood, update the active_persona_settings
    if mood and mood in mood_mapping:
        st.session_state.active_persona_settings["tone"] = mood_mapping[mood]
    elif mood is None and st.session_state.current_persona in st.session_state.saved_personas:
        # Reset to saved persona's tone if mood is cleared
        persona_settings = st.session_state.saved_personas[st.session_state.current_persona]
        if "tone" in persona_settings:
            st.session_state.active_persona_settings["tone"] = persona_settings["tone"]
    
    # Return the mapped tone for immediate use
    return mood_mapping.get(mood)

def get_current_persona_with_mood():
    """
    Get the current persona settings with any mood overrides applied.
    
    Returns:
        Dictionary of personalization settings with mood override applied
    """
    # Debug print to verify what's being returned at request time
    print(f"Returning active persona settings: {st.session_state.active_persona_settings}")
    return st.session_state.active_persona_settings.copy()

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
        save_button = st.button("Save Persona")
        if save_button:
            if persona_name:
                # Get the current personalization settings from session state
                # This matches the widget keys from sidebar.py
                current_settings = {}
                for key in ["tone", "goal", "length", "style", "language", "persona"]:
                    if key in st.session_state:
                        current_settings[key] = st.session_state[key]
                
                save_current_persona(persona_name, current_settings)
                st.success(f"Saved persona: {persona_name}")
                # Force a rerun to update the UI with new persona
                st.rerun()
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
            
            load_button = st.button("Load Persona")
            if selected_persona and load_button:
                persona_settings = load_persona(selected_persona)
                if persona_settings:
                    st.success(f"Loaded persona: {selected_persona}")
                    # Force a rerun to update the UI and apply persona settings to the chat
                    st.rerun()
        else:
            st.info("No saved personas yet. Save your current settings first.")
        
        # Mood override section
        st.subheader("Mood Override")
        # Use a different key for the mood selectbox
        mood_options = [None, "serious", "motivational", "sarcastic", "excited", "analytical"]
        selected_mood = st.selectbox(
            "Temporarily change tone based on mood:",
            options=mood_options,
            index=0,
            key="mood_override_selectbox"  # Changed key name here
        )
        
        mood_button = st.button("Apply Mood")
        if mood_button:
            # When the button is clicked, set the mood override
            tone_override = set_mood_override(selected_mood)
            if selected_mood:
                st.success(f"Applied {selected_mood} mood (tone: {tone_override})")
            else:
                st.success("Reset to default persona tone")
            # Force a rerun to apply mood to the current chat
            st.rerun()
    
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
    if st.session_state.current_mood_override:
        persona_context += f"\nThe user has requested you adopt a {st.session_state.current_mood_override} mood for this response. "
    
    # Insert the context after the first sentence
    if persona_context:
        parts = original_prompt.split(".", 1)
        if len(parts) > 1:
            modified_prompt = parts[0] + "." + persona_context + parts[1]
            return modified_prompt
    
    return original_prompt
