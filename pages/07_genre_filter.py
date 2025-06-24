import streamlit as st
import pickle
import pandas as pd
import requests
from utils import show_movie_details, show_logout_button
import streamlit as st
API_KEY = st.secrets["TMDB_API_KEY"]

st.set_page_config(page_title="Genre Filter", layout="wide")
show_logout_button()

# 🔐 Login required
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the genre filter.")
    st.stop()

# Load movies
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# Available genres
available_genres = sorted([
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
])

# TMDb genre mapping (hardcoded, or fetch from API if needed)
genre_map = {
    "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35,
    "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751,
    "Fantasy": 14, "History": 36, "Horror": 27, "Music": 10402,
    "Mystery": 9648, "Romance": 10749, "Science Fiction": 878,
    "TV Movie": 10770, "Thriller": 53, "War": 10752, "Western": 37
}

# Fetch movies by genre from TMDb
def fetch_movies_by_genre(genre_id):
    try:
        res = requests.get(
            f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}"
        )
        res.raise_for_status()
        return res.json().get("results", [])
    except:
        return []

# Show movie posters and buttons
def display_genre_movies(movie_list):
    cols = st.columns(5)
    for i, movie in enumerate(movie_list[:15]):  # limit to 15 movies
        movie_id = movie["id"]
        title = movie["title"]
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"

        with cols[i % 5]:
            st.image(poster_url)
            if st.button(f"ℹ️ {title}", key=f"genre_detail_{i}"):
                st.session_state.selected_movie_id = movie_id
                st.rerun()

# 🔍 Detail view
if st.session_state.get("selected_movie_id"):
    show_movie_details(
        movie_id=st.session_state.selected_movie_id,
        api_key=API_KEY,
        user_id=st.session_state.user_id,
        db=__import__("db")
    )
    if st.button("🔙 Back to Genre List"):
        st.session_state.selected_movie_id = None
        st.rerun()

# 🎯 Genre selection and movie grid
else:
    st.title("🎭 Browse by Genre")

    selected_genre = st.selectbox("Choose a genre:", available_genres)
    if selected_genre:
        genre_id = genre_map[selected_genre]
        movies_by_genre = fetch_movies_by_genre(genre_id)

        if movies_by_genre:
            display_genre_movies(movies_by_genre)
        else:
            st.warning("No movies found for this genre.")
