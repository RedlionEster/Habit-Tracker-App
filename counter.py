from datetime import datetime, timedelta


class Counter:
    def __init__(self, name, description, periodicity, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # this function stores the Habit in the database
    def store(self, db):
        cursor = db.cursor()
        cursor.execute('''INSERT INTO habits (name, description, periodicity, creation_date)
                          VALUES (?, ?, ?, ?)''', (self.name, self.description, self.periodicity, self.creation_date))
        db.commit()
        self.id = cursor.lastrowid
        cursor.execute('''INSERT INTO counters (habit_id, count, last_increment_date, streak)
                          VALUES (?, 0, ?, 0)''', (self.id, self.creation_date))
        db.commit()

    # this function increments the Habit's counter and updates the streak
    def increment(self, db):
        cursor = db.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''SELECT last_increment_date, streak FROM counters WHERE habit_id = ?''', (self.id,))
        result = cursor.fetchone()
        last_increment_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        streak = result[1]

        # Determine the periodicity for the habit
        if self.periodicity == "Daily":
            next_due_date = last_increment_date + timedelta(days=1)
        elif self.periodicity == "Weekly":
            next_due_date = last_increment_date + timedelta(weeks=1)
        else:
            next_due_date = last_increment_date

        # Check if the habit was missed
        if datetime.now() > next_due_date:
            streak = 1  # Reset streak if the habit was missed
        else:
            streak += 1  # Increment streak if the habit was completed in time

        cursor.execute('''UPDATE counters
                          SET count = count + 1, last_increment_date = ?, streak = ?
                          WHERE habit_id = ?''', (current_time, streak, self.id))
        db.commit()

    # this function resets the Habit's counter and streak
    def reset(self, db):
        cursor = db.cursor()
        cursor.execute('''UPDATE counters
                          SET count = 0, last_increment_date = ?, streak = 0
                          WHERE habit_id = ?''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.id))
        db.commit()

    # this function deletes the Habit from the database
    def delete(self, db):
        cursor = db.cursor()
        cursor.execute('''DELETE FROM habits WHERE id = ?''', (self.id,))
        cursor.execute('''DELETE FROM counters WHERE habit_id = ?''', (self.id,))
        db.commit()
