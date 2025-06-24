import streamlit as st
from db import login_user
from streamlit_extras.switch_page_button import switch_page  # or use st.switch_page

st.title("🔐 Login")

# If already logged in, show message
if st.session_state.get("logged_in"):
    st.success(f"You're already logged in as **{st.session_state['username']}**.")
    st.info("Go to the main page to explore recommendations.")
    st.stop()  # Prevents re-showing login form

# Input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):
    user = login_user(username, password)

    if user:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = user[0]  # Assuming user = (id, username)
        st.success("✅ Login successful! Redirecting...")

        switch_page("main")  # OR st.switch_page("main.py")
    else:
        st.error("❌ Invalid credentials. Please try again.")
