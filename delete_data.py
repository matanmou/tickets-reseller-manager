import utilitis
def delete_event(events_data):
    if len(events_data) == 0:
        print("No events to delete.")
    else:
        print("Summary of all events: \n")
        utilitis.show_events_list(events_data)
        try:
            user_choice = int(input("\Enter the number of event to delete, or -1 to cancel: "))
            if user_choice != -1:
                del events_data[user_choice-1]
                print("Event deleted!")
        except:
            print(f"Error! Input has to be a whole number between 1 and {len(events_data)}.")