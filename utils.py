import requests
import streamlit as st

def show_logout_button():
    """Displays a logout button in the sidebar if the user is logged in."""
    if st.session_state.get("logged_in"):
        with st.sidebar:
            if st.button("🔒 Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_id = None
                st.session_state.selected_movie_id = None
                st.rerun()


def show_movie_details(movie_id, api_key, user_id=None, db=None, context="default"):
    """Displays full movie info: poster, title, overview, rating, genre, and action buttons."""

    # Fetch movie data
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"Failed to fetch movie details: {e}")
        return

    # Layout
    col1, col2 = st.columns([1, 2])
    with col1:
        poster_path = data.get("poster_path")
        if poster_path:
            st.image(f"https://image.tmdb.org/t/p/w500{poster_path}")
        else:
            st.image("https://via.placeholder.com/300x450?text=No+Poster")

    with col2:
        st.markdown(f"### {data.get('title', 'Unknown Title')}")
        st.markdown(f"**Rating:** ⭐ {data.get('vote_average', 'N/A')}")
        genres = ", ".join([g["name"] for g in data.get("genres", [])])
        st.markdown(f"**Genre:** 🎭 {genres or 'N/A'}")
        st.markdown("**Overview:**")
        st.write(data.get("overview", "No description available."))

        # 🔘 Action buttons
        if db and user_id:
            if context == "watchlist":
                # Show Remove and Mark as Watched
                if st.button("❌ Remove from Watchlist"):
                    db.remove_from_watchlist(user_id, data["title"])
                    st.success("Removed from watchlist.")
                    st.session_state.selected_movie_id = None
                    st.rerun()

                if st.button("✅ Mark as Watched"):
                    db.add_to_history(user_id, data["title"], movie_id)
                    st.success("Marked as watched.")

            elif context == "history":
                pass  # No buttons needed

            else:  # recommender, trending, genre
                if st.button("➕ Add to Watchlist"):
                    db.add_to_watchlist(user_id, data["title"], movie_id)
                    st.success("Added to watchlist!")

                if st.button("✅ Mark as Watched"):
                    db.add_to_history(user_id, data["title"], movie_id)
                    st.success("Marked as watched.")

    st.markdown("---")
