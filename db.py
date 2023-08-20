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
        description TEXT)""")

    #add periodicity

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        date TEXT,
        counterName TEXT,
        FOREIGN KEY (counterName) REFERENCES counter(name))""")


    db.commit()


def add_counter(db, name, description):
    cur = db.cursor()
    cur.execute("INSERT INTO counter VALUES (?, ?)", (name, description))
    db.commit()


def increment_counter(db, name, event_date=None):
    if not event_date:
        event_date = str(date.today())
    cur = db.cursor()
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
    db.commit()


def get_counter_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE counterName=?", (name,))
    return cur.fetchall()


def delete_counter(db, name):
    cur = db.cursor()
    cur.execute("DELETE from tracker WHERE counterName=?", (name,))
    cur.execute("DELETE from counter WHERE name=?", (name,))
    db.commit()

# something to load the database for 4 weeks of data
# preload db.py