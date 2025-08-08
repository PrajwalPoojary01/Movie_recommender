import streamlit as st
import requests
from utils import show_movie_details, show_logout_button
from db import get_history
import random

API_KEY = st.secrets["TMDB_API_KEY"]

st.set_page_config(page_title="Recommender", layout="wide")
show_logout_button()

# 🔐 Block if not logged in
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the recommender.")
    st.stop()

# 📦 Fetch popular movies for the dropdown
def fetch_popular_movies():
    try:
        res = requests.get(
            f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1"
        )
        res.raise_for_status()
        return res.json().get("results", [])
    except:
        return []

# 📦 Fetch similar movies
def fetch_similar_movies(movie_id):
    try:
        res = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={API_KEY}&language=en-US&page=1"
        )
        res.raise_for_status()
        return res.json().get("results", [])
    except:
        return []

# 📦 Recommend from history
def recommend_from_history(user_id):
    watched = get_history(user_id)
    if not watched:
        return []

    recommended_movies = []
    for _, movie_id, _ in watched[:3]:  # limit to 3 most recent
        movie_id_int = int.from_bytes(movie_id, 'little') if isinstance(movie_id, bytes) else int(movie_id)
        similar = fetch_similar_movies(movie_id_int)
        for m in similar:
            if m not in recommended_movies:
                recommended_movies.append(m)
    return recommended_movies[:5]

# 🎯 Display movies
def display_movies(movie_list, key_prefix):
    cols = st.columns(5)
    for i, movie in enumerate(movie_list[:5]):
        movie_id = movie["id"]
        title = movie["title"]
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"

        with cols[i % 5]:
            st.image(poster_url)
            if st.button(f"ℹ️ {title}", key=f"{key_prefix}_{i}"):
                st.session_state.selected_movie_id = movie_id
                st.rerun()

# 📽️ Detail View
if st.session_state.get("selected_movie_id"):
    show_movie_details(
        movie_id=st.session_state.selected_movie_id,
        api_key=API_KEY,
        user_id=st.session_state.user_id,
        db=__import__("db")
    )
    if st.button("🔙 Back to Recommendations"):
        st.session_state.selected_movie_id = None
        st.rerun()

# 🎬 Main View
else:
    st.title("🎬 Movie Recommender")

    popular_movies = fetch_popular_movies()
    movie_titles = [m["title"] for m in popular_movies]
    movie_lookup = {m["title"]: m["id"] for m in popular_movies}

    selected_movie = st.selectbox("Choose a movie:", movie_titles)

    col_rec, col_surprise = st.columns([1, 1])

    with col_rec:
        if st.button("🎯 Show Recommendations"):
            similar_movies = fetch_similar_movies(movie_lookup[selected_movie])
            if similar_movies:
                st.subheader("🎯 Top Recommendations")
                display_movies(similar_movies, "rec")

    with col_surprise:
        if st.button("🎲 Surprise Me"):
            random_movie = random.choice(popular_movies)
            st.session_state.selected_movie_id = random_movie["id"]
            st.rerun()

    # 📈 Personalized Section
    history_recs = recommend_from_history(st.session_state.user_id)
    if history_recs:
        st.markdown("---")
        st.subheader("🧠 Because you watched:")
        display_movies(history_recs, "histrec")
