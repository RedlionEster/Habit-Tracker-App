import sqlite3
from datetime import datetime, timedelta
from counter import Counter
from analyse import calculate_longest_streak, longest_streak_all_habits
from db import get_habits_list, habit_by_periodicity, get_counter


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
                        increment_date TEXT,
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    return db


def test_create_habit():
    db = setup_database()
    counter = Counter("Test Habit", "This is a test habit", "Daily")
    counter.store(db)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM habits WHERE name = 'Test Habit'")
    habit = cursor.fetchone()
    assert habit is not None
    assert habit[0] == "Test Habit"


def test_increment_habit():
    db = setup_database()
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.increment(db)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM counters WHERE habit_id = ?", (counter.id,))
    count = cursor.fetchone()[0]
    assert count == 1


def test_reset_habit():
    db = setup_database()
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.increment(db)
    counter.reset(db)
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM counters WHERE habit_id = ?", (counter.id,))
    count = cursor.fetchone()[0]
    assert count == 0


def test_delete_habit():
    db = setup_database()
    counter = Counter("Exercise", "Daily exercise routine", "Daily")
    counter.store(db)
    counter.delete(db)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM habits WHERE name = 'Exercise'")
    habit = cursor.fetchone()
    assert habit is None


def test_calculate_longest_streak():
    db = setup_database()
    counter = Counter("Read", "Read books", "Daily")
    counter.store(db)

    # Manually insert different dates for increments
    increment_date1 = datetime.now() - timedelta(days=2)
    increment_date2 = datetime.now() - timedelta(days=1)
    cursor = db.cursor()
    cursor.execute('''INSERT INTO counters (habit_id, increment_date)
                      VALUES (?, ?)''', (counter.id, increment_date1.strftime("%Y-%m-%d %H:%M:%S")))
    cursor.execute('''INSERT INTO counters (habit_id, increment_date)
                      VALUES (?, ?)''', (counter.id, increment_date2.strftime("%Y-%m-%d %H:%M:%S")))
    db.commit()

    counter2 = Counter("Exercise", "Daily exercise routine", "Daily")
    counter2.store(db)
    counter2.increment(db)

    # Add debugging information
    cursor.execute("SELECT * FROM counters WHERE habit_id = ?", (counter.id,))
    read_counters = cursor.fetchall()
    print(f"Counters for 'Read': {read_counters}")

    cursor.execute("SELECT * FROM counters WHERE habit_id = ?", (counter2.id,))
    exercise_counters = cursor.fetchall()
    print(f"Counters for 'Exercise': {exercise_counters}")

    streak = calculate_longest_streak(db, "Read")
    print(f"Calculated streak for 'Read': {streak}")
    assert streak == 2

    streak2 = calculate_longest_streak(db, "Exercise")
    print(f"Calculated streak for 'Exercise': {streak2}")
    assert streak2 == 1


def test_longest_streak_all_habits():
    db = setup_database()
    habit1 = Counter("Read", "Read books", "Daily")
    habit1.store(db)

    # Manually insert different dates for increments
    increment_date1 = datetime.now() - timedelta(days=2)
    increment_date2 = datetime.now() - timedelta(days=1)
    cursor = db.cursor()
    cursor.execute('''INSERT INTO counters (habit_id, increment_date)
                      VALUES (?, ?)''', (habit1.id, increment_date1.strftime("%Y-%m-%d %H:%M:%S")))
    cursor.execute('''INSERT INTO counters (habit_id, increment_date)
                      VALUES (?, ?)''', (habit1.id, increment_date2.strftime("%Y-%m-%d %H:%M:%S")))
    db.commit()

    habit2 = Counter("Exercise", "Daily exercise routine", "Daily")
    habit2.store(db)
    habit2.increment(db)

    longest_streak = longest_streak_all_habits(db)
    assert longest_streak == 2


def test_get_habits_list():
    db = setup_database()
    counter = Counter("Test Habit", "This is a test habit", "Daily")
    counter.store(db)
    habits = get_habits_list(db)
    assert "Test Habit" in habits


def test_habit_by_periodicity():
    db = setup_database()
    daily_habit = Counter("Daily Habit", "Daily habit description", "Daily")
    daily_habit.store(db)
    weekly_habit = Counter("Weekly Habit", "Weekly habit description", "Weekly")
    weekly_habit.store(db)
    daily_habits = habit_by_periodicity(db, "Daily")
    weekly_habits = habit_by_periodicity(db, "Weekly")
    assert "Daily Habit" in daily_habits
    assert "Weekly Habit" in weekly_habits


def test_get_counter():
    db = setup_database()
    counter = Counter("Test Habit", "This is a test habit", "Daily")
    counter.store(db)
    fetched_counter = get_counter(db, "Test Habit")
    assert fetched_counter is not None
    assert fetched_counter.name == "Test Habit"


if __name__ == "__main__":
    test_create_habit()
    test_increment_habit()
    test_reset_habit()
    test_delete_habit()
    test_calculate_longest_streak()
    test_longest_streak_all_habits()
    test_get_habits_list()
    test_habit_by_periodicity()
    test_get_counter()
    print("All tests passed!")
