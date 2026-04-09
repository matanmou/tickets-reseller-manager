"""
This module contains utility functions for application
For convenience, these functions are used in multiple modules to avoid code repetition and to keep the code organized.
"""

import datetime

def show_events_list(events_data):
    """
    This function is used to print the list of events
    Parameters:
        events_data (list): list of events to be printed
    """
    if len(events_data) == 0: # if the list is empty, print a message to inform the user
        print("\nThere is no events!\n")
    else: 
        i = 0 #init a counter for event numbering
        for event in events_data: #loop through the list of events and print the event information with numbering
            print(f'[{i+1}] {event['event']} - {event['date']} - {event['venue']}')
            i += 1

def list_of_upcoming_events(events_data):
    """
    This function is used to get a list of upcoming events
    Parameters:
        events_data (list): list of events
    Returns:
        list: list of upcoming events
    """
    upcoming_events = [] #init an empty list to store the only upcoming events
    i = 0 #init a counter to keep track of the original index of the event in the original events data list
    for event in events_data: #loop through events list and check if the event is upcoming event
        if datetime.datetime.strptime(event['date'], "%d/%m/%Y") >= datetime.datetime.now(): #if event date is greater than or equal to the current date
            new_event = event.copy() #make a copy of the event to avoid modifying the original event in the events data list
            new_event['indx'] = i #add the original index to know the position of the event in the original events data list
            upcoming_events.append(new_event) #add the event to the upcoming events list
        i += 1
    return upcoming_events

def list_of_previous_events(events_data):
    """
    This function is used to get a list of previous events
    Parameters:
        events_data (list): list of events
    Returns:
        list: list of previous events
    """
    previous_events = [] #init an empty list to store the only previous events
    i = 0 #init a counter to keep track of the original index of the event in the original events data list
    for event in events_data: #loop through events list
        if datetime.datetime.strptime(event['date'], "%d/%m/%Y") < datetime.datetime.now(): #if event date is less than the current date
            new_event = event.copy() #make a copy of the event to avoid modifying the original event in the events data list
            new_event['indx'] = i #add the original index to know the position of the event in the original events data list
            previous_events.append(new_event) #add the event to the previous events list
        i += 1
    return previous_events

def list_sorted_by_tickets_selling(events_data):
    """
    This function is used to get a list of events sorted by the number of sold tickets in descending order
    """
    new_event_list = [] #init an empty list to store the events with the number of sold tickets on each event
    for event in events_data: #loop through the events data list
        new_event = event.copy() #make a copy of the event to avoid modifying the original event in the events data list
        sold_count = 0 #init a counter for the number of sold tickets for this event
        for tickets in new_event['sold'].values(): #loop through the section's tickets list in sold key
            sold_count += len(tickets) #add to counter the number of sold tickets in this section
        new_event['sold_count'] = sold_count #add the counter to the new event
        new_event_list.append(new_event) #add the new event to the new event list
    sorted_events = sorted(new_event_list, key=lambda x: x['sold_count'], reverse=True) #sort the new event list by the number of sold tickets in descending order
    return sorted_events