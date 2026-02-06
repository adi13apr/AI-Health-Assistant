import streamlit as st
from supabase import create_client
from datetime import datetime
import re


class AuthService:

    # ---------------- INIT ---------------- #
    def __init__(self):
        try:
            self.supabase = create_client(
                st.secrets["SUPABASE_URL"],
                st.secrets["SUPABASE_KEY"]
            )
        except Exception as e:
            st.error(f"Failed to initialize Supabase: {str(e)}")
            raise e

        self.try_restore_session()

    # ---------------- RESTORE SESSION ---------------- #
    def try_restore_session(self):
        """Restore Supabase session if exists"""

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

    # ---------------- VALIDATE TOKEN ---------------- #
    def validate_session_token(self):
        """Validate existing Supabase session"""

        try:
            session = self.supabase.auth.get_session()

            if not session or not session.access_token:
                return None

            user = self.supabase.auth.get_user()

            if not user or not user.user:
                return None

            return self.get_user_data(user.user.id)

        except Exception:
            return None

    # ---------------- SIGN UP ---------------- #
    def sign_up(self, email, password, name):

        try:
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": {"name": name}},
            })

            if not auth_response.user:
                return False, "Signup failed"

            user_data = {
                "id": auth_response.user.id,
                "email": email,
                "name": name,
                "created_at": datetime.now().isoformat(),
            }

            self.supabase.table("users").insert(user_data).execute()

            return True, user_data

        except Exception as e:
            return False, str(e)

    # ---------------- SIGN IN ---------------- #
    def sign_in(self, email, password):

        try:
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not auth_response.user:
                return False, "Invalid login"

            user_data = self.get_user_data(auth_response.user.id)

            st.session_state.auth_token = auth_response.session.access_token
            st.session_state.refresh_token = auth_response.session.refresh_token
            st.session_state.user = user_data

            return True, user_data

        except Exception as e:
            return False, str(e)

    # ---------------- SIGN OUT ---------------- #
    def sign_out(self):

        try:
            self.supabase.auth.sign_out()
        except Exception:
            pass

    # ---------------- CREATE SESSION ---------------- #
def create_session(self, user_id, title=None):
    try:
        from datetime import datetime

        now = datetime.now()
        default_title = f"{now.strftime('%d-%m-%Y')} | {now.strftime('%H:%M:%S')}"

        data = {
            "user_id": user_id,
            "title": title or default_title
        }

        print("Creating session with:", data)   # DEBUG

        response = (
            self.supabase
            .table("chat_sessions")
            .insert(data)
            .execute()
        )

        print("Supabase response:", response)   # DEBUG

        if response.data:
            return True, response.data[0]

        return False, "No data returned"

    except Exception as e:
        print("CREATE SESSION ERROR:", e)   # 👈 REAL ERROR
        return False, str(e)


    # ---------------- GET USER SESSIONS ---------------- #
    def get_user_sessions(self, user_id):

        try:
            response = (
                self.supabase
                .table("chat_sessions")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )

            return True, response.data

        except Exception as e:
            return False, str(e)

    # ---------------- SAVE MESSAGE ---------------- #
    def save_chat_message(self, session_id, content, role="user"):

        try:
            data = {
                "session_id": session_id,
                "content": content,
                "role": role
            }

            response = (
                self.supabase
                .table("chat_messages")
                .insert(data)
                .execute()
            )

            return True, response.data[0]

        except Exception as e:
            return False, str(e)

    # ---------------- GET MESSAGES ---------------- #
    def get_session_messages(self, session_id):

        try:
            response = (
                self.supabase
                .table("chat_messages")
                .select("*")
                .eq("session_id", session_id)
                .order("created_at")
                .execute()
            )

            return True, response.data

        except Exception as e:
            return False, str(e)

    # ---------------- DELETE SESSION ---------------- #
    def delete_session(self, session_id):

        try:
            self.supabase.table("chat_messages") \
                .delete() \
                .eq("session_id", session_id) \
                .execute()

            self.supabase.table("chat_sessions") \
                .delete() \
                .eq("id", session_id) \
                .execute()

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
