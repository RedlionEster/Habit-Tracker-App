import sqlite3
from datetime import datetime, timedelta

def create_tables(db):
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
                        count INTEGER,
                        last_increment_date TEXT,
                        streak INTEGER,
                        longest_streak INTEGER DEFAULT 0,
                        FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
                    )''')
    db.commit()

def preload_db():
    db = sqlite3.connect('main.db')
    create_tables(db)
    cursor = db.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM counters")
    cursor.execute("DELETE FROM habits")
    db.commit()

    # Predefined habits with creation and increment dates
    predefined_habits = [
        {
            "name": "Exercise",
            "description": "Daily exercise routine",
            "periodicity": "Daily",
            "creation_date": "2023-01-01 00:00:00",
            "increments": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06",
                           "2023-01-07"]
        },
        {
            "name": "Read",
            "description": "Read a book",
            "periodicity": "Daily",
            "creation_date": "2023-01-01 00:00:00",
            "increments": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"]
        },
        {
            "name": "Meditate",
            "description": "Daily meditation",
            "periodicity": "Daily",
            "creation_date": "2023-01-01 00:00:00",
            "increments": ["2023-01-01", "2023-01-02", "2023-01-03"]
        },
        {
            "name": "Weekly Review",
            "description": "Review weekly goals",
            "periodicity": "Weekly",
            "creation_date": "2023-01-01 00:00:00",
            "increments": ["2023-01-07", "2023-01-14", "2023-01-21"]
        },
        {
            "name": "Grocery Shopping",
            "description": "Weekly grocery shopping",
            "periodicity": "Weekly",
            "creation_date": "2023-01-01 00:00:00",
            "increments": ["2023-01-07", "2023-01-14", "2023-01-21", "2023-01-28"]
        }
    ]

    for habit in predefined_habits:
        cursor.execute('''INSERT INTO habits (name, description, periodicity, creation_date)
                          VALUES (?, ?, ?, ?)''', (habit['name'], habit['description'], habit['periodicity'], habit['creation_date']))
        habit_id = cursor.lastrowid

        for increment_date in habit['increments']:
            cursor.execute('''INSERT INTO counters (habit_id, count, last_increment_date, streak, longest_streak)
                              VALUES (?, 1, ?, 1, 1)''', (habit_id, increment_date + " 00:00:00"))

    db.commit()
    db.close()

if __name__ == "__main__":
    preload_db()
