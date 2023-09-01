import questionary
from db import get_db, habit_by_periodicity
from counter import Counter
from analyse import calculate_count


def main():
    db = get_db()

    stop = False

    while not stop:
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create", "Increment", "Reset", "Analyse", "Delete", "Exit"]
        ).ask()

        if choice == "Create":
            name = questionary.text("What's the name of your counter?").ask()
            desc = questionary.text("What's the description of your counter?").ask()
            per = questionary.select("What is the periodicity of you habit?", choices=["Daily", "Weekly"]).ask()
            counter = Counter(name, desc, per)
            counter.store(db)
            print(f"Counter '{name}' created!")

        elif choice == "Increment":
            name = questionary.text("What's the name of the counter you want to increment?").ask()
            counter = Counter(name, "No description", "No Periodicity")
            counter.increment()
            counter.add_event(db)
            print(f"Counter '{name}' incremented!")

        elif choice == "Reset":
            name = questionary.text("What's the name of the counter you want to reset?").ask()
            counter = Counter(name, "No description", "No Periodicity")
            counter.reset()
            print(f"Counter '{name}' reset to 0!")

        elif choice == "Analyse":
            name = questionary.select("What do you want to analyse?", choices=["Habit", "Periodicity", "Longest Streak"]).ask()  # change the text

            if name == "Habit":
                name = questionary.text("What do you want to analyse?").ask()

                count = calculate_count(db, name)
                print(f"{name} has been incremented {count} times")

            elif name == "Periodicity":
                name = questionary.select("Select a periodicity", choices=["Daily", "Weekly"]).ask()

                if name == "Daily":
                    name = questionary.select("Select the habit", choices=habit_by_periodicity(db, "Daily")).ask()
                    count = calculate_count(db, name)
                    print(f"{name} has been incremented {count} times")
                else:
                    name = questionary.select("Select the habit", choices=habit_by_periodicity(db, "Weekly")).ask()
                    count = calculate_count(db, name)
                print(f"{name} has been incremented {count} times")

            else:
                print("Streak")

        elif choice == "Delete":
            name = questionary.text("What's the name of the counter you want to delete?").ask()
            counter = Counter(name, "No description", "No Periodicity")
            counter.delete_habit(db)
            print(f"{name} has been deleted")

        else:
            print("You closed the app.")
            stop = True


if __name__ == '__main__':
    main()
