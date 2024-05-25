import sqlite3
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

    db.commit()
    db.close()


if __name__ == "__main__":
    preload_db()
