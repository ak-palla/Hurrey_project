"""
Utilities for simple user authentication and saving personalized settings.
"""
import streamlit as st
import json
import os
import datetime

# Directory to store user data
USER_DATA_DIR = "./user_data"

def initialize_auth_state():
    """
    Initialize authentication state variables.
    """
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'user_settings' not in st.session_state:
        st.session_state.user_settings = {}

def login_user(username, password):
    """
    Log in a user with the given credentials.
    
    Args:
        username: Username
        password: Password
        
    Returns:
        Boolean indicating success
    """
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
    
    user_file = os.path.join(USER_DATA_DIR, f"{username}.json")
    
    if not os.path.exists(user_file):
        st.error("User does not exist")
        return False
    
    try:
        with open(user_file, 'r') as f:
            user_data = json.load(f)
            
        if user_data.get('password') == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.session_state.user_settings = user_data.get('settings', {})
            
            # Update last login time
            user_data['last_login'] = datetime.datetime.now().isoformat()
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)
                
            return True
        else:
            st.error("Incorrect password")
            return False
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return False

def register_user(username, password):
    """
    Register a new user.
    
    Args:
        username: Username
        password: Password
        
    Returns:
        Boolean indicating success
    """
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
    
    user_file = os.path.join(USER_DATA_DIR, f"{username}.json")
    
    if os.path.exists(user_file):
        st.error("Username already exists")
        return False
    
    try:
        user_data = {
            'username': username,
            'password': password,
            'created_at': datetime.datetime.now().isoformat(),
            'last_login': datetime.datetime.now().isoformat(),
            'settings': {
                'default_session': f"{username}_default",
                'default_personalization': {
                    'tone': 'Friendly',
                    'goal': 'Educate',
                    'length': 'Medium',
                    'style': 'Straightforward',
                    'language': 'English',
                    'persona': 'Intermediate'
                },
                'saved_personas': {},
                'saved_sessions': []
            }
        }
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.user_settings = user_data['settings']
        
        return True
    except Exception as e:
        st.error(f"Registration failed: {str(e)}")
        return False

def logout_user():
    """
    Log out the current user.
    """
    save_user_settings()  # Save settings before logout
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.user_settings = {}

def save_user_settings():
    """
    Save the current user's settings to their file.
    
    Returns:
        Boolean indicating success
    """
    if not st.session_state.logged_in or not st.session_state.current_user:
        return False
    
    username = st.session_state.current_user
    user_file = os.path.join(USER_DATA_DIR, f"{username}.json")
    
    try:
        # Read existing user data
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        # Update settings
        user_data['settings'] = st.session_state.user_settings
        
        # Save personas
        if 'saved_personas' in st.session_state:
            user_data['settings']['saved_personas'] = st.session_state.saved_personas
        
        # Save last session ID
        if 'session_id' in st.session_state:
            user_data['settings']['last_session_id'] = st.session_state.session_id
            
            # Add to saved sessions if not already there
            if st.session_state.session_id not in user_data['settings'].get('saved_sessions', []):
                if 'saved_sessions' not in user_data['settings']:
                    user_data['settings']['saved_sessions'] = []
                user_data['settings']['saved_sessions'].append(st.session_state.session_id)
        
        # Save personalization settings
        personalization_keys = ['tone', 'goal', 'length', 'style', 'language', 'persona']
        current_personalization = {}
        for key in personalization_keys:
            if key in st.session_state:
                current_personalization[key] = st.session_state[key]
        
        if current_personalization:
            user_data['settings']['default_personalization'] = current_personalization
            
        # Write back to file
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
            
        return True
    except Exception as e:
        st.error(f"Failed to save user settings: {str(e)}")
        return False

def load_user_settings():
    """
    Load a user's saved settings into session state.
    
    Returns:
        Boolean indicating success
    """
    if not st.session_state.logged_in or not st.session_state.current_user:
        return False
        
    try:
        # Load saved personas
        if 'saved_personas' in st.session_state.user_settings:
            st.session_state.saved_personas = st.session_state.user_settings.get('saved_personas', {})
            
        # Load default session
        if 'default_session' in st.session_state.user_settings:
            st.session_state.session_id = st.session_state.user_settings.get('default_session')
            
        # Load personalization settings
        if 'default_personalization' in st.session_state.user_settings:
            personalization = st.session_state.user_settings.get('default_personalization', {})
            for key, value in personalization.items():
                st.session_state[key] = value
                
        return True
    except Exception as e:
        st.error(f"Failed to load user settings: {str(e)}")
        return False

def render_auth_ui():
    """
    Render the authentication UI.
    
    Returns:
        Boolean indicating if the user is logged in
    """
    initialize_auth_state()
    
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.current_user}")
        if st.sidebar.button("Logout"):
            logout_user()
            st.rerun()
        return True
    else:
        with st.sidebar.expander("Login / Register", expanded=False):
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input("Password", type="password", key="login_password")
                if st.button("Login"):
                    if login_user(login_username, login_password):
                        load_user_settings()
                        st.rerun()
            
            with tab2:
                reg_username = st.text_input("Username", key="reg_username")
                reg_password = st.text_input("Password", type="password", key="reg_password")
                reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
                if st.button("Register"):
                    if reg_password != reg_password_confirm:
                        st.error("Passwords do not match")
                    elif register_user(reg_username, reg_password):
                        st.success("Registration successful!")
                        st.rerun()
        
        return False
