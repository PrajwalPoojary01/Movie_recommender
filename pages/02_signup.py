import streamlit as st
from db import register_user
from utils import show_logout_button
show_logout_button()


st.set_page_config(page_title="Sign Up", layout="wide")
st.title("📝 Sign Up")




if st.session_state.get("logged_in", False):
    st.warning("You're already logged in.")
    st.stop()

username = st.text_input("Choose a username")
password = st.text_input("Choose a password", type="password")

if st.button("Register"):
    if username and password:
        success = register_user(username, password)
        if success:
            st.success("User registered! Please click **Login** to continue.")
            st.stop()  # ✅ STOP and let user manually go to Login
        else:
            st.error("Username already exists.")
    else:
        st.warning("Please enter both username and password.")
