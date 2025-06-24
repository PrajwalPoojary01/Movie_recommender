import streamlit as st
import pickle
import pandas as pd
import requests
from utils import show_movie_details, show_logout_button
from db import get_history
import streamlit as st
API_KEY = st.secrets["TMDB_API_KEY"]


st.set_page_config(page_title="Recommender", layout="wide")
show_logout_button()

# 🔐 Block if not logged in
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the recommender.")
    st.stop()

# Load movie data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Initialize state
if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None
if "recommended" not in st.session_state:
    st.session_state.recommended = False

# 📦 Poster fetch
def fetch_poster_path(movie_id):
    try:
        res = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
        if res.status_code == 200:
            return res.json().get("poster_path", "")
    except:
        pass
    return ""

# 🎯 Recommend based on selected movie
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6]

    titles, ids, posters = [], [], []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster_path = fetch_poster_path(movie_id)
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"
        titles.append(title)
        ids.append(movie_id)
        posters.append(poster_url)
    return titles, posters, ids

# 🧠 Recommend based on user's watch history
def recommend_from_history(user_id):
    watched = get_history(user_id)
    if not watched:
        return [], [], []

    recommended_scores = {}
    watched_titles = [w[0] for w in watched]
    watched_ids = [int.from_bytes(w[1], 'little') if isinstance(w[1], bytes) else int(w[1]) for w in watched]

    for title, movie_id in zip(watched_titles, watched_ids):
        movie_row = movies[movies["title"] == title]
        if not movie_row.empty:
            idx = movie_row.index[0]
            scores = list(enumerate(similarity[idx]))
            for i, score in scores:
                recommended_id = movies.iloc[i].movie_id
                if recommended_id in watched_ids:
                    continue
                recommended_scores[recommended_id] = recommended_scores.get(recommended_id, 0) + score

    sorted_recs = sorted(recommended_scores.items(), key=lambda x: x[1], reverse=True)
    sorted_recs = sorted_recs[:5]

    titles, ids, posters = [], [], []
    for movie_id, _ in sorted_recs:
        row = movies[movies["movie_id"] == movie_id]
        if not row.empty:
            title = row.iloc[0].title
            poster_path = fetch_poster_path(movie_id)
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"
            titles.append(title)
            ids.append(movie_id)
            posters.append(poster_url)
    return titles, posters, ids

# 📽️ Detail View
if st.session_state.selected_movie_id:
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

    selected_movie = st.selectbox("Choose a movie:", movies["title"].values)

    col_rec, col_surprise = st.columns([1, 1])

    with col_rec:
        if st.button("🎯 Show Recommendation"):
            st.session_state.recommended = True

    with col_surprise:
        if st.button("🎲 Surprise Me"):
            random_movie_id = movies.sample(1).iloc[0]["movie_id"]
            st.session_state.selected_movie_id = int(random_movie_id)
            st.rerun()

    if st.session_state.recommended:
        titles, posters, ids = recommend(selected_movie)
        st.subheader("🎯 Top Recommendations")
        cols = st.columns(5)
        for i in range(len(titles)):
            with cols[i]:
                st.image(posters[i])
                if st.button(f"ℹ️ {titles[i]}", key=f"rec_{i}"):
                    st.session_state.selected_movie_id = ids[i]
                    st.rerun()

        # 📈 Personalized Section
        hist_titles, hist_posters, hist_ids = recommend_from_history(st.session_state.user_id)
        if hist_titles:
            st.markdown("---")
            st.subheader("🧠 Because you watched:")
            cols = st.columns(5)
            for i in range(len(hist_titles)):
                with cols[i]:
                    st.image(hist_posters[i])
                    if st.button(f"ℹ️ {hist_titles[i]}", key=f"histrec_{i}"):
                        st.session_state.selected_movie_id = hist_ids[i]
                        st.rerun()
