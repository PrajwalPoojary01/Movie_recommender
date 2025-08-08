import streamlit as st
import requests
from utils import show_movie_details, show_logout_button

API_KEY = st.secrets["TMDB_API_KEY"]

st.set_page_config(page_title="Genre Filter", layout="wide")
show_logout_button()

# 🔐 Require login
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the genre filter.")
    st.stop()

# ✅ TMDb Genre Mapping
genre_map = {
    "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35,
    "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751,
    "Fantasy": 14, "History": 36, "Horror": 27, "Music": 10402,
    "Mystery": 9648, "Romance": 10749, "Science Fiction": 878,
    "TV Movie": 10770, "Thriller": 53, "War": 10752, "Western": 37
}

# 📦 Fetch movies by genre
def fetch_movies_by_genre(genre_id):
    try:
        res = requests.get(
            f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&sort_by=popularity.desc"
        )
        res.raise_for_status()
        return res.json().get("results", [])
    except:
        return []

# 🎯 Display movie grid
def display_movies(movie_list):
    cols = st.columns(5)
    for i, movie in enumerate(movie_list[:15]):
        movie_id = movie["id"]
        title = movie["title"]
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"

        with cols[i % 5]:
            st.image(poster_url)
            if st.button(f"ℹ️ {title}", key=f"genre_detail_{i}"):
                st.session_state.selected_movie_id = movie_id
                st.rerun()

# 🔍 Movie detail view
if st.session_state.get("selected_movie_id"):
    show_movie_details(
        movie_id=st.session_state.selected_movie_id,
        api_key=API_KEY,
        user_id=st.session_state.user_id,
        db=__import__("db")
    )
    if st.button("🔙 Back to Genres"):
        st.session_state.selected_movie_id = None
        st.rerun()

# 🎬 Genre selection
else:
    st.title("🎭 Browse by Genre")
    selected_genre = st.selectbox("Choose a genre:", sorted(genre_map.keys()))

    if selected_genre:
        genre_id = genre_map[selected_genre]
        movies_by_genre = fetch_movies_by_genre(genre_id)

        if movies_by_genre:
            display_movies(movies_by_genre)
        else:
            st.warning("No movies found for this genre.")
