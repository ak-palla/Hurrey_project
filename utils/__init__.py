"""
Utils package initialization.

This package contains utility functions for file handling and session management.
"""
from utils.file_handler import process_uploaded_files
from utils.session_manager import (
    initialize_session_state,
    get_session_history,
    clear_session_history
)
from utils.user_auth import (
    initialize_auth_state,
    login_user,
    register_user,
    logout_user,
    save_user_settings,
    load_user_settings,
    render_auth_ui
)

__all__ = [
    'process_uploaded_files',
    'initialize_session_state',
    'get_session_history',
    'clear_session_history',
    'initialize_auth_state',
    'login_user',
    'register_user',
    'logout_user',
    'save_user_settings',
    'load_user_settings',
    'render_auth_ui'
]
