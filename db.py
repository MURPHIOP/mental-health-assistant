# db.py
import sqlite3

conn = sqlite3.connect('mood_logs.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS moodlog
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  emotion TEXT,
                  text TEXT)''')
    conn.commit()

def add_log(timestamp, emotion, text):
    c.execute("INSERT INTO moodlog (timestamp, emotion, text) VALUES (?, ?, ?)",
              (timestamp, emotion, text))
    conn.commit()

def get_logs():
    c.execute("SELECT * FROM moodlog ORDER BY id DESC")
    return c.fetchall()
