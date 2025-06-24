import streamlit as st
from db import login_user
from utils import show_logout_button
show_logout_button()


st.set_page_config(page_title="Login", layout="wide")
st.title("🔑 Login")




if st.session_state.get("logged_in", False):
    st.warning("You're logged in, Navigate to Main Section.")
    st.stop()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = login_user(username, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = user[0]

        # ✅ Use new API for query params
        st.query_params["start"] = "main"
        st.rerun()
    else:
        st.error("Invalid username or password.")
