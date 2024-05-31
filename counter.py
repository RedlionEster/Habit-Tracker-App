from datetime import datetime


class Counter:
    def __init__(self, name, description, periodicity, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def store(self, db):
        cursor = db.cursor()
        cursor.execute('''INSERT INTO habits (name, description, periodicity, creation_date)
                          VALUES (?, ?, ?, ?)''', (self.name, self.description, self.periodicity, self.creation_date))
        db.commit()
        self.id = cursor.lastrowid

    def increment(self, db, increment_date=None):
        cursor = db.cursor()
        if increment_date is None:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            current_time = increment_date.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''INSERT INTO counters (habit_id, increment_date)
                          VALUES (?, ?)''', (self.id, current_time))
        db.commit()

    def reset(self, db):
        cursor = db.cursor()
        cursor.execute('''DELETE FROM counters WHERE habit_id = ?''', (self.id,))
        db.commit()

    def delete(self, db):
        cursor = db.cursor()
        cursor.execute('''DELETE FROM habits WHERE id = ?''', (self.id,))
        cursor.execute('''DELETE FROM counters WHERE habit_id = ?''', (self.id,))
        db.commit()
