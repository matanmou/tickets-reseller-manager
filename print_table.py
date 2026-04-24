def print_table(cocktails):
    if not cocktails:
        print("No data available")
        return

    headers = ["Name", "Event", "Date"]

    name_width = max(len(c.get("name", "")) for c in cocktails)
    event_width = max(len(c.get("event", "")) for c in cocktails)
    date_width = max(len(c.get("date", "")) for c in cocktails)

    name_width = max(name_width, len(headers[0]))
    event_width = max(event_width, len(headers[1]))
    date_width = max(date_width, len(headers[2]))

    print("\n" + "-" * (name_width + event_width + date_width + 10))
    print(
        f"{headers[0]:<{name_width}} | "
        f"{headers[1]:<{event_width}} | "
        f"{headers[2]:<{date_width}}"
    )
    print("-" * (name_width + event_width + date_width + 10))

    for c in cocktails:
        print(
            f"{c.get('name',''):<{name_width}} | "
            f"{c.get('event',''):<{event_width}} | "
            f"{c.get('date',''):<{date_width}}"
        )

    print("-" * (name_width + event_width + date_width + 10))