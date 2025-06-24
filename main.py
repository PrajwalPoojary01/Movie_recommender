
import streamlit as st
from utils import show_logout_button
show_logout_button()



st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Welcome to Movie Recommender System")

params = st.query_params()
if params.get("page") == ["main"]:
    st.success("Welcome to the main page!")

# ✅ Show login success if redirected
if st.query_params.get("start") == "main":
    st.query_params.clear()
    st.success("✅ Login successful! Welcome back.")


if not st.session_state.get("logged_in", False):
    st.subheader("🔐 Please log in to continue")
    st.markdown("If you don't have an account, register below:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login"):
            st.switch_page("pages/01_login.py")
    with col2:
        if st.button("📝 Sign Up"):
            st.switch_page("pages/02_signup.py")

else:
    username = st.session_state.username
    st.success(f"Welcome back, {username}! 👋")

    st.subheader("📂 Choose a feature:")
    st.page_link("pages/03_recommender.py", label="🎥 Movie Recommender")
    st.page_link("pages/05_watchlist.py", label="📃 Watchlist")
    st.page_link("pages/06_history.py", label="📜 Watched History")
    st.page_link("pages/07_genre_filter.py", label="🎭 Genre Filter")
    st.page_link("pages/08_trending_popular.py", label="🔥 Trending & Popular")
