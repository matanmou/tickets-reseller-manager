"""
This module summarizes the system.
It's let the user to see the summary of the events and tickets information.
"""


from datetime import datetime
import utilitis

def show_summary(events_data):
    """
    Show a summary of the system to the user.
    Parameters:
        events_data (list): list of events.
    """
    print('===== Summary Menu =====') #header for summary
    print('') #spacer
    #print the total number of events in the system
    print(f'Total number of events in the system: {len(events_data)}')
    #for convenience. get lists on order and by specific criteria to use in the summary
    upcoming_events = utilitis.list_of_upcoming_events(events_data)
    previous_events = utilitis.list_of_previous_events(events_data)
    sorted_events = utilitis.list_sorted_by_tickets_selling(events_data)
    years_cnt = count_events_this_year(events_data) #get dict with count of event in each year
    this_year_str = datetime.now().strftime("%Y") #get the current year
    number_this_year = years_cnt[this_year_str] #get the counter for current year
    #print the number of event in current year
    print(f'The number of events this year ({this_year_str}): {number_this_year}')
    print('') #spacer
    #print the best selling event by number of tickets
    print(f'Most Tickets Sold Event: {sorted_events[0]["event"]} - Number of sold tickets: {sorted_events[0]["sold_count"]}')
    most_income_event = most_income_from_event(events_data) #get the best selling event by total income
    event_income = calculate_event_income(most_income_event) #calculate the income to show in the summary
    #print the best selling event by total income
    print(f'Most Income Event: {most_income_event["event"]} - Total income: {event_income:.2f} NIS')
    income = total_income(events_data) #calculate the total income from sold tickets for all events
    #print the total income from sold tickets for all events
    print(f'Total all events income: {income:.2f} NIS')
    print('') #spacer
    if len(upcoming_events) > 0: #print the next event if there are upcoming events
        print(f'Upcoming Event: {upcoming_events[0]["event"]}')
    else:
        print('No upcoming events')
    if len(previous_events) > 0: #print the last event if there are previous events
        print(f'Previous Event: {previous_events[-1]["event"]}')
    else:
        print('No previous events')

    input('\nPress Enter to continue...') #wait for user input before return to main menu
    print('\nReturn to main menu...')


def count_events_this_year(events_data):
    """
    Count the number of events in each year. return a dict with the count per year.
    Parameters:
        events_data (list): list of events.
    Returns:
        dict: A dictionary with years as keys and events counter as values.
    """
    season_cnt = {}
    for event in events_data:
        year = event['date'].split('/')[-1]
        if year in season_cnt:
            season_cnt[year] += 1
        else:
            season_cnt[year] = 1
    return season_cnt

def total_income(events_data):
    """
    Calculate the total income from sold tickets for all events.
    Parameters:
        events_data (list): list of events.
    Returns:
        float: Total income from sold tickets.
    """
    total_income = 0 #init a variable to store the total income from sold tickets
    for event in events_data: #loop through all events
        total_income += calculate_event_income(event) #call the function to calculate the income from each event  and add it to the total income
    return total_income

def most_income_from_event(events_data):
    """
    Get the best selling event by total income.
    Parameters:
        events_data (list): list of events.
    Returns:
        dict: the most income event.
    """
    most_income_event = {}
    most_income = 0
    for event in events_data: #loop through all events
        event_income = calculate_event_income(event) #call the function to calculate the income from each event
        if event_income > most_income: #if the income from this event is greater than the current most income, update the most income and the most income event
            most_income = event_income
            most_income_event = event.copy()
    return most_income_event


def calculate_event_income(event):
    """
    Calculate the total income from sold tickets for a specific event.
    Parameters:
        event (dict): the event to calculate its income.
    Returns:
        float: Total income from sold tickets for the event.
    """
    event_income = 0
    for section in event['sold'].values(): #lopp through the sections of sold tickets
        for ticket in section: #loop through each ticket and add the price to event income
            event_income += ticket[-1]
    return event_income