from db import get_counter_data

def calculate_count(db, counter):
    data = get_counter_data(db, counter)
    return len(data)

def calculate_average(db, counter):
    data = get_counter_data(db, counter)
    if not data:
        return 0
    total = len(data)
    days = (data[-1][0] - data[0][0]).days + 1
    return total / days