import streamlit as st
from db import register_user
import time

st.title("📝 Sign Up")

# If already logged in, redirect to main
if st.session_state.get("logged_in"):
    st.switch_page("main.py")  # if main is in root
    st.stop()

# Input fields
new_username = st.text_input("Choose a username")
new_password = st.text_input("Choose a password", type="password")

# Register button
if st.button("Register"):
    success = register_user(new_username, new_password)

    if success:
        # ✅ Set a session flag to show after redirect (optional)
        st.session_state.signup_success = True

        # ✅ Redirect to login by reloading the app with ?page=01_login
        st.markdown("""
            <meta http-equiv="refresh" content="0; url=/?page=01_login">
        """, unsafe_allow_html=True)
        st.stop()

    else:
        st.error("❌ Username already exists. Try a different one.")
