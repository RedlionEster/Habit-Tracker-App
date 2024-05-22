import questionary
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
            choices=["Create", "Increment", "Reset", "Analyse", "Delete", "Exit"]
        ).ask()

        if choice == "Create":  # When creating a new habit # works - delete this comment later

            habit_created = False

            try:
                name = questionary.text("What's the name of your new habit?").ask()  # type the counter name

                # Check if the habit already exists
                if get_counter(db, name):
                    print("This habit already exists.")
                else:
                    # Only ask for description and periodicity if the habit does not exist
                    desc = questionary.text("How do you wanna describe your habit?").ask()  # counter description
                    per = questionary.select(
                        "Is this a Daily or a Weekly habit?",
                        choices=["Daily", "Weekly"]
                    ).ask()

                    counter = Counter(name, desc, per)
                    counter.store(db)
                    print(f"Habit '{name}' created!")
                    habit_created = True

            finally:
                if habit_created:
                    print("Create habit process completed.")



        elif choice == "Increment":   # When incrementing an existing habit # it works - delete this comment later

            habits = get_habits_list(db)
            habits = [habit for habit in habits if habit != "exit"]
            habits.sort()  # Sort the list of habits
            habits.append("Exit")  # Ensure 'exit' is always at the bottom

            name = questionary.select(
                message="What's the name of the habit you want to increment?",
                choices=habits
            ).ask()

            if name == "Exit":
                print("Exiting increment process.")

            else:
                counter = Counter(name, description="No description", periodicity="No Periodicity")
                counter.increment()
                counter.add_event(db)
                print(f"Counter '{name}' incremented!")


        elif choice == "Reset": # When resetting an existing habit  # it works - delete this comment later

            habits = get_habits_list(db)
            habits = [habit for habit in habits if habit != "exit"]
            habits.sort()  # Sort the list of habits
            habits.append("Exit")  # Ensure 'Exit' is always at the bottom

            name = questionary.select(
                message="What's the name of the counter you want to reset?",
                choices=habits).ask()

            if name == "Exit":
                print("Exiting reset process.")

            else:
                counter = Counter(name, description="No description", periodicity="No Periodicity")
                counter.reset(db)
                print(f"Counter '{name}' reset to 0!")


        elif choice == "Analyse":
            analysis_choice = questionary.select("What do you want to analyse?", choices=[
                "Habit", "Periodicity", "Longest Streak"]).ask()

            if analysis_choice == "Habit":  # works - delete this comment later
                name = questionary.text("What habit do you want to analyse?").ask()
                count = calculate_count(db, name)

                if count is None or count == 0:
                    print(f"The habit '{name}' does not exist or has no increments recorded.")
                else:
                    print(f"{name} has been incremented {count} times")

            elif analysis_choice == "Periodicity":  # works - delete this comment later
                per = questionary.select("Select a periodicity", choices=["Daily", "Weekly"]).ask()
                name = questionary.select("Select the habit", choices=habit_by_periodicity(db, per)).ask()
                count = calculate_count(db, name)
                print(f"{name} has been incremented {count} times")

            elif analysis_choice == "Longest Streak":
                name = questionary.text("What habit do you want to analyse for the longest streak?").ask()
                streak = calculate_longest_streak(db, name)
                print(f"The longest streak for {name} is {streak} times")

        elif choice == "Delete":  # When deleting an existing habit  # works - delete this comment later

            habits = get_habits_list(db)
            habits = [habit for habit in habits if habit != "exit"]
            habits.sort()  # Sort the list of habits
            habits.append("Exit")  # Ensure 'Exit' is always at the bottom

            name = questionary.select(
                message="What's the name of the counter you want to delete?",
                choices=habits).ask()

            if name == "Exit":
                print("Exiting delete process.")
            else:
                counter = Counter(name, description="No description", periodicity="No Periodicity")
                counter.delete_habit(db)
                print(f"Counter '{name}' has been deleted")

        else:
            print("You closed the Habit Tracking App!")
            stop = True


if __name__ == '__main__':
    cli()
