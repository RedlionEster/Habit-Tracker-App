from counter import Counter
from db import get_db, get_counter, habit_by_periodicity, get_habits_list
from analyse import calculate_count, calculate_streak, calculate_longest_streak
import os
from datetime import datetime


def get_counter_data(db, name):
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM counters
                      JOIN habits ON counters.habit_id = habits.id
                      WHERE habits.name = ?''', (name,))
    return cursor.fetchall()


def get_periodicity(db, name):
    cursor = db.cursor()
    cursor.execute('''SELECT periodicity FROM habits WHERE name = ?''', (name,))
    return cursor.fetchone()[0]


def single_habit_cut_list(db, name):
    cursor = db.cursor()
    cursor.execute('''SELECT last_increment_date FROM counters
                      JOIN habits ON counters.habit_id = habits.id
                      WHERE habits.name = ?''', (name,))
    return [row[0] for row in cursor.fetchall()]


def get_countername_list(db):
    cursor = db.cursor()
    cursor.execute('''SELECT name FROM habits''')
    return [row[0] for row in cursor.fetchall()]


class TestCounter:

    def setup_method(self):
        self.db = get_db("test.db")

        cursor = self.db.cursor()
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
                            count INTEGER,
                            last_increment_date TEXT,
                            streak INTEGER,
                            FOREIGN KEY (habit_id) REFERENCES habits (id)
                        )''')
        self.db.commit()

        # Predefined habit for testing
        self.counter = Counter("test_counter", "Test habit", "Daily")
        self.counter.store(self.db)
        self.dates = ["2023-07-01", "2023-07-02", "2023-07-03", "2023-07-04"]

        for date in self.dates:
            current_time = datetime.strptime(date, "%Y-%m-%d")
            cursor.execute('''UPDATE counters
                              SET count = count + 1, last_increment_date = ?, streak = ?
                              WHERE habit_id = ?''',
                           (current_time.strftime("%Y-%m-%d %H:%M:%S"), self.dates.index(date) + 1, self.counter.id))
            self.db.commit()

    def test_counter(self):
        counter = Counter("test_counter_1", "test_description_1", "Daily")
        counter.store(self.db)
        counter.increment(self.db)
        counter.reset(self.db)
        counter.increment(self.db)
        counter.delete(self.db)

    def test_db_counter(self):
        data = get_counter_data(self.db, "test_counter")
        assert len(data) == 4

        count = calculate_count(self.db, "test_counter")
        assert count == 4

    def test_streak(self):
        periodicity = get_periodicity(self.db, "test_counter")
        assert periodicity == "Daily"

        dates = single_habit_cut_list(self.db, "test_counter")
        assert len(dates) == 4

        streak = calculate_streak(self.db, "test_counter")
        assert len(streak) == 4

        countername_list = get_countername_list(self.db)
        assert len(countername_list) == 1

        longest_streak = calculate_longest_streak(self.db)
        assert len(longest_streak) == 4

    def teardown_method(self):
        self.db.close()
        os.remove("test.db")


# Ensure the tests are executed
if __name__ == "__main__":
    test = TestCounter()
    test.setup_method()
    test.test_counter()
    test.test_db_counter()
    test.test_streak()
    test.teardown_method()
