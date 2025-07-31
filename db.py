import sqlite3

def create_table():
    conn = sqlite3.connect('moodlog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS moodlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            emotion TEXT,
            text TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_log(timestamp, emotion, text):
    conn = sqlite3.connect('moodlog.db')
    c = conn.cursor()
    c.execute('INSERT INTO moodlog (timestamp, emotion, text) VALUES (?, ?, ?)', (timestamp, emotion, text))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect('moodlog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM moodlog ORDER BY timestamp DESC')
    data = c.fetchall()
    conn.close()
    return data
