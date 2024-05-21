import sqlite3
from datetime import date


def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS counter (
        name TEXT PRIMARY KEY,
        description TEXT,
        periodicity TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        date TEXT,
        counterName TEXT,
        FOREIGN KEY (counterName) REFERENCES counter(name))""")
    db.commit()


# this function adds a counter
def add_counter(db, name, description, periodicity):
    cur = db.cursor()
    cur.execute("INSERT INTO counter VALUES (?, ?, ?)", (name, description, periodicity))
    db.commit()


# this function increments a counter
def increment_counter(db, name, event_date=None):
    if not event_date:
        event_date = str(date.today())
    cur = db.cursor()
    cur.execute("INSERT INTO tracker (date, counterName) VALUES (?, ?)", (event_date, name))
    db.commit()


# implement some error handling?
def get_counter_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT date FROM tracker WHERE counterName=?", (name,))
    return [(date.fromisoformat(row[0]),) for row in cur.fetchall()]


def habit_by_periodicity(db, periodicity):
    cur = db.cursor()
    cur.execute("SELECT name FROM counter WHERE periodicity=?", (periodicity,))
    return [row[0] for row in cur.fetchall()]


def get_habits_list(db):  # check if this part works
    cur = db.cursor()
    cur.execute("SELECT name FROM counter")
    all_habits = cur.fetchall()
    habits_set = set()
    for counters in all_habits:
        habits_set.add(counters[0])
    return list(habits_set)


def reset_counter(db, name):
    cur = db.cursor()
    cur.execute("DELETE FROM tracker WHERE counterName=?", (name,))
    db.commit()


def delete_counter(db, name):
    cur = db.cursor()
    cur.execute("DELETE FROM tracker WHERE counterName=?", (name,))
    cur.execute("DELETE FROM counter WHERE name=?", (name,))
    db.commit()


def get_counter(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM counter WHERE name=?", (name,))
    return cur.fetchone()
