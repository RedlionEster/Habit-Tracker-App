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

    # Predefined habits
    predefined_habits = [
        {"name": "Exercise", "desc": "Daily exercise routine", "per": "Daily"},
        {"name": "Read", "desc": "Read a book", "per": "Daily"},
        {"name": "Meditate", "desc": "Daily meditation", "per": "Daily"},
        {"name": "Weekly Review", "desc": "Review weekly goals", "per": "Weekly"},
        {"name": "Grocery Shopping", "desc": "Weekly grocery shopping", "per": "Weekly"}
    ]

    for habit in predefined_habits:
        counter = Counter(habit['name'], habit['desc'], habit['per'])
        counter.store(db)

        # Simulate completing the habit over time
        if habit['name'] == "Exercise":
            add_habit_completions(db, counter.id, 14, "days")  # 14-day streak
        elif habit['name'] == "Read":
            add_habit_completions(db, counter.id, 5, "days")  # 5-day streak
        elif habit['name'] == "Meditate":
            add_habit_completions(db, counter.id, 7, "days")  # 7-day streak
        elif habit['name'] == "Weekly Review":
            add_habit_completions(db, counter.id, 4, "weeks")  # 4-week streak
        elif habit['name'] == "Grocery Shopping":
            add_habit_completions(db, counter.id, 2, "weeks")  # 2-week streak

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
