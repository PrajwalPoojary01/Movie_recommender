import sqlite3
from datetime import datetime
import os

DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Watchlist table with added_at
    c.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            user_id INTEGER,
            title TEXT,
            movie_id INTEGER,
            added_at TEXT,
            PRIMARY KEY (user_id, title),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # History table with added_at
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            user_id INTEGER,
            title TEXT,
            movie_id INTEGER,
            added_at TEXT,
            PRIMARY KEY (user_id, title),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# Call this once on app start
init_db()

# User Functions
def register_user(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Watchlist Functions
def add_to_watchlist(user_id, title, movie_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT OR REPLACE INTO watchlist (user_id, title, movie_id, added_at) VALUES (?, ?, ?, ?)",
              (user_id, title, movie_id, now))
    conn.commit()
    conn.close()

def get_watchlist(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, movie_id, added_at FROM watchlist WHERE user_id = ?", (user_id,))
    results = c.fetchall()
    conn.close()
    return results

def remove_from_watchlist(user_id, title):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM watchlist WHERE user_id = ? AND title = ?", (user_id, title))
    conn.commit()
    conn.close()

def clear_watchlist(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM watchlist WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# History Functions
def add_to_history(user_id, title, movie_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT OR REPLACE INTO history (user_id, title, movie_id, added_at) VALUES (?, ?, ?, ?)",
              (user_id, title, movie_id, now))
    conn.commit()
    conn.close()

def get_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, movie_id, added_at FROM history WHERE user_id = ?", (user_id,))
    results = c.fetchall()
    conn.close()
    return results

def clear_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
