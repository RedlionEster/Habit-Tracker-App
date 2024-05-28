from db import get_habits_list
from datetime import datetime

# this function calculates the longest streak for the chosen habit
def calculate_longest_streak(db, habit_name):
    cursor = db.cursor()
    cursor.execute('''SELECT DISTINCT last_increment_date FROM counters
                      INNER JOIN habits ON counters.habit_id = habits.id 
                      WHERE habits.name = ?
                      ORDER BY last_increment_date ASC''', (habit_name,))
    rows = cursor.fetchall()

    # print(f"Fetched rows for habit '{habit_name}': {rows}")

    if not rows:
        return 0

    # Parse dates from the database
    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in rows]
    # print(f"Parsed dates for habit '{habit_name}': {dates}")

    # Initialize streak variables
    longest_streak = 1
    current_streak = 1

    # Calculate the longest streak
    for i in range(1, len(dates)):
        # print(f"Checking dates: {dates[i - 1]} and {dates[i]}")
        if (dates[i] - dates[i - 1]).days == 1:
            current_streak += 1
            # print(f"Current streak incremented: {current_streak}")
        else:
            longest_streak = max(longest_streak, current_streak)
            # print(f"New longest streak found: {longest_streak}")
            current_streak = 1

    # Final check at the end of the loop
    longest_streak = max(longest_streak, current_streak)
    # print(f"Final longest streak: {longest_streak}")

    return longest_streak


# this function calculates the longest streak from all habits
def longest_streak_all_habits(db):
    habits = get_habits_list(db)
    longest_streak = 0
    for habit in habits:
        streak = calculate_longest_streak(db, habit)
        if streak > longest_streak:
            longest_streak = streak
    return longest_streak
