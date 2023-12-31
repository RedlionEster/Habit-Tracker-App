from db import get_counter_data
import pandas as pd


def calculate_count(db, counter):
    """
    Calculate the count of the counter
    :param db: the database
    :param counter: the counter
    :return: the count
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


def calculate_longest_streak(db, counter):
    """
    Calculate the longest streak of the counter
    :param db: sqlite3 database connection
    :param counter: name of the counter from the database
    :return: longest streak of the counter, as an integer, 0 if no streak, date of the first streak,
    date of the last streak, name of the counter
    """
    data = get_counter_data(db, counter)
    streak = 0
    longest_streak = 0
    for i in range(len(data)):
        if data[i][0] == data[i-1][0]:
            streak += 1
            if streak > longest_streak:
                longest_streak = streak
        else:
            streak = 0
    return longest_streak
