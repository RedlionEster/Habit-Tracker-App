# My Habit-Tracker-App Project

Introducing a Habit Tracking App project, created for the *Object-Oriented and Functional Programming with Python*
Course at the IU International University of Applied Sciences. 


## What is it?

This App was programmed with Python.
It's a simple Command Line Interface (CLI) App designed to track your habits. 
Follow the prompts to add and complete habits.
Create, implement, reset, delete, and monitor your habits with ease. 
Analyze your participation to see how well you're sticking to your habits.


## How to install it?

1. Download the repository from GitHub: https://github.com/RedlionEster/Habit-Tracker-App
2. Make sure you have Python 3.12+ installed on your computer.
3. Run the command to install the required libraries:


```shell
pip install -r requirements.txt
```


## Load the database:

To load the Database with 4 weeks of data for testing purposes, run:

```shell
python preload_db.py
```

## Usage:

1. Run `python main.py` to start the App.

2. Use the arrow keys on your keyboard to choose from the following options:
      
   * Create a New Habit: Add a new habit to track.  
   * Increment Habit: Mark your habit as completed for the current period.  
   * Reset Habit: Reset the progress of an existing habit.  
   * Analyse Habits: Review your habit tracking data.  
   * Delete Habit: Remove a habit from your tracking list.  
   * Exit: Leave the App.  

### Creating a New Habit
* Run the application and select "Create a New Habit".
* Enter the name of your new habit.
* Enter a description for your habit.
* Choose whether it's a Daily or Weekly habit.
* The habit will be created and stored in the database.

### Completing a Task
* Run the application and select "Increment Habit".
* Select the habit you want to increment.
* The habit's count will be incremented, and the last increment date will be updated.

### Resetting a Habit
* Run the application and select "Reset Habit".
* Select the habit you want to reset.
* The habit's count will be reset to 0.

### Analyzing Habits
1. Run the application and select "Analyse Habits".
2. Choose from the following options:

* List all habits: View a list of all currently tracked habits.
* List habits by periodicity: View habits filtered by their periodicity (Daily or Weekly).
* Longest streak of all habits: View the longest streak achieved among all habits.
* Longest streak for a habit: View the longest streak achieved for a specific habit.

### Deleting a Habit
Run the application and select "Delete Habit".
Select the habit you want to delete.
The habit will be removed from the database.

## Example Habits
The application comes with the following predefined habits:

Exercise (Daily)
Read (Daily)
Meditate (Daily)
Weekly Review (Weekly)
Grocery Shopping (Weekly)
Each habit has example tracking data for a period of 4 weeks.
   

```shell
python main.py
```


## Tests:

The `test_project.py` module is designed to automate testing of the habit tracking app's functionality, 
ensuring that the core features like creating, incrementing, resetting, and deleting habits work correctly, 
and that database operations are performed as expected.

Run the test using the following command:

```shell
python -m pytest test_project.py
```

## Note:

Note: This is a basic CLI App and can be extended with more features or implemented with a Graphic User Interface.