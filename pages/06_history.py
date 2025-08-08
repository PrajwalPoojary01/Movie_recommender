import streamlit as st
import requests
from db import get_history, clear_history
from utils import show_movie_details, show_logout_button

API_KEY = st.secrets["TMDB_API_KEY"]

st.set_page_config(page_title="Watch History", layout="wide")
show_logout_button()

# 🔐 Require login
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to view your history.")
    st.stop()

# 📦 Fetch movie details from TMDb
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except:
        return None

# 📦 Fetch similar movies from TMDb
def fetch_similar_movies(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={API_KEY}&language=en-US"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json().get("results", [])
    except:
        return []

user_id = st.session_state.user_id
history = get_history(user_id)

st.title("📜 Watched History")

# 🎯 Detail view
if st.session_state.get("selected_movie_id"):
    show_movie_details(
        movie_id=st.session_state.selected_movie_id,
        api_key=API_KEY,
        user_id=user_id,
        db=__import__("db"),
        context="history"
    )
    if st.button("🔙 Back to History"):
        st.session_state.selected_movie_id = None
        st.rerun()

# 🧹 Clear History
elif not history:
    st.info("You haven't marked any movies as watched.")
else:
    if st.button("🧹 Clear History"):
        clear_history(user_id)
        st.success("History cleared.")
        st.rerun()

    st.subheader("🎞️ Movies You've Watched")
    cols = st.columns(5)
    for idx, (title, movie_id, added_at) in enumerate(history):
        try:
            movie_id_int = int.from_bytes(movie_id, byteorder="little") if isinstance(movie_id, bytes) else int(movie_id)
        except:
            continue

        details = fetch_movie_details(movie_id_int)
        if not details:
            continue

        poster_path = details.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"

        with cols[idx % 5]:
            st.image(poster_url)
            st.caption(f"🕒 Watched on: {added_at}")
            if st.button(f"ℹ️ {title}", key=f"detail_hist_{idx}"):
                st.session_state.selected_movie_id = movie_id_int
                st.rerun()

    # 🎯 Recommend based on history
    st.markdown("---")
    st.subheader("🧠 Because you watched:")
    recommended_movies = []
    for _, movie_id, _ in history:
        movie_id_int = int.from_bytes(movie_id, byteorder="little") if isinstance(movie_id, bytes) else int(movie_id)
        similar_movies = fetch_similar_movies(movie_id_int)
        for m in similar_movies:
            if m not in recommended_movies:
                recommended_movies.append(m)

    recommended_movies = recommended_movies[:5]
    cols = st.columns(5)
    for i, m in enumerate(recommended_movies):
        poster_path = m.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"
        with cols[i % 5]:
            st.image(poster_url)
            if st.button(f"ℹ️ {m['title']}", key=f"histrec_{i}"):
                st.session_state.selected_movie_id = m["id"]
                st.rerun()
