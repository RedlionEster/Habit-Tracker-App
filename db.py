import sqlite3
from counter import Counter  # Add this import

def get_db():
    db = sqlite3.connect('main.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS counters (
                        id INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        increment_date TEXT,
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    db.commit()
    return db

def get_habits_list(db):
    cursor = db.cursor()
    cursor.execute('SELECT name FROM habits')
    rows = cursor.fetchall()
    return [row[0] for row in rows]

def habit_by_periodicity(db, periodicity):
    cursor = db.cursor()
    cursor.execute('SELECT name FROM habits WHERE periodicity = ?', (periodicity,))
    rows = cursor.fetchall()
    return [row[0] for row in rows]

def get_counter(db, name):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM habits WHERE name = ?', (name,))
    habit = cursor.fetchone()
    if habit:
        return Counter(habit[1], habit[2], habit[3], habit[0])
    else:
        return None
