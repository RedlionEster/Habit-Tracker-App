import sqlite3
from counter import Counter

def get_db():
    return sqlite3.connect('main.db')

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
    cursor.execute("SELECT * FROM habits WHERE name = ?", (name,))
    habit = cursor.fetchone()
    if habit:
        return Counter(habit[1], habit[2], habit[3], habit[0])
    return None
