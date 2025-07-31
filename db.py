import sqlite3

conn = sqlite3.connect('moodlog.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS moodlogs (
                    user TEXT,
                    date TEXT,
                    emotion TEXT,
                    message TEXT
                )''')

def add_log(user, date, emotion, message):
    c.execute('INSERT INTO moodlogs (user, date, emotion, message) VALUES (?, ?, ?, ?)',
              (user, date, emotion, message))
    conn.commit()

def get_logs(user):
    c.execute('SELECT * FROM moodlogs WHERE user=? ORDER BY date DESC', (user,))
    return c.fetchall()
