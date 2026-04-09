"""
Dummy data management for the ticket reseller application.
This module provides functions to load and save data from a JSON file.
"""

import json
from pathlib import Path

# add the path to the JSON file that will be used to store the dummy data
dir_path = Path(__file__).parent
file_path = dir_path / 'data.json'

def menu(data):
    """
    Menu and handle user input for loading and saving data.
    Parameters:
        data (dict): The existing data.
    Returns:
        dict: The updated data.
    """

    while True: #while loop to keep the user in the data menu until they choose to return to the main menu
        try: #show user the data menu and try to get user input
            user_choice = int(input("""\n==== Data Menu =====
[1] Load data
[2] Save data
[0] Return to main menu
---------------------
Enter your choice: """))

        except ValueError: #if user input is not a valid integer
            print('\nWrong Input!!!!\n')
            continue

        if user_choice == 0: #if user chooses to return to the main menu
            print('Return to main menu...')
            return data
        elif user_choice == 1: #if user chooses to load data
            data = load_data(data)
        elif user_choice == 2: #if user chooses to save data
            save_data(data)
        else: #if user input is not a valid option from the menu
            print('\nPlease choose a valid option from the menu!\n')

def load_data(old_data):
    """
    Load data from the JSON file. If the file is not found, it will return the existing data.
    Parameters:
        old_data (dict): The existing data.
    Returns:
        dict: The new data.
    """
    try: #try to load data from the JSON file
        with open(file_path, 'r') as dummy:
            new_data = json.load(dummy) #load the data from the JSON file and store it in new_data variable
            print('Data loaded successfully!')
    except FileNotFoundError: #if the JSON file is not found, print an error message and return the existing data
        print('File Not Found!')
        new_data = old_data
    return new_data

def save_data(data):
    """
    Save the data to the JSON file.
    Parameters:
        data (dict): The data to be saved.
    """
    try: #try to save the data to the JSON file
        with open(file_path, 'w') as dummy:
            json.dump(data, dummy, indent=2) #save the data to the JSON file
        print('Data saved successfully!')
    except FileNotFoundError: #if the JSON file is not found, print an error message
        print('File Not Found!')