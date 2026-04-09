"""
This module is for adding data to the runtime events data.
It provides a menu for the user to add tickets to existing events or to add new events.
"""

import utilitis
events_data = []

def menu(events_data):
    """
    Display the add tickets menu.
    Parameters:
        events_data (list): list of events.
    Returns:
        list: The updated events data.
    """
    while True: #while loop to keep the user in the add tickets menu until they choose to return to the main menu
        try: #show user the add tickets menu and try to get user input
            user_choice = int(input("""==== Add Tickets Menu =====
[1] Add ticket to event
[2] Add event
[0] Return to main menu
---------------------
Enter your choise: """))
            print('') #spacer
        except ValueError: #if user input is not a valid integer
            print('Wrong Input!!!! Please enter a valid option from the menu!\n')
            continue
        if user_choice == 0: #if user choose to return to main menu
            print('Return to main menu...')
            return events_data
        elif user_choice == 1: #if user choose to add ticket to event
            events_data = add_ticket_to_event(events_data)
        elif user_choice == 2: #if user choose to add new event
            events_data = add_event(events_data)
        else: #if user choose an invalid option from the menu
            print('Please choose valid option from the menu!')

def add_ticket_to_event(events_data):
    """
    Add a ticket to an existing event.
    if the event is not in the list, the user can choose to add a new event by choosing the option from the menu.
    parameters:
        events_data (list): list of events.
    Returns:
        list: The updated events data.
    """
    while True: #while loop to keep the user in the menu until they choose to return to the add tickets menu
        #call function to get the list of upcoming events and add original index for each event in the original events data list
        upcoming_events = utilitis.list_of_upcoming_events(events_data)
        print('--- Add tickets to event ---') #header
        print('Choose event:')
        #call function to print the list of upcoming events and add options for adding new event or returning to add tickets menu
        utilitis.show_events_list(upcoming_events)
        print(f'[-1] Not in the list? Add new event')
        print(f'[0] Return to add tickets menu')
        try: #try to get user input for choosing from the menu
            user_choise = int(input("Enter your choise: "))
            print('') #spacer
        except ValueError: #if user input is not a valid integer
            print('Wrong Input!!!! Try again within the valid integer range!\n')
            continue
    
        if user_choise == 0: #if user choose to return to add tickets menu
            print('Return to tickets menu...\n')
            return events_data
        elif user_choise == -1: #if user choose to add new event
            events_data = add_event(events_data)
        else: #if user choose an event from the list to add tickets to it, and try to get user input for the ticket information and add the ticket to the chosen event available tickets list
            try:
                if user_choise <= len(upcoming_events):
                    print(f'You have selected event: {upcoming_events[user_choise-1]["event"]}\n') #header for the ticket information input
                    print('Enter the ticket information:') 
                    print('(Enter -1 to cancel at anytime)') #tell user he can cancel anytime by entering -1
                    sec = input("Enter ticket\'s section: ")
                    if sec == '-1': #if user cancel
                        print('\nCancel adding ticket...\n')
                        continue
                    sn = input("Enter ticket\'s serial number: ")
                    if sn == '-1': #if user cancel
                        print('\nCancel adding ticket...\n')
                        continue
                    row = input("Enter ticket\'s row: ")
                    if row == '-1': #if user cancel
                        print('\nCancel adding ticket...\n')
                        continue
                    seat = input("Enter ticket\'s seat: ")
                    if seat == '-1': #if user cancel
                        print('\nCancel adding ticket...\n')
                        continue
                    price = float(input("Enter ticket\'s price: "))
                    if price == -1: #if user cancel
                        print('\nCancel adding ticket...\n')
                        continue
                    #get the index of the chosen event in the original events data list
                    event_indx = upcoming_events[user_choise-1]['indx']
                    if list(events_data[event_indx]['available'].keys()).count(sec) == 0: #if the section is not already exist in the available tickets dict for this event, add ticket and key (section) to the available dict
                        events_data[event_indx]['available'][sec] = [[sn, row, seat, price]]
                    else: #if the section already exist in the available tickets list and append the ticket to the section list
                        events_data[event_indx]['available'][sec].append([sn, row, seat, price])
                else: #if user choose an invalid option from the available events menu
                    print("Try again! Please choose a number from the menu!\n")
            except IndexError: #if user input is a valid integer but not in the range of the available events menu options
                print("Try again! Please choose a number from the menu!\n")
                continue
            except ValueError: #if user input for price is not a valid decimal number
                print("Wrong Input! Try again! Please enter a decimal number for the price!\n")
                continue
            print('') #spacer
            input('Ticket is successfully added! Press Enter to continue...') #wait for user input
            print('') #spacer

def add_event(events_data):
    """
    Add a new event to the events data list.
    Parameters:
        events_data (list): list of events.
    Returns:
        list: The updated events data.
    """
    print("--- Add Event ---") #header
    #ask user for new event information
    print('Enter the new event information:')
    print('(Enter -1 to cancel at anytime)') #tell user he can cancel anytime by entering -1
    event_name = input("Enter event name: ")
    if event_name == '-1': #if user cancel
        print('\nCancel adding event...\n')
        return events_data
    event_date = input("Enter event date: ")
    if event_date == '-1': #if user cancel
        print('\nCancel adding event...\n')
        return events_data
    event_venue = input("Enter event venue: ")
    if event_venue == '-1': #if user cancel
        print('\nCancel adding event...\n')
        return events_data
    #add new event information to new event dict and append it to the events data list
    events_data.append({'event': event_name, 'date': event_date, 'venue': event_venue, 'available': {}, 'sold': {}})
    print(f'\nThe event \'{event_name}\' is successfully added!\n') #print success message to user
    return events_data
