# db.py
import sqlite3

def create_connection():
    conn = sqlite3.connect("mood_logs.db", check_same_thread=False)
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            emotion TEXT,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_log(timestamp, emotion, text):
    conn = create_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO mood_logs (timestamp, emotion, text) VALUES (?, ?, ?)",
        (timestamp, emotion, text)
    )
    conn.commit()
    conn.close()

def get_logs():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM mood_logs ORDER BY timestamp DESC")
    logs = c.fetchall()
    conn.close()
    return logs
