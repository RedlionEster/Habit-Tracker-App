import sqlite3
from counter import Counter


# connects to the database "main.db" and returns the connection object
def get_db():
    """
    connects to the database and returns the connection object
    :return: sqlite3 database connection
    """
    return sqlite3.connect('main.db')


# list of all habits stored in the database
def get_habits_list(db):
    """
    fetches the names of all habits from the database
    :param db: sqlite3 database
    :return: list of all habits
    """
    cursor = db.cursor()
    cursor.execute("SELECT name FROM habits")
    return [row[0] for row in cursor.fetchall()]


# returns the list of habits by periodicity (daily or weekly)
def habit_by_periodicity(db, periodicity):
    """
    fetches the names of habits from the database based on the given periodicity
    :param db: sqlite3 database
    :param periodicity: daily or weekly habit periodicity
    :return: list of habits by periodicity
    """
    cursor = db.cursor()
    cursor.execute("SELECT name FROM habits WHERE periodicity = ?", (periodicity,))
    return [row[0] for row in cursor.fetchall()]


# retrieves a specific habit from the table by it's name and returns it with data
def get_counter(db, name):
    """
    select a habit and return a Counter object with habit's data
    :param db: sqlite3 database
    :param name: the name of a habit to fetch
    :return: selected habit data or none if no habit found
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habits WHERE LOWER(name) = LOWER(?)", (name,))
    habit = cursor.fetchone()
    if habit:
        return Counter(habit[1], habit[2], habit[3], habit[0])
    return None
