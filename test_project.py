import sqlite3
from counter import Counter


def test_create_habit():
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT
                    )''')
    cursor.execute('''CREATE TABLE counters (
                        id INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        count INTEGER,
                        last_increment_date TEXT,
                        streak INTEGER,
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    counter = Counter("Test Habit", "This is a test habit", "Daily")
    counter.store(db)
    cursor.execute("SELECT name FROM habits WHERE name = 'Test Habit'")
    habit = cursor.fetchone()
    assert habit[0] == "Test Habit"


def test_increment_habit():
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT
                    )''')
    cursor.execute('''CREATE TABLE counters (
                        id INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        count INTEGER,
                        last_increment_date TEXT,
                        streak INTEGER,
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.increment(db)
    cursor.execute("SELECT count FROM counters WHERE habit_id = ?", (counter.id,))
    count = cursor.fetchone()
    assert count[0] == 1


def test_reset_habit():
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT
                    )''')
    cursor.execute('''CREATE TABLE counters (
                        id INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        count INTEGER,
                        last_increment_date TEXT,
                        streak INTEGER,
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.increment(db)
    counter.reset(db)
    cursor.execute("SELECT count FROM counters WHERE habit_id = ?", (counter.id,))
    count = cursor.fetchone()
    assert count[0] == 0


def test_delete_habit():
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT
                    )''')
    cursor.execute('''CREATE TABLE counters (
                        id INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        count INTEGER,
                        last_increment_date TEXT,
                        streak INTEGER,
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.delete(db)
    cursor.execute("SELECT * FROM habits WHERE name = 'Exercise'")
    habit = cursor.fetchone()
    assert habit is None

if __name__ == "__main__":
    test_create_habit()
    test_increment_habit()
    test_reset_habit()
    test_delete_habit()
