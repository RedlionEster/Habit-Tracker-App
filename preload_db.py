from db import get_db, add_counter, increment_counter


def preload_db():
    db = get_db()

    add_counter(db, "run", "sport", "daily")
    for day in range(1, 31):
        increment_counter(db, "run", f"2023-08-{day:02d}")

    add_counter(db, "eat", "food", "weekly")
    for day in range(1, 31):
        increment_counter(db, "eat", f"2023-08-{day:02d}")

    return db
