from db import add_counter, increment_counter, delete_counter, reset_counter


class Counter:
    def __init__(self, name: str, description: str, periodicity: str):
        """Counter class to count events
        :param name: the name of the counter
        :param description: the description of the counter
        :param periodicity: the periodicity of the counter
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.count = 0

    def increment(self):
        """
        Increments the counter by one.
        """
        self.count += 1

    def reset(self, db):
        """
        Resets the counter to zero and updates the database
        :param db: the database instance
        """
        self.count = 0
        reset_counter(db, self.name)

    def __str__(self):
        """
        Returns a string representation of the counter.
        :return: A string showing the name and current count of the counter
        """
        return f"{self.name}: {self.count}"

    def store(self, db):
        """
        Stores the counter information in the database.
        :param db: the database instance
        """
        add_counter(db, self.name, self.description, self.periodicity)

    def add_event(self, db, date: str = None):
        """
        Adds an event to the counter and updates the database.
        :param db: the database instance
        :param date: the date of the event
        """
        increment_counter(db, self.name, date)

    def delete_habit(self, db):
        """
        Deletes the habit from the database.
        :param db: the database instance
        """
        delete_counter(db, self.name)


# just temporary code to test the counter locally - comment out or delete later
# counter = Counter("test name", "test description", "test periodicity")
# counter.increment()
# print(counter)
