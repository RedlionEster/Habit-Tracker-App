from db import get_habits_list


def calculate_longest_streak(db, habit_name):
    cursor = db.cursor()
    cursor.execute('''SELECT longest_streak FROM counters 
                      INNER JOIN habits ON counters.habit_id = habits.id 
                      WHERE habits.name = ?''', (habit_name,))
    result = cursor.fetchone()

    if not result:
        return 0

    return result[0]


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
