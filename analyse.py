from db import get_counter_data

def calculate_count(db, counter):
    data = get_counter_data(db, counter)
    return len(data)

def calculate_longest_streak(db, counter):
    data = get_counter_data(db, counter)
    if not data:
        return 0

    streak = 1
    longest_streak = 1
    for i in range(1, len(data)):
        if (data[i][0] - data[i-1][0]).days == 1:
            streak += 1
            if streak > longest_streak:
                longest_streak = streak
        else:
            streak = 1
    return longest_streak
