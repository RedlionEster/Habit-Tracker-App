import sqlite3
from datetime import datetime, timedelta
from counter import Counter


def preload_db():
    db = sqlite3.connect('main.db')
    cursor = db.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS habits")
    cursor.execute("DROP TABLE IF EXISTS counters")

    # Create tables
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

    # Predefined habits with varied streaks
    predefined_habits = [
        {"name": "Exercise", "desc": "Daily exercise routine", "per": "Daily"},
        {"name": "Read", "desc": "Read a book", "per": "Daily"},
        {"name": "Meditate", "desc": "Daily meditation", "per": "Daily"},
        {"name": "Weekly Review", "desc": "Review weekly goals", "per": "Weekly"},
        {"name": "Grocery Shopping", "desc": "Weekly grocery shopping", "per": "Weekly"}
    ]

    # Predefined streaks per habit
    streaks = {
        "Exercise": 14,  # 14-day streak
        "Read": 10,  # 10-day streak
        "Meditate": 7,  # 7-day streak
        "Weekly Review": 3,  # 3-week streak
        "Grocery Shopping": 4  # 4-week streak
    }

    for habit in predefined_habits:
        counter = Counter(habit['name'], habit['desc'], habit['per'])
        counter.store(db)

        # Simulate completing the habit over time
        if habit['per'] == "Daily":
            add_habit_completions(db, counter.id, streaks[habit['name']], "days")
        elif habit['per'] == "Weekly":
            add_habit_completions(db, counter.id, streaks[habit['name']], "weeks")

    db.commit()
    db.close()


def add_habit_completions(db, habit_id, num_periods, period_type):
    cursor = db.cursor()
    last_increment_date = datetime.now() - timedelta(**{period_type: num_periods})
    for _ in range(num_periods):
        last_increment_date += timedelta(**{period_type: 1})
        cursor.execute('''UPDATE counters
                          SET count = count + 1, last_increment_date = ?, streak = streak + 1
                          WHERE habit_id = ?''', (last_increment_date.strftime("%Y-%m-%d %H:%M:%S"), habit_id))
    db.commit()


if __name__ == "__main__":
    preload_db()
