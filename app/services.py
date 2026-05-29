"""
View-model helpers that wrap the pure utilities from the original CLI modules.
This is what lets routes stay thin and the templates stay dumb.
"""

from datetime import datetime

import utilitis
import summary as cli_summary


def upcoming(events_data):
    return utilitis.list_of_upcoming_events(events_data)


def previous(events_data):
    return utilitis.list_of_previous_events(events_data)


def by_sold_count(events_data):
    return utilitis.list_sorted_by_tickets_selling(events_data)


def sort_events(events_data, key):
    """Mirror sort_by_date.py / sort_by_event.py behavior."""
    if key == "date":
        return sorted(
            events_data,
            key=lambda e: datetime.strptime(e["date"], "%d/%m/%Y"),
        )
    if key == "event":
        return sorted(events_data, key=lambda e: e.get("event", "").lower())
    return events_data


def find_ticket_by_serial(events_data, serial):
    """Return (event, section, status, ticket) or None."""
    serial = serial.strip()
    for event in events_data:
        for status, bucket in (("Available", event["available"]),
                               ("Sold", event["sold"])):
            for section, tickets in bucket.items():
                for ticket in tickets:
                    if ticket[0] == serial:
                        return event, section, status, ticket
    return None


def build_summary(events_data):
    """Return a dict with all numbers the CLI summary printed."""
    if not events_data:
        return {
            "total_events": 0,
            "this_year_label": datetime.now().strftime("%Y"),
            "this_year_count": 0,
            "most_sold_event": None,
            "most_sold_count": 0,
            "most_income_event": None,
            "most_income_amount": 0.0,
            "total_income": 0.0,
            "upcoming_event": None,
            "previous_event": None,
        }

    sorted_by_sold = cli_summary.utilitis.list_sorted_by_tickets_selling(events_data)
    years = cli_summary.count_events_this_year(events_data)
    this_year = datetime.now().strftime("%Y")
    most_income_event = cli_summary.most_income_from_event(events_data)
    most_income_amount = cli_summary.calculate_event_income(most_income_event) if most_income_event else 0.0
    upcoming_events = upcoming(events_data)
    previous_events = previous(events_data)

    return {
        "total_events": len(events_data),
        "this_year_label": this_year,
        "this_year_count": years.get(this_year, 0),
        "most_sold_event": sorted_by_sold[0]["event"] if sorted_by_sold else None,
        "most_sold_count": sorted_by_sold[0]["sold_count"] if sorted_by_sold else 0,
        "most_income_event": most_income_event.get("event") if most_income_event else None,
        "most_income_amount": most_income_amount,
        "total_income": cli_summary.total_income(events_data),
        "upcoming_event": upcoming_events[0]["event"] if upcoming_events else None,
        "previous_event": previous_events[-1]["event"] if previous_events else None,
    }
