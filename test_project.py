import sqlite3
from counter import Counter
from analyse import calculate_longest_streak

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
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.increment(db)
    cursor.execute("SELECT count FROM counters WHERE habit_id = ?", (counter.id,))
    count = cursor.fetchone()
    assert count[0] == 1

def test_calculate_longest_streak():
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
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    for _ in range(5):
        counter.increment(db)
    streak = calculate_longest_streak(db, "Exercise")
    assert streak == 5
