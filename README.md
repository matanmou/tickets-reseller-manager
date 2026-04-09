# Tickets Reseller Manager
Tickets Reseller Manager is a commend=line application base on python.
This application let reseller to track his inventory and make action like add and update events and tickets.
This project is for devops course


## Features

- **Show Tickets / Events information** - Show tickets and events information 
- **Add Tickets / Events information** - Create new events and/or add new ticket to events
- **Update Tickets / Events information** - Update and modify events and tickets information 
- **Summary** - Show inventory summary
- **Load/Save Inventory** - Load or save the current and update inventory by reseller choose


## Requirements

Python 3

## Installation and running

**Clone the repository**
```bash
   git clone https://github.com/matanmou/tickets-reseller-manager.git
```
**Run the application**
```bash
  python3 main.py
```

## Usage Guide
Once the application starts, It present a main menu:
1. **Show Tickets / Events information**
    - **[1] Show Upcoming Events** - Show only all upcoming events
    - **[2] Show Available Tickets** - Show only upcoming events with available tickets and tickets information
    - **[3] Show All History Events** - Show all events include outdated event
    - **[4] Show Best Selling Events** - Show top 5 best selling events by number of tickets
2. **Add Tickets / Events information**
    - **[1] Add ticket to event** - Add a new ticket to event
    - **[2] Add event** - Create new event
3. **Update Tickets / Events information**
    - **[1] Update Event Tickets** - Update tickets information
    - **[2] Update Event Information** - Update event information
4. **Summary**
    - Show inventory summary
5. **Load/Save Inventory**
    - **[1] Load data** - Load new data
    - **[2] Save data** - Save the current update data in the application
0. **Exit**
    - Exit from the application

## Data Structure
**Event data** - List of events dictionaries

*each event dictionary*:
   - ***"event"***: *event's name*
   - ***"date"***: *event's date*
   - ***"venue"***: *event's location*
   - ***"available"***: *dictionary of section with available tickets fot the event (each ticket is a list)*
     - ***"section"***: *ticket's section*

            each ticket is list with this order: [SERIAL NUMBER, ROW, SEAT, PRICE]

   - ***"sold"***: *dictionary of section with sold tickets fot the event (each ticket is a list)*
     - ***"section"***: *ticket's section*

            each ticket is list with this order: [SERIAL NUMBER, ROW, SEAT, PRICE]
