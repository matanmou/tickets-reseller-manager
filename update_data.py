"""
This module is for updating the data of the events and tickets.
It provides a menu for the user to update the tickets of an event or to update the information of an event.
"""

import utilitis

def menu(events_data):
    """
    Display the update tickets menu.
    Parameters:
        events_data (list): list of events.
    Returns:
        list: The updated events data.
    """
    while True: #while loop to keep the user in the update tickets menu until they choose to return to the main menu
        try: #show user the update tickets menu and try to get user input
            user_choice = int(input("""==== Update Tickets Menu =====
[1] Update Event Tickets
[2] Update Event Information
[0] Return To Main Menu
---------------------
Enter your choise: """))
            print('') #spacer 
        except ValueError: #if user input is not a valid integer
            print('Wrong Input!!!! Please enter an valid option from the menu!\n')
            continue

        if user_choice == 0: #if user choose to return to main menu
            print('Return to main menu...')
            return events_data
        elif user_choice == 1: #if user choose to update event tickets
            update_event_tickets(events_data)
        elif user_choice == 2: #if user choose to update event information
            update_event_information(events_data)
        else:
            print('Please choose valid option from the menu!\n')

def update_event_tickets(events_data):
    """
    Update the tickets of an event.
    Parameters:
        events_data (list): list of events.
    Returns:
        list: The updated events data.
    """
    upcoming_events = utilitis.list_of_upcoming_events(events_data) #call function to get the list of upcoming events and add original index for each event in the original events data list
    while True: #while loop to keep the user in the menu until they choose to return to the update tickets menu
        print('--- Update Event Tickets ---') #header for the update event tickets menu
        print('Upcoming Events:')
        utilitis.show_events_list(upcoming_events) #call function to print the list of upcoming events
        print(f'[0] Return to add tickets menu')
        try: #try to get user input for choosing from the menu
            user_choise = int(input("Enter your choise: "))
        except ValueError: #if user input is not a valid integer
            print('\nWrong Input!!!! Please enter a valid option from the menu!\n')
            continue
        if user_choise == 0: #if user choose to return to add tickets menu
            print('Return to add tickets menu...\n')
            return events_data
        elif user_choise <= len(upcoming_events) and user_choise > 0: #if user choose a valid event from the list
            event = upcoming_events[user_choise - 1] #assign the chosen event to a variable for easier access
            print(f'\nYou have selected event: {event["event"]}') #header for the ticket information input
            user_choise = input("Do you want to sold or unsoled tickets? (sold/unsold/cancel): ").lower()
            if user_choise == 'unsold': #if user choose to unsold, show all sold tickets to user
                sold_tickets = event['sold'] #assign for convenience
                if len(sold_tickets) == 0: #i there are no sold tickets for this event
                    print('No sold tickets for this event.')
                else:
                    print('--- Sold Tickets ---')
                    for sec, tickets in event['sold'].items():
                        print(f'Section {sec}')
                        print("-"*10)
                        i = 0
                        for ticket in tickets:
                            print(f'[{i+1}] Ticket {ticket[0]} - row: {ticket[1]}, seat: {ticket[2]}, price: {ticket[3]} NIS')
                            i += 1
                    try: #try to get user input for choosing the section
                        sec_choise = input("Enter the section of the ticket you want to unsold: ")
                        if sec_choise == '0': #if user choose to cancel
                            print('Return to update event tickets menu...')
                        elif sec_choise not in event['sold']: #if the section is not in the sold tickets list
                            print('\nWrong Input!!!!\nThis section does not exist.\n')
                        else: #if the section exist, ask user to choose the ticket by the number from the list above
                            ticket_choise = int(input("Enter the number of the ticket you want to unsold: "))
                            #the unsold ticket: remove from sold and add to available
                            ticket = event['sold'][sec_choise][ticket_choise - 1]
                            event['available'][sec_choise].append(ticket)
                            event['sold'][sec_choise].pop(ticket_choise - 1)
                        print(f'Ticket {ticket[0]} has been unsold successfully!')  #print success message
                    except ValueError: #if user input is not a valid integer
                        print('\nWrong Input!!!! Please enter a valid option from the menu!\n')
            
            elif user_choise == 'sold': #if user choose to sold, show all available tickets to user
                available_tickets = event['available'] #assign for convenience 
                if len(available_tickets) == 0: #if there are no available tickets for this event
                    print('No available tickets for this event.')
                elif len(available_tickets) > 0: #if there are available tickets for this event
                    print('--- Available Tickets ---')
                    #loop through the sections and tickets to print them
                    for sec, tickets in event['available'].items(): 
                        print(f'Section {sec}')
                        print("-"*10)
                        i = 0
                        for ticket in tickets:
                            print(f'[{i+1}] Ticket {ticket[0]} - row {ticket[1]}, seat {ticket[2]}, price {ticket[3]}')
                            i += 1
                        try: #try to get user input for choosing the section and ticket to sold
                            print(f'Enter 0 anytime to cancel and return to update event tickets menu') #tell user how to cancel
                            sec_choise = input("Enter the section of the ticket you want to sold: ")
                            if sec_choise not in event['available']: #if the section is not in the available tickets list
                                print('\nWrong Input!!!!\nThis section does not exist.\n')
                            elif sec_choise == '0': #if user choose to cancel
                                    print('Canceling update...')
                                    print('Return to update event tickets menu...')
                            else: #if the section exist, ask user to choose the ticket by the number from the list above
                                ticket_choise = int(input("Enter the number of the ticket you want to sold: "))
                                if ticket_choise == 0: #if user choose to cancel
                                    print('Canceling update...')
                                    print('Return to update event tickets menu...')
                                else: #if user choose a valid ticket number, the sold ticket: remove from available and add to sold
                                    ticket = event['available'][sec_choise][ticket_choise - 1]
                                    event['sold'][sec_choise].append(ticket)
                                    event['available'][sec_choise].pop(ticket_choise - 1)
                                    print(f'Ticket {ticket[0]} has been sold successfully!')
                        except ValueError: #if user input is not a valid integer
                            print('\nWrong Input!!!! Please enter a valid option from the menu!\n')
            elif user_choise == 'cancel': #if user choose to cancel
                print('Canceling update...')
                print('Return to update event tickets menu...')
            else: #if user choose an invalid option from the sold/unsold
                print('\nWrong Input!!!! Please enter a valid choice!\n')

