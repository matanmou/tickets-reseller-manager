# Tickets Reseller Manager

Tickets Reseller Manager lets resellers track their event/ticket inventory.
It ships in two flavours:

- **CLI** — `python main.py` (original menu-driven app).
- **Web (Flask)** — same features served over HTTP, deployable behind Apache via mod_wsgi.

Both flavours share the same `data.json` storage so they're interchangeable.


## Features

- **Show Tickets / Events information** — upcoming, all-history, best-selling, available, search-by-serial
- **Add Tickets / Events information** — add event, add ticket to event, duplicate event
- **Update Tickets / Events information** — edit event details, sell / unsell tickets
- **Delete event**
- **Summary** — totals, income, top event, next/previous event
- **Load / Save Inventory** — `data.json` persistence (CLI: explicit; web: auto-save on every mutation)


## Requirements

- Python 3.10+
- For Apache deployment: `libapache2-mod-wsgi-py3`


## Installation

```bash
git clone https://github.com/matanmou/tickets-reseller-manager.git
cd tickets-reseller-manager
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```


## Running the CLI

```bash
venv/bin/python main.py
```


## Running the web app

### Development server

```bash
venv/bin/flask --app wsgi:application run --debug
```
Open <http://localhost:5000>.

### Production — Apache + mod_wsgi

A ready-to-use vhost is included at [apache/tickets-reseller.conf](apache/tickets-reseller.conf).

```bash
sudo apt install libapache2-mod-wsgi-py3
sudo cp apache/tickets-reseller.conf /etc/apache2/sites-available/
sudo a2ensite tickets-reseller
sudo chown www-data:www-data data.json    # so Apache can persist mutations
sudo systemctl reload apache2
```
Tail logs at `/var/log/apache2/tickets-reseller-error.log`. After editing app code, touch `wsgi.py` (or reload Apache) to pick up changes.

### Routes
| Method | Path                                                | Purpose                       |
|--------|-----------------------------------------------------|-------------------------------|
| GET    | `/`                                                 | Dashboard                     |
| GET    | `/events?sort=date\|event`                          | All events (sortable)         |
| GET    | `/events/upcoming`                                  | Upcoming only                 |
| GET    | `/events/best-selling`                              | Top 5 by sold count           |
| GET    | `/events/<idx>`                                     | Event detail + tickets        |
| GET/POST | `/events/new`                                     | Add event                     |
| GET/POST | `/events/<idx>/edit`                              | Edit event                    |
| POST   | `/events/<idx>/duplicate`                           | Duplicate event               |
| POST   | `/events/<idx>/delete`                              | Delete event                  |
| GET/POST | `/events/<idx>/tickets/new`                       | Add ticket                    |
| POST   | `/events/<idx>/tickets/<section>/<pos>/sell`        | Mark ticket sold              |
| POST   | `/events/<idx>/tickets/<section>/<pos>/unsell`      | Mark ticket unsold            |
| GET    | `/tickets/available`                                | Available tickets across upcoming |
| GET    | `/tickets/search?serial=...`                        | Search by serial number       |
| GET    | `/summary`                                          | Full summary                  |
| GET/POST | `/data`                                           | Explicit save / reload        |

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

## Open for contribution
1. **Delete Event(DONE)** - Delete event from the list and the inventory
2. **Duplicate Event(DONE)** - user choose event to duplicate and all tickets init to available dict, ask user for new date
3. **Show user ticket by serial number(DONE)** - let user enter serial number of ticket and print ticket details (ticket and event information)
