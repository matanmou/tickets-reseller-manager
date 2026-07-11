# Tickets Reseller Static Frontend

This folder contains a static HTML/CSS/JS version of the Tickets Reseller Manager.

## Files

- `index.html` — main frontend page
- `styles.css` — layout and styling
- `app.js` — application logic and navigation
- `data.json` — sample events and tickets dataset

## Run locally

To use the app, open the `frontend` folder in a local server and visit `http://localhost:8000`.

### Python server

```bash
cd frontend
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Notes

- Data is loaded from `data.json` and persisted in browser storage.
- Changes are stored in `localStorage`, so reload does not lose the current inventory unless you clear browser data.
- Use the navigation bar to browse the dashboard, events, search, and summary pages.
- The frontend logs the current EC2 instance ID to the browser console if `window.EC2_INSTANCE_ID` is injected by the server. Otherwise it logs `unknown`.
