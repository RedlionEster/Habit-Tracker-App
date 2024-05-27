import sqlite3
from counter import Counter
from analyse import calculate_longest_streak, longest_streak_all_habits


def setup_database():
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
    return db, cursor


def test_create_habit():
    db, cursor = setup_database()
    counter = Counter("Test Habit", "This is a test habit", "Daily")
    counter.store(db)
    cursor.execute("SELECT name FROM habits WHERE name = 'Test Habit'")
    habit = cursor.fetchone()
    assert habit[0] == "Test Habit"


def test_increment_habit():
    db, cursor = setup_database()
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.increment(db)
    cursor.execute("SELECT count FROM counters WHERE habit_id = ?", (counter.id,))
    count = cursor.fetchone()
    assert count[0] == 1


def test_reset_habit():
    db, cursor = setup_database()
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.increment(db)
    counter.reset(db)
    cursor.execute("SELECT count FROM counters WHERE habit_id = ?", (counter.id,))
    count = cursor.fetchone()
    assert count[0] == 0


def test_delete_habit():
    db, cursor = setup_database()
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.delete(db)
    cursor.execute("SELECT * FROM habits WHERE name = 'Exercise'")
    habit = cursor.fetchone()
    assert habit is None


def test_calculate_longest_streak():
    db, cursor = setup_database()
    counter = Counter("Read", "Read books", "Daily")
    counter.store(db)
    counter.increment(db)
    counter.increment(db)

    counter2 = Counter("Exercise", "Daily exercise routine", "Daily")
    counter2.store(db)
    counter2.increment(db)

    streak = calculate_longest_streak(db, "Read")
    assert streak == 2

    streak2 = calculate_longest_streak(db, "Exercise")
    assert streak2 == 1


def test_longest_streak_all_habits():
    db, cursor = setup_database()
    habit1 = Counter("Read", "Read books", "Daily")
    habit1.store(db)
    habit1.increment(db)
    habit1.increment(db)

    habit2 = Counter("Exercise", "Daily exercise routine", "Daily")
    habit2.store(db)
    habit2.increment(db)

    longest_streak = longest_streak_all_habits(db)
    assert longest_streak == 2


if __name__ == "__main__":
    test_create_habit()
    test_increment_habit()
    test_reset_habit()
    test_delete_habit()
    test_calculate_longest_streak()
    test_longest_streak_all_habits()
