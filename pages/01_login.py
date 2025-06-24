import streamlit as st
from db import login_user
import time

st.title("🔐 Login")

# Already logged in?
if st.session_state.get("logged_in"):
    st.success(f"You're logged in as **{st.session_state['username']}**.")
    st.info("Go to the main section from the sidebar.")
    st.stop()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = login_user(username, password)

    if user:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = user[0]

        st.success("✅ Login successful! Redirecting...")

        time.sleep(1)
        st.rerun()  # ✅ This will now take user to main.py (streamlit auto loads it)

    else:
        st.error("❌ Invalid credentials. Please try again.")
