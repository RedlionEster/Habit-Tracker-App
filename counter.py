from datetime import datetime, timedelta

class Counter:
    """
    A class to represent a habit and its associated data.

    Attributes:
    id : int
        Unique identifier for the habit.
    name : str
        Name of the habit.
    description : str
        Description of the habit.
    periodicity : str
        Periodicity of the habit (e.g., 'Daily', 'Weekly').
    creation_date : str
        The date and time when the habit was created.
    """

    def __init__(self, name, description, periodicity, id=None):
        """
        Initializes a Counter object with the given name, description, and periodicity.
        Optionally takes an id.

        Parameters:
        name : str
            The name of the habit.
        description : str
            A brief description of the habit.
        periodicity : str
            The periodicity of the habit (e.g., 'Daily', 'Weekly').
        id : int, optional
            The unique identifier for the habit (default is None).
        """
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
        cursor.execute('''INSERT INTO counters (habit_id, count, last_increment_date, streak, longest_streak)
                          VALUES (?, 0, ?, 0, 0)''', (self.id, self.creation_date))
        db.commit()

    def increment(self, db):
        cursor = db.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''SELECT last_increment_date, streak, longest_streak FROM counters WHERE habit_id = ?''', (self.id,))
        result = cursor.fetchone()
        if not result:
            print(f"No counters found for habit_id {self.id}")
            return

        last_increment_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        streak = result[1]
        longest_streak = result[2]

        if self.periodicity == "Daily":
            if (datetime.now() - last_increment_date).days == 0:
                streak += 1
            elif (datetime.now() - last_increment_date).days > 1:
                streak = 1  # Reset streak if a day is missed
        elif self.periodicity == "Weekly":
            if (datetime.now() - last_increment_date).days <= 7:
                streak += 1
            elif (datetime.now() - last_increment_date).days > 7:
                streak = 1  # Reset streak if a week is missed

        if streak > longest_streak:
            longest_streak = streak

        cursor.execute('''UPDATE counters
                          SET count = count + 1, last_increment_date = ?, streak = ?, longest_streak = ?
                          WHERE habit_id = ?''', (current_time, streak, longest_streak, self.id))
        db.commit()
        print(f"Habit '{self.name}' incremented. New streak: {streak}, Longest streak: {longest_streak}, Last increment date: {current_time}")

    def reset(self, db):
        cursor = db.cursor()
        cursor.execute('''UPDATE counters
                          SET count = 0, last_increment_date = ?, streak = 0, longest_streak = 0
                          WHERE habit_id = ?''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.id))
        db.commit()

    def delete(self, db):
        cursor = db.cursor()
        cursor.execute('''DELETE FROM counters WHERE habit_id = ?''', (self.id,))
        cursor.execute('''DELETE FROM habits WHERE id = ?''', (self.id,))
        db.commit()
