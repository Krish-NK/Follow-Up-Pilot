# FollowUpPilot

A lightweight CRM and sales follow-up assistant for freelancers, agencies, independent salespeople, and small businesses.

**Need help?** Start with the in-app **Quick Support** guide at the bottom of the workspace. It includes Windows and Mac setup tips, browser recommendations, common errors, and data-safety advice.

## Features
- Dashboard with lead totals, pipeline value, conversion tracking, and follow-ups due.
- Create, edit, search, filter, and delete leads.
- Track stages: New, Contacted, Interested, Converted, and Lost.
- Store contact details, deal value, source, follow-up date, and conversation notes.
- Follow-up queue for overdue and upcoming tasks.
- Export leads to CSV.
- Responsive desktop and mobile interface.
- SQLite storage. No paid API keys or external database required.

## Recommended browsers

Use a current, updated browser:
- **Google Chrome:** easiest cross-platform default.
- **Microsoft Edge:** strong choice on Windows and also available on Mac.
- **Apple Safari:** a good default on macOS.
- **Mozilla Firefox:** supported alternative.

Keep the browser updated. VPNs, proxies, ad blockers, privacy extensions, antivirus web shields, and strict browser protections can sometimes interfere with local development addresses.

## Requirements

- Python 3.10 or newer.
- Windows 10/11, or a supported macOS version.
- A modern browser.
- Internet access is needed the first time to install Python packages. The app itself runs locally after setup.

## Windows setup

