# FollowUpPilot

A lightweight CRM and sales follow-up assistant for freelancers, agencies, independent salespeople, and small businesses.

**Need help?** Start with the in-app **Quick Support** guide at the bottom of the workspace. It explains browser recommendations, Opera 403 errors, server startup, health checks, and port conflicts.

## Features
- Dashboard with lead totals, pipeline value, conversion tracking, and follow-ups due.
- Create, edit, search, filter, and delete leads.
- Track stages: New, Contacted, Interested, Converted, and Lost.
- Store contact details, deal value, source, follow-up date, and conversation notes.
- Follow-up queue for overdue and upcoming tasks.
- Export leads to CSV.
- Responsive desktop and mobile interface.
- SQLite storage. No paid API keys or external database required.

## Browser recommendations

Use a current, updated browser:
- **Google Chrome:** recommended cross-platform starting point.
- **Microsoft Edge:** another strong cross-platform option.
- **Mozilla Firefox:** supported alternative.
- **Apple Safari:** recommended option on macOS.

FollowUpPilot uses standard browser features such as Fetch, modern JavaScript, and CSS. Keep your browser updated. Browser extensions, VPNs, proxies, antivirus web shields, and strict privacy settings can interfere with local addresses even when the app itself is working.

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

7. Open **http://127.0.0.1:5000/** in your browser. Keep the Terminal window open while using the app.

The app creates its SQLite database in the Flask instance folder automatically. The first run creates the database. When upgrading from an older version, the app attempts to copy the previous project-root database into the new instance folder if one exists.

## Troubleshooting guide

### 1. Browser says 403 Forbidden or Access Denied

First, check whether the page is a browser-branded block page or an app response:
1. Open **http://127.0.0.1:5000/api/health**.
2. Check the Terminal window. If the request never appears in the Flask log, the browser, extension, VPN, proxy, or another local security tool may be blocking it before it reaches the app.
3. Try the same address in a different browser. If Safari or Chrome works but Opera does not, the app is likely running and the issue is specific to the failing browser or its settings.

**For Opera:**
- Open a Private window and test again.
- Temporarily turn off Opera VPN for this test.
- Check Opera Settings for a configured proxy.
- Temporarily disable the ad blocker and privacy extensions, or add a site exception for the local app if the extension supports it.
- Try **http://localhost:5000/** instead of **http://127.0.0.1:5000/**.
- Restore your preferred privacy protections after testing. Do not permanently disable security features just to use the app.

These steps are troubleshooting suggestions, not a guarantee that every 403 has the same cause. A 403 returned by the Flask app will appear in its Terminal request log; a browser-generated block may not.

### 2. This site can't be reached / connection refused
- Confirm the server is running and the Terminal window has not been closed.
- Start it again from the project folder with the virtual environment activated: `python app.py`.
- Visit **http://127.0.0.1:5000/**, not an HTTPS address.
- Check the health endpoint: **http://127.0.0.1:5000/api/health**. A healthy response includes `"status":"ok"`.

### 3. Port 5000 is already in use
Start on another port:

macOS/Linux:
```bash
PORT=5001 python app.py
```

Windows PowerShell:
```powershell
$env:PORT=5001
python app.py
```

Then visit **http://127.0.0.1:5001/**.

### 4. Changes are not appearing
- Refresh the page.
- If necessary, do a hard refresh: `Cmd + Shift + R` on Mac or `Ctrl + Shift + R` on Windows/Linux.
- Confirm you extracted and launched the latest project folder, not an older copy.

### 5. API or database error
- Check the Terminal output for the first Python error message.
- Confirm the virtual environment is activated and dependencies installed with `python -m pip install -r requirements.txt`.
- Do not delete the database file to troubleshoot unless you have a backup. It contains your saved leads.

### 6. Still not working?
Record the browser name/version, operating system, exact URL, error text, and the last relevant lines from the Terminal. Remove or hide any customer contact information before sharing logs or screenshots. Test the health endpoint and another browser to help identify whether the problem is browser-side or server-side.

## Deployment and data safety

This repository is an MVP for local, single-user testing. **Do not expose it to the public internet or use it for real customer data yet.** Before a public multi-user launch, implement authentication, per-user data isolation, CSRF protection, secure session configuration, database backups, and production monitoring. Use a production WSGI server rather than Flask's built-in development server.

For a compatible Linux hosting environment, the included `Procfile` uses Gunicorn. The SQLite setup is suitable for local development, not concurrent multi-user production hosting; use a managed database for a real public service.

## Stack
Python, Flask, SQLite, HTML, CSS, and vanilla JavaScript.

## License
MIT
