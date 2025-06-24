import streamlit as st
import requests
from utils import show_movie_details, show_logout_button
import streamlit as st
API_KEY = st.secrets["TMDB_API_KEY"]


st.set_page_config(page_title="Search", layout="wide")
show_logout_button()

# 🔐 Require login
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the search feature.")
    st.stop()

# Movie display
def display_movies(movie_list):
    cols = st.columns(5)
    for i, movie in enumerate(movie_list[:15]):
        movie_id = movie.get("id")
        title = movie.get("title") or movie.get("name", "Untitled")
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Poster"

        with cols[i % 5]:
            st.image(poster_url)
            if st.button(f"ℹ️ {title}", key=f"search_{i}"):
                st.session_state.selected_movie_id = movie_id
                st.rerun()

# Search functions
def search_by_title(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
    res = requests.get(url)
    return res.json().get("results", []) if res.status_code == 200 else []

def search_person_movies(query, role):
    # Find person
    search_url = f"https://api.themoviedb.org/3/search/person?api_key={API_KEY}&query={query}"
    search_res = requests.get(search_url).json().get("results", [])
    if not search_res:
        return []

    person_id = search_res[0]["id"]
    credits_url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={API_KEY}"
    credits = requests.get(credits_url).json()

    if role == "Actor":
        return credits.get("cast", [])
    elif role == "Director":
        return [movie for movie in credits.get("crew", []) if movie.get("job") == "Director"]
    return []

# 🔍 Detail view
if st.session_state.get("selected_movie_id"):
    show_movie_details(
        movie_id=st.session_state.selected_movie_id,
        api_key=API_KEY,
        user_id=st.session_state.user_id,
        db=__import__("db")
    )
    if st.button("🔙 Back to Search"):
        st.session_state.selected_movie_id = None
        st.rerun()

# 🔎 Search UI
else:
    st.title("🔍 Search Movies")

    mode = st.selectbox("Search by", ["Title", "Actor", "Director"])
    query = st.text_input(f"Enter {mode} name")

    if query:
        with st.spinner("Searching..."):
            if mode == "Title":
                results = search_by_title(query)
            else:
                results = search_person_movies(query, mode)

        if results:
            st.markdown(f"### Showing results for **{query}**")
            display_movies(results)
        else:
            st.warning("No results found.")
