import questionary
from db import get_db
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
            counter = Counter(name, desc)
            counter.store(db)
            print(f"Counter '{name}' created!")

        elif choice == "Increment":
            name = questionary.text("What's the name of the counter you want to increment?").ask()
            counter = Counter(name, "No description")
            counter.increment()
            counter.add_event(db)
            print(f"Counter '{name}' incremented!")

        elif choice == "Reset":
            name = questionary.text("What's the name of the counter you want to reset?").ask()
            counter = Counter(name, "No description")
            counter.reset()
            print(f"Counter '{name}' reset to 0!")

        elif choice == "Analyse":
            name = questionary.select("Do you want to analyse by Habit, Periodicity or Check the longest streak?", choices=["Habit", "Periodicity", "Logest Streak"]).ask() #change the text

            if name == "Habit":
                name = questionary.text("What do you want to analyse?").ask()

                count = calculate_count(db, name)
                print(f"{name} has been incremented {count} times")

            elif name == "Periodicity":
                print("Periodicity")

            else:
                print("Streak")

        elif choice == "Delete":
            name = questionary.text("What's the name of the counter you want to delete?").ask()
            counter = Counter(name, " ")
            counter.delete_habit(db)
            print(f"{name} has been deleted")

        else:
            print("You closed the app.")
            stop = True


if __name__ == '__main__':
    main()
