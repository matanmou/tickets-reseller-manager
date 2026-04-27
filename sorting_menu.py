import sort_by_date
import sort_by_event

def sorting_menu(cocktails):
    while True:
        print("\n--- Sorting Menu ---")
        print("1. Sort by event")
        print("2. Sort by date")
        print("3. Back to main menu")

        choice = input("Select option: ").strip()

        if choice == "1":
            sort_by_event.sort_by_event(cocktails)
        elif choice == "2":
            sort_by_date.sort_by_date(cocktails)
        elif choice == "3":
            return
        else:
            print("Invalid option")