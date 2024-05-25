from db import get_habits_list, get_counter


def calculate_longest_streak(db, habit_name):
    cursor = db.cursor()
    cursor.execute('''SELECT streak FROM counters 
                      INNER JOIN habits ON counters.habit_id = habits.id 
                      WHERE habits.name = ?''', (habit_name,))
    streak = cursor.fetchone()
    if streak:
        return streak[0]
    return 0


def longest_streak_all_habits(db):
    habits = get_habits_list(db)
    longest_streak = 0
    for habit in habits:
        streak = calculate_longest_streak(db, habit)
        if streak > longest_streak:
            longest_streak = streak
    return longest_streak


def longest_streak_for_habit(db, habit_name):
    return calculate_longest_streak(db, habit_name)
