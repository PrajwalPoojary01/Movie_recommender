# 📽️ Movie Recommender System 🎬

A personalized movie recommendation web app built with **Streamlit**, powered by the **TMDb API**, and backed by **SQLite** for user management, watchlist, and viewing history.

### 🔗 Live Demo  
👉 [Click here to try the app on Streamlit Cloud](https://your-app-url.streamlit.app)

---

### ✨ Features

- 🔐 **Login & Signup** with secure user sessions  
- 🎞️ **Movie Recommendations** using content similarity  
- 🎯 **Genre Filter** for mood-based exploration  
- 📈 **Trending & Popular** movies from TMDb  
- 🧾 **Watchlist** to save movies for later  
- ✅ **History** to track watched movies  
- ℹ️ **Detail View** with poster, rating, genres, and description  
- 🧠 **Recommendations based on watch history**  
- 🎲 **“Surprise Me”** feature to explore randomly  
- 📤 **Download Watchlist & History** as PDF or CSV  
- ☁️ **Deployed on Streamlit Cloud**  

---

### 🛠️ Tech Stack

| Frontend | Backend | API | Database |
|----------|---------|-----|----------|
| Streamlit | Python | TMDb API | SQLite |

---

### 📦 Setup Instructions

#### 1. Clone the Repo

```bash
git clone https://github.com/your-username/Movie_recommender.git
cd Movie_recommender
```

#### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Add TMDb API Key

Create a file called `config.py` (or use environment variable) and add:

```python
import os
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
```

Or set it directly in Streamlit Cloud under **Secrets**.

#### 5. Run the App

```bash
streamlit run main.py
```

---

### 📁 Project Structure

```
Movie_recommender/
│
├── main.py                  # Entry point
├── config.py                # API key loader
├── db.py                    # SQLite user management
├── pages/
│   ├── 01_login.py
│   ├── 02_signup.py
│   ├── 03_recommender.py
│   ├── 04_watchlist.py
│   ├── 05_history.py
│   ├── 06_genre_filter.py
│   ├── 07_trending.py
│   ├── 08_search.py
├── utils.py                 # Reusable components (poster fetch, detail view)
├── movie_dict.pkl           # Movie metadata
├── similarity.pkl           # Precomputed similarity matrix
├── users.db                 # SQLite DB
└── requirements.txt






*Generated on June 24, 2025*
