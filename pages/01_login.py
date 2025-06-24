import streamlit as st
from db import login_user
import time

st.title("🔐 Login")

# If already logged in
if st.session_state.get("logged_in"):
    st.success(f"You're logged in as **{st.session_state['username']}**.")
    st.info("Go to the main section from the sidebar.")
    st.stop()

# Inputs
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):
    user = login_user(username, password)

    if user:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = user[0]

        st.success("✅ Login successful! Redirecting to main...")

        # ✅ Redirect using query param
        time.sleep(1.5)
        st.experimental_set_query_params(page="main")  # You can read this param in main.py

        st.markdown("""
            <meta http-equiv="refresh" content="0;url=/?">
        """, unsafe_allow_html=True)

    else:
        st.error("❌ Invalid credentials. Please try again.")
