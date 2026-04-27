"""
Tickets Reseller Manager is an application that let to tickets resellers to manage their tickets to events inventory.
The application allows users to add, update, show and summarize the tickets and events information.
"""

import add_data
import summary
import update_data
import show_data
import dummy_data
import delete_data
import sorting_menu
print('Welcome to Tickets Reseller Manager!') #welcome message to the user when they start the program
#load data before the menu and tell th user that the data is loading
print('loading data...')
data = dummy_data.load_data([]) #Load data from the JSON file when the program starts

while True: #while loop to keep the user in the main menu until they choose to exit the program
    print('') #spacer
    print(f'{'='*21}')
    try: #show user the main menu and try to get user input
        user_choice = int(input("""===== Main Menu =====
[1] Show Tickets / Events information
[2] Add Tickets / Events information
[3] Update Tickets / Events information
[4] Summary
[5] Delete Event
[6] Load/Save Data
[8] Sorting
[0] Exit
---------------------
Enter your choise: """))
        print('') #spacer
    except ValueError: #if user input is not a valid integer
        print('Wrong Input!!!! Please enter a valid option from the menu!')
        continue

    if user_choice == 0: #if user choose to exit the program
        print('Exit...')
        break
    elif user_choice == 1: #if user choose to show information
        show_data.menu(data)
    elif user_choice == 2: #if user choose to add information
        data = add_data.menu(data)
    elif user_choice == 3: #if user choose to update information
        data = update_data.menu(data)
    elif user_choice == 4: #if user choose to show summary
        summary.show_summary(data)
    elif user_choice == 5: #if user wants to delete an event
        delete_data.delete_event(data)
    elif user_choice == 6: #if user choose to load/save data
        data = dummy_data.menu(data)
    elif user_choice == 8: #sorting
        sorting_menu.sorting_menu(data)
    else: #if user choose an invalid option from the menu
        print('Try again. Please choose a valid option from the menu!')
