# My Habit-Tracker-App Project

Introducing a Habit Tracking App project, created for the "Object-Oriented and Functional Programming with Python"
course at the IU International University of Applied Sciences. 


## What is it?

This is a simple Command Line Interface (CLI) App designed to track your habits. 
Follow the prompts to add and complete habits.
Create, implement, reset, delete, and monitor your habits with ease. 
Analyze your participation to see how well you're sticking to your habits.


## Installation

1. Download the repository from GitHub: https://github.com/RedlionEster/Habit-Tracker-App
2. Make sure you have Python 3.12+ installed on your computer.
3. Run the command to install the required libraries:


```shell
pip install -r requirements.txt
```


## Load the database:

Run the command to load the Database with 1 month of data:

```shell
python preload_db.py
```

## Usage:

1. Run `python main.py` to start the app.
2. Choose options to create, reset, analyse, delete and complete (increment) your habits,
   using the arrow keys on your keyboard.

```shell
python main.py
```


## Tests:

The `test_project.py` module is designed to automate testing of the habit tracking app's functionality, 
ensuring that the core features like creating, incrementing, resetting, and deleting habits work correctly, 
and that database operations are performed as expected.

Run the test using the following command:

```shell
pytest .
```

## Note:

Note: This is a basic example and can be extended with more features or implemented with a Graphic User Interface.