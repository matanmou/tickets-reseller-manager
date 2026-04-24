import print_table

def sort_by_event(cocktails):
    print("\nSorted by event:")
    print_table.print_table(sorted(cocktails, key=lambda x: x.get("event", "").lower()))