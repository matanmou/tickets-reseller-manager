"""
This module shows the data of the events and tickets.
It provides a menu for the user to choose what data they want to see.
"""

import utilitis

def menu(events_data):
    """
    Display the show tickets menu.
    Parameters:
        events_data (list): list of events.
    """
    while True: #while loop for menu show until user choose to return to main menu
        try: #show user the show tickets menu and try to get user input
            user_choice = int(input("""==== Show Tickets Menu =====
[1] Show Upcoming Events
[2] Show Available Tickets
[3] Show All History Events
[4] Show Best Selling Events
[0] Return To Main Menu
---------------------
Enter your choise: """))
            print('') #spacer
        except ValueError: #if user input is not a valid integer.
            print('Wrong Input!!!! Please enter a valid option from the menu!')
            continue

        if user_choice == 0: #if user choose to return to main menu
            print('Return to main menu...')
            return
        elif user_choice == 1: #if user choose to show upcoming events
            show_upcoming_events(events_data)
        elif user_choice == 2: #if user choose to show all available tickets
            show_available_tickets(events_data)
        elif user_choice == 3: #if user choose to show all history events
            show_all_events(events_data)
        elif user_choice == 4: #if user choose to show best selling events
            show_best_selling_events(events_data)
        else: #if user choose an invalid option from the menu
            print('Please choose number from the menu!\n')
            continue
        input('\nPress Enter to continue...') #wait for user input before showing the menu again

def show_upcoming_events(events_data):
    """
    show the upcoming events.
    Parameters:
        events_data (list): list of events.
    """
    upcoming_events = utilitis.list_of_upcoming_events(events_data) #call the function to get the list of upcoming events
    print('--- Upcoming Events ---') #header
    utilitis.show_events_list(upcoming_events) #call the function to print the list of events

def show_available_tickets(events_data):
    """
    show the available tickets for upcoming events.
    Parameters:
        events_data (list): list of events.
    """
    upcoming_events = utilitis.list_of_upcoming_events(events_data)  #call the function to get the list of upcoming events
    for event in upcoming_events: #loop through the list of upcoming events
        print(f'\nAvailable tickets for event {event['event']}:') #header for each event
        if len(event['available']) == 0: #if there are no available tickets for this event
            print('No tickets available for this event.')
        else: #if there are available tickets for this event, loop through the sections and tickets to print them
            for sec, tickets in event['available'].items():
                print(f'Section {sec}') #header for each section
                print("-"*10)
                i = 0 #init a counter for ticket numbering
                for ticket in tickets: #loop to print each ticket
                    print(f'[{i+1}] Ticket {ticket[0]} - row: {ticket[1]}, seat: {ticket[2]}, price: {ticket[3]} NIS')
                    i += 1

def show_all_events(events_data):
    """
    show all events including history events.
    Parameters:
        events_data (list): list of events.
    """
    print('--- All Events ---') #header
    utilitis.show_events_list(events_data)  #call the function to print the list of events

def show_best_selling_events(events_data):
    """
    show the top 5 best selling events.
    Parameters:
        events_data (list): list of events.
    """
    sorted_events = utilitis.list_sorted_by_tickets_selling(events_data) #call the function to get the list of events sorted by the number of sold tickets and add counter for each event
    print('--- Best Selling Events ---') #header
    print('Top 5 events with the most sold tickets:') #header
    for i in range(5): #loop to print the top 5 events with the most sold tickets
        if i < len(sorted_events): #if there are less than 5 events
            print(f'[{i+1}] {sorted_events[i]["event"]} - Number of sold tickets: {sorted_events[i]["sold_count"]}')
        else:
            print('No more events to show...')
            break 