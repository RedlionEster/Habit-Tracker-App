import questionary
from db import get_db, habit_by_periodicity, get_habits_list, get_counter
from counter import Counter
from analyse import longest_streak_all_habits, calculate_longest_streak


# Main function that runs the CLI, providing options for the user to manage their habits
def cli():
    db = get_db()

# Greet the user after running python main.py
    while not questionary.confirm("Hi User! Welcome to your Habit Tracking App! Wanna proceed?").ask():
        pass

    stop = False

# Select what do you want to do
    while not stop:
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create a New Habit",
                     "Increment Habit",
                     "Reset Habit",
                     "Analyse Habits",
                     "Delete Habit",
                     "Exit"]).ask()

        if choice == "Create a New Habit":
            create_habit(db)
        elif choice == "Increment Habit":
            increment_habit(db)
        elif choice == "Reset Habit":
            reset_habit(db)
        elif choice == "Analyse Habits":
            analyse_habits(db)
        elif choice == "Delete Habit":
            delete_habit(db)
        elif choice == "Exit":
            stop = True


# Guides the user through the process of creating a new habit
def create_habit(db):
    name = questionary.text("What's the name of your new habit?").ask()

    if get_counter(db, name):   # error handling when creating an existing habit
        print("This habit already exists.")
    else:
        desc = questionary.text("How do you wanna describe your habit?").ask()
        per = questionary.select("Is this a Daily or a Weekly habit?", choices=["Daily", "Weekly"]).ask()
        counter = Counter(name, desc, per)
        counter.store(db)
        print(f"Habit '{name}' created!")


# Guides the user through incrementing a habit's counter
def increment_habit(db):
    habits = get_habits_list(db)
    name = questionary.select(
        "What's the name of the habit you want to increment?", choices=habits + ["Exit"]).ask()
    if name != "Exit":
        counter = get_counter(db, name)
        counter.increment(db)
        print(f"Habit '{name}' incremented!")


# Guides the user through resetting a habit's counter and streak
def reset_habit(db):
    habits = get_habits_list(db)
    name = questionary.select(
        "What's the name of the habit you want to reset?", choices=habits + ["Exit"]).ask()
    if name != "Exit":
        counter = get_counter(db, name)
        counter.reset(db)
        print(f"Habit '{name}' reset!")


# Guides the user through analyzing their habits
def analyse_habits(db):
    analysis_choice = questionary.select(
        "What analysis would you like to perform?",
        choices=["List all habits",
                 "List habits by periodicity",
                 "Longest streak of all habits",
                 "Longest streak for a habit", "Exit"]).ask()

    if analysis_choice == "List all habits":
        habits = get_habits_list(db)
        print("Currently tracked habits:")
        for habit in habits:
            print(habit)

    elif analysis_choice == "List habits by periodicity":
        periodicity = questionary.select("Select the periodicity", choices=["Daily", "Weekly"]).ask()
        habits = habit_by_periodicity(db, periodicity)
        print(f"Tracked habits with {periodicity} periodicity:")
        for habit in habits:
            print(habit)

    elif analysis_choice == "Longest streak of all habits":
        streak = longest_streak_all_habits(db)
        print(f"The longest streak of all habits is {streak}.")

    elif analysis_choice == "Longest streak for a habit":
        habits = get_habits_list(db)
        name = questionary.select("Select the habit", choices=habits + ["Exit"]).ask()
        if name != "Exit":
            streak = calculate_longest_streak(db, name)
            print(f"The longest streak for habit '{name}' is {streak}.")

    elif analysis_choice == "Exit":
        return


# Guides the user through deleting a habit
def delete_habit(db):
    habits = get_habits_list(db)
    name = questionary.select(
        "What's the name of the habit you want to delete?", choices=habits + ["Exit"]).ask()
    if name != "Exit":
        counter = get_counter(db, name)
        counter.delete(db)
        print(f"Habit '{name}' deleted!")


if __name__ == "__main__":
    cli()
