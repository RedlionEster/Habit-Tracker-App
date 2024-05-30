from db import get_habits_list
from datetime import datetime


def calculate_longest_streak(db, habit_name):
    cursor = db.cursor()
    cursor.execute('''SELECT last_increment_date FROM counters 
                      INNER JOIN habits ON counters.habit_id = habits.id 
                      WHERE habits.name = ?
                      ORDER BY last_increment_date''', (habit_name,))
    increments = cursor.fetchall()

    if not increments:
        return 0

    longest_streak = 1
    current_streak = 1

    for i in range(1, len(increments)):
        if (datetime.strptime(increments[i][0], "%Y-%m-%d %H:%M:%S") - datetime.strptime(increments[i - 1][0],
                                                                                         "%Y-%m-%d %H:%M:%S")).days == 1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        elif (datetime.strptime(increments[i][0], "%Y-%m-%d %H:%M:%S") - datetime.strptime(increments[i - 1][0],
                                                                                           "%Y-%m-%d %H:%M:%S")).days > 1:
            current_streak = 1

    return longest_streak


def longest_streak_all_habits(db):
    habits = get_habits_list(db)
    longest_streak = 0
    for habit in habits:
        streak = calculate_longest_streak(db, habit)
        if streak > longest_streak:
            longest_streak = streak
    return longest_streak


def list_all_habits(db):
    cursor = db.cursor()
    cursor.execute('''SELECT name, description, periodicity, creation_date FROM habits''')
    habits = cursor.fetchall()
    return habits


def list_habits_by_periodicity(db, periodicity):
    cursor = db.cursor()
    cursor.execute('''SELECT name, description, creation_date FROM habits WHERE periodicity = ?''', (periodicity,))
    habits = cursor.fetchall()
    return habits
