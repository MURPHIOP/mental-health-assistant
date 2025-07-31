# db.py

import sqlite3

def create_table():
    conn = sqlite3.connect('moodlogs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            emotion TEXT,
            text TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_log(timestamp, emotion, text):
    conn = sqlite3.connect('moodlogs.db')
    c = conn.cursor()
    c.execute('INSERT INTO logs (timestamp, emotion, text) VALUES (?, ?, ?)', (timestamp, emotion, text))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect('moodlogs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM logs ORDER BY id DESC')
    logs = c.fetchall()
    conn.close()
    return logs
