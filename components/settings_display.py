"""
Component for displaying current personalization settings.
"""
import streamlit as st

def display_settings(personalization):
    """
    Display the current personalization settings in the UI.
    
    Args:
        personalization: Dictionary containing all personalization settings
    """
    st.subheader("Current Personalization Settings")
    settings_col1, settings_col2 = st.columns(2)
    
    with settings_col1:
        st.info(f"Tone: {personalization['tone']} | Goal: {personalization['goal']} | Length: {personalization['length']}")
    
    with settings_col2:
        st.info(f"Style: {personalization['style']} | Language: {personalization['language']} | Persona: {personalization['persona']}")

def display_personalization_details(personalization):
    """
    Display detailed personalization information in an expander.
    
    Args:
        personalization: Dictionary containing all personalization settings
    """
    with st.expander("Personalization Details", expanded=False):
        st.json(personalization)
