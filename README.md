# FollowUpPilot

A lightweight CRM and sales follow-up assistant for freelancers, agencies, independent salespeople, and small businesses.

## Features
- Dashboard with lead totals, pipeline value, conversion tracking, and follow-ups due.
- Create, edit, search, filter, and delete leads.
- Track stages: New, Contacted, Interested, Converted, and Lost.
- Store contact details, deal value, source, follow-up date, and conversation notes.
- Follow-up queue for overdue and upcoming tasks.
- Export leads to CSV.
- Responsive desktop and mobile interface.
- SQLite storage. No paid API keys or external database required.

## Run locally

**Requirements:** Python 3.10 or newer.

1. Download and extract this repository.
2. Open Terminal (macOS/Linux) or PowerShell (Windows) in the extracted project folder.
3. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

   On Windows, use `py -m venv .venv` if `python3` is unavailable.

4. Activate it:

   macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Start the app:

   ```bash
   python app.py
   ```

7. Open **http://127.0.0.1:5000** in your browser. Keep the Terminal window open while using the app.

The app creates its SQLite database in the Flask instance folder automatically. This keeps the database location stable even if the app is launched from another working directory.

## Browser troubleshooting

- If the page does not load, confirm the Terminal still shows the server is running.
- Try **http://localhost:5000/** as an alternative to **http://127.0.0.1:5000/**.
- If one browser shows **403 Access Denied** but another browser works, the request may be blocked by that browser, a VPN, proxy, privacy setting, or extension. Try a private window or another browser, and check those browser settings. A browser-generated 403 is not necessarily an application response.
- Check the server's Terminal output for the request and status code. The app's health endpoint is **http://127.0.0.1:5000/api/health** and should return JSON with `"status":"ok"`.
- If port 5000 is already in use, stop the other process or start with another port:
  macOS/Linux: `PORT=5001 python app.py`
  Windows PowerShell: `$env:PORT=5001; python app.py`
  Then visit **http://127.0.0.1:5001**.

## Deployment and data safety

This repository is an MVP for local, single-user testing. **Do not expose it to the public internet or use it for real customer data yet.** Before a public multi-user launch, implement authentication, per-user data isolation, CSRF protection, secure session configuration, database backups, and production monitoring. Use a production WSGI server rather than Flask's built-in development server.

For a compatible Linux hosting environment, the included `Procfile` uses Gunicorn. The SQLite setup is suitable for local development, not concurrent multi-user production hosting; use a managed database for a real public service.

## Stack
Python, Flask, SQLite, HTML, CSS, and vanilla JavaScript.

## License
MIT
