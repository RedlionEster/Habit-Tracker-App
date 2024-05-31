import sqlite3
from counter import Counter


def get_db():
    """
        Initialize and return the database connection.

        Returns:
        -------
        sqlite3.Connection
            The database connection.
        """
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


# Retrieve a list of all habit names from the database
def get_habits_list(db):
    cursor = db.cursor()
    cursor.execute('SELECT name FROM habits')
    rows = cursor.fetchall()
    return [row[0] for row in rows]


# Retrieve a list of habit names filtered by their periodicity
def habit_by_periodicity(db, periodicity):
    cursor = db.cursor()
    cursor.execute('SELECT name FROM habits WHERE periodicity = ?', (periodicity,))
    rows = cursor.fetchall()
    return [row[0] for row in rows]


# Retrieve a Counter object for a given habit name
def get_counter(db, name):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM habits WHERE name = ?', (name,))
    habit = cursor.fetchone()
    if habit:
        return Counter(habit[1], habit[2], habit[3], habit[0])
    else:
        return None
