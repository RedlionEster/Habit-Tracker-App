import sqlite3
from counter import Counter

def get_db():
    db = sqlite3.connect('main.db')
    create_tables(db)
    return db

def create_tables(db):
    cursor = db.cursor()

    # Create tables if they don't exist
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
                        count INTEGER,
                        last_increment_date TEXT,
                        streak INTEGER,
                        FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
                    )''')
    db.commit()

def habit_by_periodicity(db, periodicity):
    cursor = db.cursor()
    cursor.execute("SELECT name FROM habits WHERE periodicity = ?", (periodicity,))
    return [row[0] for row in cursor.fetchall()]

def get_habits_list(db):
    cursor = db.cursor()
    cursor.execute("SELECT name FROM habits")
    return [row[0] for row in cursor.fetchall()]

def get_counter(db, name):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habits WHERE LOWER(name) = LOWER(?)", (name,))
    habit = cursor.fetchone()
    if habit:
        return Counter(habit[1], habit[2], habit[3], habit[0])
    return None

def delete_habit(db, name):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM habits WHERE name = ?", (name,))
    habit_id = cursor.fetchone()
    if habit_id:
        cursor.execute("DELETE FROM counters WHERE habit_id = ?", (habit_id[0],))
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id[0],))
        db.commit()