1. Install Python from [python.org/downloads](https://www.python.org/downloads/) or the Microsoft Store. During installation, follow the installer prompts and make sure the Python launcher is available.
2. Download the repository ZIP from GitHub and extract it. Do not try to run the app from inside the ZIP preview.
3. Open the extracted **Follow-Up-Pilot** folder in File Explorer.
4. Open PowerShell in that folder. In File Explorer, click the address bar, type `powershell`, and press Enter.
5. Create a virtual environment:

   ```powershell
   py -3 -m venv .venv
   ```

6. Activate it:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks the activation script, you can use Command Prompt instead and run `.venv\Scripts\activate.bat`. Alternatively, allow locally created scripts for your Windows user only with `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, then reopen PowerShell. Do not set a machine-wide unrestricted policy.

7. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

8. Start the app:

   ```powershell
   python app.py
   ```

9. Open **http://127.0.0.1:5000/** in your browser. Keep PowerShell open while using the app.

**Windows tips**
- If `py` works but `python` does not, use `py` to create the environment, then activate it before using `python`.
- If Windows asks whether Python can access a network, this local-only app should not need to be exposed to other devices. Do not create a public inbound firewall rule for it.
- Avoid running the project as Administrator. Normal user permissions are sufficient.
- If you use OneDrive or another sync tool, keep the live SQLite database out of folders that may sync or lock files while the app is running. Back it up when the app is stopped.
- To stop the app, return to PowerShell and press `Ctrl + C`.

## macOS setup

1. Check whether Python 3 is installed. Open **Terminal** and run:

   ```bash
   python3 --version
   ```

2. If Python 3.10 or newer is not available, install a current Python 3 release from [python.org/downloads](https://www.python.org/downloads/macos/).
3. Download the repository ZIP from GitHub and extract it. Open the extracted **Follow-Up-Pilot** folder in Finder.
4. Open Terminal in the project folder. A simple method is to type `cd ` in Terminal, drag the project folder into the Terminal window, and press Enter.
5. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

6. Activate it:

   ```bash
   source .venv/bin/activate
   ```

7. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

8. Start the app:

   ```bash
   python app.py
   ```

9. Open **http://127.0.0.1:5000/** in Safari, Chrome, Edge, or Firefox. Keep Terminal open while using the app.

**Mac tips**
- Use `python3` to create the environment. Once it is activated, use `python` for the remaining commands.
- Do not use `sudo pip install`. Install packages inside the project's virtual environment.
- On Apple silicon (M-series) and Intel Macs, install the appropriate current Python installer from python.org if Python is missing. You do not need to install Homebrew just to run this project.
- If macOS asks about network access, remember that the app is intended for use on your own computer. Do not configure router port forwarding or expose it to the internet.
- To stop the app, return to Terminal and press `Control + C`.

## Run locally: quick reference

After the first setup, start the app like this each time:

**macOS**
```bash
cd /path/to/Follow-Up-Pilot
source .venv/bin/activate
python app.py
```

**Windows PowerShell**
```powershell
cd C:\path\to\Follow-Up-Pilot
.venv\Scripts\Activate.ps1
python app.py
```

Then visit **http://127.0.0.1:5000/**. If you close the terminal, the local server stops. Reopen the terminal and repeat the start commands to use the app again.

## Troubleshooting guide

### 1. Browser says 403 Forbidden or Access Denied

First, check whether the page is a browser-branded block page or an app response:
1. Open **http://127.0.0.1:5000/api/health**.
2. Check the Terminal or PowerShell window. If the request never appears in the Flask log, the browser, extension, VPN, proxy, or another local security tool may be blocking it before it reaches the app.
3. Try the same address in another browser. If Safari or Chrome works but Opera does not, the app is likely running and the issue is specific to the failing browser or its settings.

**For Opera**
- Open a Private window and test again.
- Temporarily turn off Opera VPN for this test.
- Check Opera Settings for a configured proxy.
- Temporarily disable ad blocking and privacy extensions, or add a local-site exception if supported.
- Try **http://localhost:5000/** instead of **http://127.0.0.1:5000/**.
- Restore your preferred privacy protections after testing. Do not permanently disable security features just to use the app.

These are troubleshooting suggestions, not a guarantee that every 403 has the same cause. A 403 returned by Flask should appear in its Terminal or PowerShell request log; a browser-generated block may not.

### 2. This site can't be reached / connection refused
- Confirm the server is running and the Terminal or PowerShell window is still open.
- Start it again from the project folder with the virtual environment activated: `python app.py`.
- Visit **http://127.0.0.1:5000/**, not an HTTPS address.
- Check **http://127.0.0.1:5000/api/health**. A healthy response includes `"status":"ok"`.

### 3. Port 5000 is already in use

macOS:
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
- Hard refresh: `Cmd + Shift + R` on Mac or `Ctrl + Shift + R` on Windows.
- Confirm you extracted and launched the latest project folder, not an older copy.

### 5. Python or package command not found
- Windows: try `py --version` and create the environment with `py -3 -m venv .venv`.
- Mac: try `python3 --version`.
- Reopen the terminal after installing Python. If it still fails, reinstall Python from the official Python website and follow its PATH/launcher setup instructions.

### 6. API or database error
- Check the Terminal or PowerShell output for the first Python error message.
- Confirm the virtual environment is activated and run `python -m pip install -r requirements.txt`.
- Do not delete the database file to troubleshoot unless you have a backup. It contains your saved leads.

### 7. Back up your leads
The SQLite database is stored in the project's `instance` folder. Stop the app with `Ctrl + C` (Windows) or `Control + C` (Mac), then copy the database file from `instance` to a safe backup location. Keep backups private because lead records may contain personal and business contact information. Do not share the database in screenshots or public repositories.

### 8. Still not working?
Record the browser name/version, operating system, exact URL, error text, and the last relevant lines from the Terminal or PowerShell. Remove or hide customer contact information before sharing logs or screenshots. Test the health endpoint and another browser to help identify whether the problem is browser-side or server-side.

## Deployment and data safety

This repository is an MVP for local, single-user testing. **Do not expose it to the public internet or use it for real customer data yet.** Before a public multi-user launch, implement authentication, per-user data isolation, CSRF protection, secure session configuration, database backups, and production monitoring. Use a production WSGI server rather than Flask's built-in development server.

For a compatible Linux hosting environment, the included `Procfile` uses Gunicorn. The SQLite setup is suitable for local development, not concurrent multi-user production hosting; use a managed database for a real public service.

## Stack
Python, Flask, SQLite, HTML, CSS, and vanilla JavaScript.

## License
MIT
