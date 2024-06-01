from db import get_db
from counter import Counter
from datetime import datetime


def preload_db():
    """
    Preload the database with predefined habits and their respective increment dates.
    """
    db = get_db()
    cursor = db.cursor()

    # Create tables if they do not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS counters (
                        id INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        increment_date TEXT,
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    db.commit()

    # Predefined habits and their respective dates
    habits = {
        "study": ["2023-07-01", "2023-07-02", "2023-07-03", "2023-07-04", "2023-07-05", "2023-07-06", "2023-07-07",
                  "2023-07-08", "2023-07-09", "2023-07-10", "2023-07-11", "2023-07-12", "2023-07-13", "2023-07-14",
                  "2023-07-15", "2023-07-16", "2023-07-17", "2023-07-18", "2023-07-19", "2023-07-20", "2023-07-21",
                  "2023-07-22", "2023-07-23", "2023-07-24", "2023-07-25", "2023-07-26", "2023-07-27", "2023-07-28",
                  "2023-07-29", "2023-07-30", "2023-07-31"],
        "read": ["2023-07-01", "2023-07-02", "2023-07-03", "2023-07-05", "2023-07-06", "2023-07-07", "2023-07-08",
                 "2023-07-09", "2023-07-10", "2023-07-11", "2023-07-12", "2023-07-14", "2023-07-15", "2023-07-16",
                 "2023-07-17", "2023-07-18", "2023-07-19", "2023-07-20", "2023-07-21", "2023-07-22", "2023-07-23",
                 "2023-07-25", "2023-07-26", "2023-07-27", "2023-07-28", "2023-07-29", "2023-07-30", "2023-07-31"],
        "gaming": ["2023-07-01", "2023-07-02", "2023-07-03", "2023-07-05", "2023-07-06", "2023-07-21", "2023-07-24",
                   "2023-07-30"],
        "sport": ["2023-07-01", "2023-07-09", "2023-07-16", "2023-07-23", "2023-07-30"],
        "laundry": ["2023-07-01", "2023-07-31"]
    }

    for habit, dates in habits.items():
        cursor.execute('SELECT id FROM habits WHERE name = ?', (habit,))
        habit_id = cursor.fetchone()
        if not habit_id:
            counter = Counter(habit, f"{habit} habit", "Daily" if habit != "laundry" else "Weekly")
            counter.store(db)
            cursor.execute('SELECT id FROM habits WHERE name = ?', (habit,))
            habit_id = cursor.fetchone()[0]
        else:
            habit_id = habit_id[0]

        for date in dates:
            current_time = datetime.strptime(date, "%Y-%m-%d")
            cursor.execute('''INSERT INTO counters (habit_id, increment_date)
                              VALUES (?, ?)''', (habit_id, current_time.strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()


preload_db()
