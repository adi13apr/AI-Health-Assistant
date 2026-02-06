import streamlit as st
from supabase import create_client
from datetime import datetime
import re


class AuthService:

    def __init__(self):
        try:
            self.supabase = create_client(
                st.secrets["SUPABASE_URL"],
                st.secrets["SUPABASE_KEY"]
            )
        except Exception as e:
            st.error(f"Failed to initialize services: {str(e)}")
            raise e

        self.try_restore_session()

    # ---------------- SESSION RESTORE ---------------- #
    def try_restore_session(self):
        try:
            session = self.supabase.auth.get_session()
            if session and session.access_token:
                user = self.supabase.auth.get_user()
                if user and user.user:
                    user_data = self.get_user_data(user.user.id)
                    if user_data:
                        st.session_state.auth_token = session.access_token
                        st.session_state.refresh_token = session.refresh_token
                        st.session_state.user = user_data
        except Exception:
            pass

    # ---------------- SIGN IN ---------------- #
    def sign_in(self, email, password):
        try:
            auth_response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )

            if auth_response and auth_response.user:

                user_data = self.get_user_data(auth_response.user.id)

                st.session_state.auth_token = auth_response.session.access_token
                st.session_state.refresh_token = auth_response.session.refresh_token
                st.session_state.user = user_data

                return True, user_data

            return False, "Invalid login"

        except Exception as e:
            return False, str(e)

    # ---------------- CREATE SESSION (FIXED) ---------------- #
    def create_session(self, user_id, title=None):
        """Create a new chat session"""

        try:
            current_time = datetime.now()

            default_title = (
                f"{current_time.strftime('%d-%m-%Y')} | "
                f"{current_time.strftime('%H:%M:%S')}"
            )

            session_data = {
                "user_id": user_id,
                "title": title or default_title
            }

            response = (
                self.supabase
                .table("chat_sessions")
                .insert(session_data)
                .execute()
            )

            if response.data and len(response.data) > 0:
                return True, response.data[0]

            return False, "Insert failed"

        except Exception as e:
            print("Create session error:", e)
            return False, str(e)

    # ---------------- GET USER SESSIONS ---------------- #
    def get_user_sessions(self, user_id):
        try:
            result = (
                self.supabase
                .table("chat_sessions")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )

            return True, result.data

        except Exception as e:
            return False, str(e)

    # ---------------- SAVE MESSAGE ---------------- #
    def save_chat_message(self, session_id, content, role="user"):
        try:
            message_data = {
                "session_id": session_id,
                "content": content,
                "role": role
            }

            result = (
                self.supabase
                .table("chat_messages")
                .insert(message_data)
                .execute()
            )

            return True, result.data[0]

        except Exception as e:
            return False, str(e)

    # ---------------- GET MESSAGES ---------------- #
    def get_session_messages(self, session_id):
        try:
            result = (
                self.supabase
                .table("chat_messages")
                .select("*")
                .eq("session_id", session_id)
                .order("created_at")
                .execute()
            )

            return True, result.data

        except Exception as e:
            return False, str(e)

    # ---------------- DELETE SESSION ---------------- #
    def delete_session(self, session_id):
        try:
            self.supabase.table("chat_messages").delete().eq(
                "session_id", session_id
            ).execute()

            self.supabase.table("chat_sessions").delete().eq(
                "id", session_id
            ).execute()

            return True, None

        except Exception as e:
            return False, str(e)

    # ---------------- GET USER DATA ---------------- #
    def get_user_data(self, user_id):
        try:
            response = (
                self.supabase
                .table("users")
                .select("*")
                .eq("id", user_id)
                .single()
                .execute()
            )

            return response.data

        except Exception:
            return None
