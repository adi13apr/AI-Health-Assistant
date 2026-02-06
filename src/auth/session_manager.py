import streamlit as st
from datetime import datetime, timedelta
from config.app_config import SESSION_TIMEOUT_MINUTES
import json


class SessionManager:

    # ---------------- INIT SESSION ---------------- #
    @staticmethod
    def init_session():
        """Initialize or validate session."""

        if 'session_initialized' not in st.session_state:
            st.session_state.session_initialized = True
            SessionManager._restore_from_storage()

        if 'auth_service' not in st.session_state:
            from auth.auth_service import AuthService
            st.session_state.auth_service = AuthService()

        # ---- Session timeout check ---- #
        if 'last_activity' in st.session_state:
            idle_time = datetime.now() - st.session_state.last_activity
            if idle_time > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                SessionManager.clear_session_state()
                st.error("Session expired. Please log in again.")
                st.rerun()

        st.session_state.last_activity = datetime.now()

        # ---- Validate session token ---- #
        if 'user' in st.session_state:
            user_data = st.session_state.auth_service.validate_session_token()
            if not user_data:
                SessionManager.clear_session_state()
                st.error("Invalid session. Please log in again.")
                st.rerun()

    # ---------------- STORAGE RESTORE ---------------- #
    @staticmethod
    def _restore_from_storage():
        try:
            SessionManager._inject_storage_script()
        except Exception:
            pass

    # ---------------- STORAGE SCRIPT ---------------- #
    @staticmethod
    def _inject_storage_script():

        storage_script = """
        <script>
        window.addEventListener('DOMContentLoaded', function() {
            const storedAuth = localStorage.getItem('hia_auth');
            if (storedAuth) {
                try {
                    window.hia_auth_data = JSON.parse(storedAuth);
                } catch (e) {
                    localStorage.removeItem('hia_auth');
                }
            }
        });

        window.saveAuthData = function(authData) {
            localStorage.setItem('hia_auth', JSON.stringify(authData));
        };

        window.clearAuthData = function() {
            localStorage.removeItem('hia_auth');
        };

        window.getAuthData = function() {
            const stored = localStorage.getItem('hia_auth');
            return stored ? JSON.parse(stored) : null;
        };
        </script>
        """

        st.markdown(storage_script, unsafe_allow_html=True)

    # ---------------- CLEAR SESSION ---------------- #
    @staticmethod
    def clear_session_state():

        SessionManager._clear_persistent_storage()

        keys_to_keep = ['session_initialized']

        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]

    # ---------------- CLEAR STORAGE ---------------- #
    @staticmethod
    def _clear_persistent_storage():

        clear_script = """
        <script>
        if (typeof window.clearAuthData === 'function') {
            window.clearAuthData();
        }
        </script>
        """

        st.markdown(clear_script, unsafe_allow_html=True)

    # ---------------- SAVE STORAGE ---------------- #
    @staticmethod
    def _save_to_persistent_storage(user_data, auth_token):

        auth_data = {
            'user': user_data,
            'auth_token': auth_token,
            'timestamp': datetime.now().isoformat()
        }

        save_script = f"""
        <script>
        if (typeof window.saveAuthData === 'function') {{
            window.saveAuthData({json.dumps(auth_data)});
        }}
        </script>
        """

        st.markdown(save_script, unsafe_allow_html=True)

    # ---------------- AUTH CHECK ---------------- #
    @staticmethod
    def is_authenticated():
        return bool(st.session_state.get('user'))

    # ---------------- CREATE SESSION (FIXED) ---------------- #
    @staticmethod
    def create_chat_session():
        """Create a new chat session."""

        if not SessionManager.is_authenticated():
            return False, "Not authenticated"

        try:
            # ✅ FIXED USER ID PATH
            user_id = st.session_state.user["user"]["id"]

            return st.session_state.auth_service.create_session(user_id)

        except Exception as e:
            print("Create session error:", e)
            return False, str(e)

    # ---------------- GET SESSIONS (FIXED) ---------------- #
    @staticmethod
    def get_user_sessions():
        """Get user's chat sessions."""

        if not SessionManager.is_authenticated():
            return False, []

        try:
            # ✅ FIXED USER ID PATH
            user_id = st.session_state.user["user"]["id"]

            return st.session_state.auth_service.get_user_sessions(user_id)

        except Exception as e:
            print("Fetch sessions error:", e)
            return False, []

    # ---------------- DELETE SESSION ---------------- #
    @staticmethod
    def delete_session(session_id):

        if not SessionManager.is_authenticated():
            return False, "Not authenticated"

        try:
            return st.session_state.auth_service.delete_session(session_id)

        except Exception as e:
            print("Delete session error:", e)
            return False, str(e)

    # ---------------- LOGOUT ---------------- #
    @staticmethod
    def logout():

        if 'auth_service' in st.session_state:
            st.session_state.auth_service.sign_out()

        SessionManager.clear_session_state()

    # ---------------- LOGIN ---------------- #
    @staticmethod
    def login(email, password):

        if 'auth_service' not in st.session_state:
            from auth.auth_service import AuthService
            st.session_state.auth_service = AuthService()

        success, user_data = st.session_state.auth_service.sign_in(email, password)

        if success and 'auth_token' in st.session_state:
            SessionManager._save_to_persistent_storage(
                user_data,
                st.session_state.auth_token
            )

        return success, user_data
