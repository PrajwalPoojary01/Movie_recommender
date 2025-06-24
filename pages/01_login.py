import streamlit as st
from db import login_user
import time

st.title("🔐 Login")

if st.session_state.get("signup_success"):
    st.success("✅ Signup successful! You can now log in.")
    del st.session_state.signup_success


# If already logged in, skip login page
if st.session_state.get("logged_in"):
    st.switch_page("main.py")  # Automatically redirects if user visits login again
    st.stop()

# Input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):
    user = login_user(username, password)

    if user:
        # Save login info
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = user[0]

        # Instant redirect to main section
        st.switch_page("main.py")  # This is the root script, not inside /pages/
    else:
        st.error("❌ Invalid credentials. Please try again.")
