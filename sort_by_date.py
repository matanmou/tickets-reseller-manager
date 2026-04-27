import print_table

def sort_by_date(cocktails):
    print("\nSorted by date:")
    print_table.print_table(sorted(cocktails, key=lambda x: x.get("date", "")))