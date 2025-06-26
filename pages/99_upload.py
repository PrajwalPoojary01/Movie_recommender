import streamlit as st
import os

st.set_page_config(page_title="Upload Data Files", layout="centered")
st.title("📤 Upload Required Files")
st.markdown("Upload `movie_dict.pkl` and `similarity.pkl` so they can be loaded locally.")

# Create a save location relative to app root
UPLOAD_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(UPLOAD_DIR, ".."))

uploaded_files = st.file_uploader(
    "Choose your `.pkl` files",
    type=["pkl"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        save_path = os.path.join(ROOT_DIR, file.name)
        with open(save_path, "wb") as f:
            f.write(file.read())
        st.success(f"✅ Uploaded and saved `{file.name}`")

    st.info("You're all set! You can now remove this upload page after successful upload.")
