import sqlite3

def create_table():
    conn = sqlite3.connect("mood.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS moodlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            date TEXT,
            emotion TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_log(date, emotion, message, user):
    conn = sqlite3.connect("mood.db")
    c = conn.cursor()
    c.execute("INSERT INTO moodlog (user, date, emotion, message) VALUES (?, ?, ?, ?)",
              (user, date, emotion, message))
    conn.commit()
    conn.close()

def get_logs(user):
    conn = sqlite3.connect("mood.db")
    c = conn.cursor()
    c.execute("SELECT * FROM moodlog WHERE user = ?", (user,))
    data = c.fetchall()
    conn.close()
    return data
