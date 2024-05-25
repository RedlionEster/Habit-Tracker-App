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
        cursor.execute('''INSERT INTO counters (habit_id, count, last_increment_date)
                          VALUES (?, 0, ?)''', (self.id, self.creation_date))
        db.commit()

    def increment(self, db):
        cursor = db.cursor()
        cursor.execute('''UPDATE counters
                          SET count = count + 1, last_increment_date = ?
                          WHERE habit_id = ?''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.id))
        db.commit()

    def reset(self, db):
        cursor = db.cursor()
        cursor.execute('''UPDATE counters
                          SET count = 0, last_increment_date = ?
                          WHERE habit_id = ?''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.id))
        db.commit()

    def delete(self, db):
        cursor = db.cursor()
        cursor.execute('''DELETE FROM habits WHERE id = ?''', (self.id,))
        cursor.execute('''DELETE FROM counters WHERE habit_id = ?''', (self.id,))
        db.commit()
