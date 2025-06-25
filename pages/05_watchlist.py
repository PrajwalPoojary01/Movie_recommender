import streamlit as st
import pickle
import pandas as pd
import requests
import os
import io
from db import get_watchlist, remove_from_watchlist, clear_watchlist
from utils import show_movie_details, show_logout_button
import streamlit as st
API_KEY = st.secrets["TMDB_API_KEY"]


# ✅ Logout button in sidebar
show_logout_button()

# 🔐 Require login
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to view your watchlist.")
    st.stop()

# Load movie data
def load_pickle_from_gdrive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    return pickle.load(io.BytesIO(response.content))

# Load movie_dict.pkl from Google Drive
movie_dict_file_id = "1gKScLJTgWr-y0PG7sLDn1AjqfjRwQX9I"
movies_dict = load_pickle_from_gdrive(movie_dict_file_id)
movies = pd.DataFrame(movies_dict)

# 📦 Movie metadata
user_id = st.session_state.user_id
username = st.session_state.username
watchlist = get_watchlist(user_id)

st.title("📃 Your Watchlist")

# ✅ Movie Detail View
if st.session_state.get("selected_movie_id"):
    show_movie_details(
        movie_id=st.session_state.selected_movie_id,
        api_key=API_KEY,
        user_id=user_id,
        db=__import__("db"),
        context="watchlist"  # 🆕 pass context
    )

    if st.button("🔙 Back to Watchlist"):
        st.session_state.selected_movie_id = None
        st.rerun()

if st.session_state.get("selected_movie_id"):
    # detail view handled earlier
    pass

elif not watchlist:
    st.info("Your watchlist is currently empty.")

else:
    st.subheader("🎞️ Saved Movies")

    # 🧹 Clear button
    if st.button("🧹 Clear Watchlist"):
        clear_watchlist(user_id)
        st.success("Watchlist cleared.")
        st.rerun()

    cols = st.columns(5)
    for idx, (title, movie_id, added_at) in enumerate(watchlist):
        with cols[idx % 5]:
            try:
                movie_id_int = int.from_bytes(movie_id, byteorder='little') if isinstance(movie_id, bytes) else int(
                    movie_id)
            except Exception as e:
                st.write(f"❌ Skipping movie '{title}' due to bad movie_id: {e}")
                continue

            try:
                response = requests.get(
                    f"https://api.themoviedb.org/3/movie/{movie_id_int}?api_key={API_KEY}&language=en-US")
                data = response.json()
                poster_path = data.get("poster_path")
                poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"
            except:
                poster = "https://via.placeholder.com/300x450?text=No+Poster"

            st.image(poster)
            st.caption(f"🕒 {added_at}")

            if st.button(f"ℹ️ {title}", key=f"detail_watch_{idx}"):
                st.session_state.selected_movie_id = movie_id_int
                st.rerun()

            if st.button("❌ Remove", key=f"remove_{idx}"):
                remove_from_watchlist(user_id, title)
                st.success(f"{title} removed from watchlist.")
                st.rerun()
