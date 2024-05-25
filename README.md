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

To load the Database with one month of data for testing purposes, run:

```shell
python preload_db.py
```

## Usage:

1. Run `python main.py` to start the App.

2. Use the arrow keys on your keyboard to choose from the following options:
      
   * Create: Add a new habit to track.  
   * Increment: Mark your habit as completed for the current period.  
   * Reset: Reset the progress of an existing habit.  
   * Analyse: Review your habit tracking data.  
   * Delete: Remove a habit from your tracking list.  
   * Exit: Leave the App.  
   

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