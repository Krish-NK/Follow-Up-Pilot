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
1. Install Python 3.10 or newer.
2. Open Terminal in this folder.
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Windows: `.venv\\Scripts\\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Visit http://127.0.0.1:5000

The SQLite database is created automatically on first run.

## Stack
Python, Flask, SQLite, HTML, CSS, and vanilla JavaScript.

## Production note
This MVP is intended for local use and development. Before a multi-user deployment, add authentication, per-user data isolation, CSRF protection, secure production configuration, and automated backups.

## License
MIT