def update_event_information(events_data):
    """
    Update the information of an event.
    Parameters:
        events_data (list): list of events.
    Returns:
        list: The updated events data.
    """
    print('--- Update Event Information ---') #header
    utilitis.show_events_list(events_data) #call function to print the list of events with numbering for user to choose from
    print(f'[0] Return to update tickets menu')
    try: #try to get user input for choosing the event to update
        user_choise = int(input("Enter your choise: "))
    except ValueError: #if user input is not a valid integer
        print('\nWrong Input!!!! Please enter a valid option from the menu!\n')
    if user_choise == 0: #if user choose to return to update tickets menu
        print('Return to update tickets menu...')
        return events_data
    elif user_choise <= len(events_data) and user_choise > 0: #if user choose a valid event from the list
        event = events_data[user_choise - 1] #assign the chosen event for convenience
        print(f'You have selected event: {event["event"]}')
        new_user_choise = input("Do you want to update event name? (yes/no): ").lower() #ask user if they want to update the event name
        if new_user_choise == 'y' or new_user_choise == 'yes': # if user choose yes, ask for the new name and update
            new_name = input("Enter new name for the event (or press Enter to keep the current name): ")
            if new_name: #if user input is not empty, update the event name
                event['event'] = new_name
                print('Event name has been updated successfully!')
        new_user_choise = input("Do you want to update event date? (yes/no): ").lower() #ask user if they want to update the event date
        if new_user_choise == 'y' or new_user_choise == 'yes': #if user choose yes, ask for the new date and update
            new_date = input("Enter new date for the event: ")
            if new_date: #if user input is not empty, update the event date
                event['date'] = new_date
                print('Event date has been updated successfully!')
        new_user_choise = input("Do you want to update event venue? (yes/no): ").lower() #ask user if they want to update the event venue
        if new_user_choise == 'y' or new_user_choise == 'yes': #if user choose yes, ask for the new venue and update
            new_venue = input("Enter new venue for the event: ")
            if new_venue: #if user input is not empty, update the event venue
                event['venue'] = new_venue
                print('Event venue has been updated successfully!')