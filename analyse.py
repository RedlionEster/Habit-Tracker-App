from db import get_counter_data
# import pandas as pd



def calculate_count(db, counter):
    """
    Calculate the count of the counter
    :param db: sqlite3 database connection
    :param counter: name of the counter from the database
    :return: returns the number of the counter incremented events
    """
    data = get_counter_data(db, counter)
    return len(data)


def calculate_streak(db, counter):
    """
    Calculate the streak of the counter
    :param db: sqlite3 database connection
    :param counter: name of the counter from the database
    :return: streak of the counter, as an integer, 0 if no streak, date of the first streak, date of the last streak
    """
    data = get_counter_data(db, counter)
    streak = 0
    for i in range(len(data)):
        if data[i][0] == data[i-1][0]:
            streak += 1
        else:
            streak = 0
    return streak


def calculate_longest_streak(db, name):
    data = get_counter_data(db, name)
    if not data:
        return 0  # Return 0 if there is no data for the habit

    # Example logic to calculate the longest streak
    longest_streak = 0
    current_streak = 0
    for i in range(1, len(data)):
        if (data[i][0] - data[i - 1][0]).days == 1:  # assuming consecutive days for streak
            current_streak += 1
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 0
    longest_streak = max(longest_streak, current_streak)  # final check in case the longest streak is at the end

    return longest_streak
