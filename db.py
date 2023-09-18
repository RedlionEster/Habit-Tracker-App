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


# creates a cursor
def add_counter(db, name, description, periodicity):
    cur = db.cursor()
    cur.execute("INSERT INTO counter VALUES (?, ?, ?)", (name, description, periodicity))
    db.commit()


def increment_counter(db, name, event_date=None):
    if not event_date:
        event_date = str(date.today())
    cur = db.cursor()
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
    db.commit()


# what if the name doesn't exist in the database? does the user get an error?
def get_counter_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE counterName=?", (name,))
    return cur.fetchall()

# continue here with this function for periodicity


def habit_by_periodicity(db, periodicity):
    cur = db.cursor()
    cur.execute("select name from counter Where periodicity=?", (periodicity,))
    counters = cur.fetchall()
    counter_list = []
    for counter in counters:
        counter_list.append(counter[0])
    return counter_list


def delete_counter(db, name):
    cur = db.cursor()
    cur.execute("DELETE from tracker WHERE counterName=?", (name,))
    cur.execute("DELETE from counter WHERE name=?", (name,))
    db.commit()