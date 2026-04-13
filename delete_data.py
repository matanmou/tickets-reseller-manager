def delete_event(events_data):
    if len(events_data) == 0:
        print("No events to delete.")
    else:
        print("Summary of all events: \n")
        i = 0
        for event in events_data:
            i += 1
            print(f"[{i}] - {event['event']}, held on {event['date']} at {event['venue']}")
        try:
            user_choice = int(input("\Enter the number of event to delete, or -1 to cancel: "))
            if user_choice != -1:
                del events_data[user_choice-1]
                print("Event deleted!")
        except:
            print(f"Error! Input has to be a whole number between 1 and {i}.")