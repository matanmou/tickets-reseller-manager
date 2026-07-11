"""HTTP route handlers for the Tickets Reseller web app."""

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, abort,
)

from . import store
from . import services

bp = Blueprint("tickets", __name__)


# ---------- Dashboard ----------

@bp.route("/")
def index():
    events = store.load()
    return render_template(
        "index.html",
        events=events,
        summary=services.build_summary(events),
    )


# ---------- Event lists ----------

@bp.route("/events")
def events_list():
    events = store.load()
    sort = request.args.get("sort")
    view = services.sort_events(events, sort) if sort else events
    return render_template(
        "events_list.html",
        events=view,
        title="All Events",
        empty="No events yet.",
        sort=sort,
        show_actions=True,
    )


@bp.route("/events/upcoming")
def events_upcoming():
    events = store.load()
    return render_template(
        "events_list.html",
        events=services.upcoming(events),
        title="Upcoming Events",
        empty="No upcoming events.",
        show_actions=True,
    )


@bp.route("/events/best-selling")
def events_best_selling():
    events = store.load()
    ranked = services.by_sold_count(events)[:5]
    return render_template(
        "events_list.html",
        events=ranked,
        title="Top 5 Best-Selling Events",
        empty="No sales yet.",
        show_sold_count=True,
    )


# ---------- Event detail + mutations ----------

def _require_event(events, idx):
    if idx < 0 or idx >= len(events):
        abort(404)
    return events[idx]


@bp.route("/events/<int:idx>")
def event_detail(idx):
    events = store.load()
    event = _require_event(events, idx)
    return render_template("event_detail.html", event=event, idx=idx)


@bp.route("/events/new", methods=["GET", "POST"])
def event_new():
    if request.method == "POST":
        name = request.form.get("event", "").strip()
        date = request.form.get("date", "").strip()
        venue = request.form.get("venue", "").strip()
        if not (name and date and venue):
            flash("Name, date, and venue are required.", "danger")
            return render_template("event_form.html", mode="new",
                                   event={"event": name, "date": date, "venue": venue})
        events = store.load()
        events.append({"event": name, "date": date, "venue": venue,
                       "available": {}, "sold": {}})
        store.save(events)
        flash(f"Event '{name}' added.", "success")
        return redirect(url_for("tickets.events_list"))
    return render_template("event_form.html", mode="new", event=None)


@bp.route("/events/<int:idx>/edit", methods=["GET", "POST"])
def event_edit(idx):
    events = store.load()
    event = _require_event(events, idx)
    if request.method == "POST":
        event["event"] = request.form.get("event", event["event"]).strip() or event["event"]
        event["date"] = request.form.get("date", event["date"]).strip() or event["date"]
        event["venue"] = request.form.get("venue", event["venue"]).strip() or event["venue"]
        store.save(events)
        flash("Event updated.", "success")
        return redirect(url_for("tickets.event_detail", idx=idx))
    return render_template("event_form.html", mode="edit", event=event, idx=idx)


@bp.route("/events/<int:idx>/duplicate", methods=["POST"])
def event_duplicate(idx):
    events = store.load()
    event = _require_event(events, idx)
    new_event = {
        "event": event["event"],
        "date": event["date"],
        "venue": event["venue"],
        "available": {},
        "sold": {},
    }
    events.append(new_event)
    store.save(events)
    flash(f"Event '{event['event']}' duplicated.", "success")
    return redirect(url_for("tickets.events_list"))


@bp.route("/events/<int:idx>/delete", methods=["POST"])
def event_delete(idx):
    events = store.load()
    _require_event(events, idx)
    removed = events.pop(idx)
    store.save(events)
    flash(f"Event '{removed['event']}' deleted.", "success")
    return redirect(url_for("tickets.events_list"))


# ---------- Tickets ----------

@bp.route("/events/<int:idx>/tickets/new", methods=["GET", "POST"])
def ticket_new(idx):
    events = store.load()
    event = _require_event(events, idx)
    if request.method == "POST":
        section = request.form.get("section", "").strip()
        sn = request.form.get("serial", "").strip()
        row = request.form.get("row", "").strip()
        seat = request.form.get("seat", "").strip()
        price_raw = request.form.get("price", "").strip()
        try:
            price = float(price_raw)
        except ValueError:
            flash("Price must be a number.", "danger")
            return render_template("ticket_form.html", event=event, idx=idx,
                                   form=request.form)
        if not all([section, sn, row, seat]):
            flash("All ticket fields are required.", "danger")
            return render_template("ticket_form.html", event=event, idx=idx,
                                   form=request.form)
        ticket = [sn, row, seat, price]
        event["available"].setdefault(section, []).append(ticket)
        store.save(events)
        flash(f"Ticket {sn} added to section {section}.", "success")
        return redirect(url_for("tickets.event_detail", idx=idx))
    return render_template("ticket_form.html", event=event, idx=idx, form={})


@bp.route("/events/<int:idx>/tickets/<section>/<int:pos>/sell", methods=["POST"])
def ticket_sell(idx, section, pos):
    events = store.load()
    event = _require_event(events, idx)
    bucket = event["available"].get(section, [])
    if pos < 0 or pos >= len(bucket):
        abort(404)
    ticket = bucket.pop(pos)
    if not bucket:
        del event["available"][section]
    event["sold"].setdefault(section, []).append(ticket)
    store.save(events)
    flash(f"Ticket {ticket[0]} sold.", "success")
    return redirect(url_for("tickets.event_detail", idx=idx))


@bp.route("/events/<int:idx>/tickets/<section>/<int:pos>/unsell", methods=["POST"])
def ticket_unsell(idx, section, pos):
    events = store.load()
    event = _require_event(events, idx)
    bucket = event["sold"].get(section, [])
    if pos < 0 or pos >= len(bucket):
        abort(404)
    ticket = bucket.pop(pos)
    if not bucket:
        del event["sold"][section]
    event["available"].setdefault(section, []).append(ticket)
    store.save(events)
    flash(f"Ticket {ticket[0]} marked unsold.", "success")
    return redirect(url_for("tickets.event_detail", idx=idx))


# ---------- Available tickets across upcoming + search ----------

@bp.route("/tickets/available")
def tickets_available():
    events = store.load()
    return render_template(
        "tickets_available.html",
        upcoming=services.upcoming(events),
    )


@bp.route("/tickets/search")
def ticket_search():
    serial = request.args.get("serial", "").strip()
    result = None
    if serial:
        events = store.load()
        match = services.find_ticket_by_serial(events, serial)
        if match:
            event, section, status, ticket = match
            result = {
                "event": event,
                "section": section,
                "status": status,
                "ticket": ticket,
            }
    return render_template("ticket_search.html", serial=serial, result=result,
                           searched=bool(serial))


# ---------- Summary ----------

@bp.route("/summary")
def summary_view():
    events = store.load()
    return render_template("summary.html", summary=services.build_summary(events),
                           total_events=len(events))


# ---------- Data load/save ----------

@bp.route("/data", methods=["GET", "POST"])
def data_io():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "save":
            store.save(store.load())
            flash("Data saved to data.json.", "success")
        elif action == "reload":
            try:
                fresh = store.load_from_path(store.DATA_PATH)
                store.save(fresh)
                flash(f"Reloaded {len(fresh)} events from data.json.", "success")
            except FileNotFoundError:
                flash("data.json not found.", "danger")
        else:
            flash("Unknown action.", "danger")
        return redirect(url_for("tickets.data_io"))
    return render_template("data_io.html", path=str(store.DATA_PATH))
