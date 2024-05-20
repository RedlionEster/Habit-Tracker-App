import questionary
import sqlite3
from db import get_db, habit_by_periodicity, get_habits_list, get_counter
from counter import Counter
from analyse import calculate_count, calculate_longest_streak


def cli():
    db = get_db()
    questionary.confirm("Hi User! Welcome to your Habit Tracking App! Wanna proceed?").ask()

    stop = False

    while not stop:
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create", "Increment", "Reset", "Analyse", "Delete", "Exit"]).ask()

        if choice == "Create":  # works - delete this comment later

            # When creating a new habit
            try:
                name = questionary.text("What's the name of your new habit?").ask()
                desc = questionary.text("How do you wanna describe your habit?").ask()
                per = questionary.select(
                    "Is this a Daily or a Weekly habit?",
                    choices=["Daily", "Weekly"]).ask()
                counter = Counter(name, desc, per)
                counter.store(db)
                print(f"Habit '{name}' created!")

            except sqlite3.IntegrityError:  # Display warning if user creates an already existing habit
                print("This habit already exists.")

        elif choice == "Increment":   # works - delete this comment later
            # When incrementing an existing habit
            try:
                name = questionary.text("What's the name of the counter you want to increment?").ask()
                counter = Counter(name, "No description", "No Periodicity")
                counter.increment()
                counter.add_event(db)
                print(f"Counter '{name}' incremented!")

            # In case the habit we want to increment doesn't exist
            except ValueError:
                print("This Habit doesn't exist. You can choose Create to create a new one.")

        elif choice == "Reset":   # works - delete this comment later
            name = questionary.text("What's the name of the counter you want to reset?").ask()
            # When resetting an existing habit
            if get_counter(db, name):
                counter = Counter(name, "No description", "No Periodicity")
                counter.reset(db)
                print(f"Counter '{name}' reset to 0!")
            # In case the habit we want to reset doesn't exist
            else:
                print("This habit doesn't exist. You can't reset a non-existing Habit.")

        elif choice == "Analyse":
            analysis_choice = questionary.select("What do you want to analyse?", choices=[
                "Habit", "Periodicity", "Longest Streak"]).ask()

            if analysis_choice == "Habit":
                name = questionary.text("What habit do you want to analyse?").ask()
                count = calculate_count(db, name)
                print(f"{name} has been incremented {count} times")

            elif analysis_choice == "Periodicity":
                per = questionary.select("Select a periodicity", choices=["Daily", "Weekly"]).ask()
                name = questionary.select("Select the habit", choices=habit_by_periodicity(db, per)).ask()
                count = calculate_count(db, name)
                print(f"{name} has been incremented {count} times")

            elif analysis_choice == "Longest Streak":
                name = questionary.text("What habit do you want to analyse for the longest streak?").ask()
                streak = calculate_longest_streak(db, name)
                print(f"The longest streak for {name} is {streak} times")

        elif choice == "Delete":  # works - delete this comment later
            name = questionary.text("What's the name of the counter you want to delete?").ask()
            if get_counter(db, name):
                counter = Counter(name, "No description", "No Periodicity")
                counter.delete_habit(db)
                print(f"{name} has been deleted")
            else:
                print("This habit doesn't exist. You can't delete a non-existing Habit.")

        else:
            print("You closed the Habit Tracking App!")
            stop = True


if __name__ == '__main__':
    cli()
