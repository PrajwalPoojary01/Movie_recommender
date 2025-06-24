import streamlit as st
from db import register_user
import time

st.title("📝 Sign Up")

# If already logged in, redirect to main
if st.session_state.get("logged_in"):
    st.switch_page("main.py")
    st.stop()

# Input fields
new_username = st.text_input("Choose a username")
new_password = st.text_input("Choose a password", type="password")

# Register button
if st.button("Register"):
    success = register_user(new_username, new_password)

    if success:
        # Redirect to login after successful signup
        st.switch_page("01_login")
    else:
        st.error("❌ Username already exists. Try a different one.")
