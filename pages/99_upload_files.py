import streamlit as st
import os

st.title("📤 Upload Model Files (.pkl)")

st.info("Upload `similarity.pkl` and `movie_dict.pkl` to make your app work online.")

# Upload similarity.pkl
similarity_file = st.file_uploader("Upload similarity.pkl", type=["pkl"])
if similarity_file:
    with open("similarity.pkl", "wb") as f:
        f.write(similarity_file.read())
    st.success("✅ similarity.pkl uploaded!")

# Upload movie_dict.pkl
movie_dict_file = st.file_uploader("Upload movie_dict.pkl", type=["pkl"])
if movie_dict_file:
    with open("movie_dict.pkl", "wb") as f:
        f.write(movie_dict_file.read())
    st.success("✅ movie_dict.pkl uploaded!")
