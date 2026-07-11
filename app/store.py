"""
JSON-file backed data store for the web app.

Reads data.json on every request and writes it back on every mutation.
A threading.Lock guards writes within a single worker process. This matches
the file-based persistence model the CLI already used.
"""

import json
import threading
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data.json"
_lock = threading.Lock()


def load():
    """Return the events list, or [] if the file is missing/empty."""
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save(events_data):
    """Persist the events list to data.json."""
    with _lock:
        with open(DATA_PATH, "w") as f:
            json.dump(events_data, f, indent=2)


def load_from_path(path):
    """Load events from an arbitrary path (used by the /data load action)."""
    with open(path, "r") as f:
        return json.load(f)
