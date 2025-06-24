import streamlit as st
import requests
from utils import show_movie_details, show_logout_button
import streamlit as st
API_KEY = st.secrets["TMDB_API_KEY"]

st.set_page_config(page_title="Trending & Popular", layout="wide")
show_logout_button()

# 🔐 Require login
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to see trending movies.")
    st.stop()

# 🔍 Fetch trending movies from TMDb
def fetch_trending_movies():
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
        )
        if response.status_code == 200:
            return response.json().get("results", [])
    except:
        pass
    return []

# 🎞 Show trending posters
def display_trending(movies):
    cols = st.columns(5)
    for i, movie in enumerate(movies[:15]):  # limit to 15
        movie_id = movie["id"]
        title = movie["title"]
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"

        with cols[i % 5]:
            st.image(poster_url)
            if st.button(f"ℹ️ {title}", key=f"trend_{i}"):
                st.session_state.selected_movie_id = movie_id
                st.rerun()

# 🧠 Detail view
if st.session_state.get("selected_movie_id"):
    show_movie_details(
        movie_id=st.session_state.selected_movie_id,
        api_key=API_KEY,
        user_id=st.session_state.user_id,
        db=__import__("db")
    )
    if st.button("🔙 Back to Trending"):
        st.session_state.selected_movie_id = None
        st.rerun()

# 📈 Trending list
else:
    st.title("🔥 Trending Movies This Week")
    trending = fetch_trending_movies()

    if trending:
        display_trending(trending)
    else:
        st.warning("Couldn't load trending movies.")
