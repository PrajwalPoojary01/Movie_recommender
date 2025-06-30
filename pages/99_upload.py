import streamlit as st

st.set_page_config(page_title="Upload Data Files", layout="centered")

st.title("📤 Upload Pickle Files")

st.markdown(
    """
Upload the following two files to use the app properly:
- `movie_dict.pkl`
- `similarity.pkl`
"""
)

# Upload movie_dict.pkl
movie_dict_file = st.file_uploader("Upload movie_dict.pkl", type="pkl", key="movie_dict")
if movie_dict_file is not None:
    with open("movie_dict.pkl", "wb") as f:
        f.write(movie_dict_file.read())
    st.success("✅ movie_dict.pkl uploaded successfully!")

# Upload similarity.pkl
similarity_file = st.file_uploader("Upload similarity.pkl", type="pkl", key="similarity")
if similarity_file is not None:
    with open("similarity.pkl", "wb") as f:
        f.write(similarity_file.read())
    st.success("✅ similarity.pkl uploaded successfully!")

# Info
if movie_dict_file and similarity_file:
    st.markdown("---")
    st.success("🎉 Both files uploaded. You can now use the app!")
