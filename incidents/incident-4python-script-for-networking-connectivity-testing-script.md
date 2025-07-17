# 🧰 Network Diagnostic Tool – Windows 11 (Python GUI)

A simple but powerful network diagnostic tool built with Python and Tkinter for IT helpdesk and sysadmin use. This GUI utility allows you to perform basic network tests like local IP retrieval, DNS resolution, and ping tests to check internet connectivity.

---

## 📌 Project Overview

- **Tool Name:** Network Diagnostic GUI  
- **Platform:** Windows 11 (Built using Python 3.13)  
- **Purpose:** Help IT staff troubleshoot basic connectivity issues via a user-friendly interface.  
- **Language:** Python (with Tkinter)  
- **Packaged as:** Standalone `.exe` using `pyinstaller`

---

## 🎯 Features

- 🔍 Detects local IP address
- 🌐 Performs ping tests to `8.8.8.8` (Google DNS)
- 🧠 Tests DNS resolution (e.g., resolves `google.com`)
- ✅ GUI pop-up with pass/fail results
- 🗃️ Clean and minimal interface, suitable for non-technical users

---

## 📸 Screenshot

> ![Screenshot of GUI](screenshots/network_gui_demo.png)  
*Simple layout with one-click diagnostics*

---

## 🚀 Installation & Usage

### 🔧 Prerequisites (for source code)

- Python 3.10+ installed on Windows
- Required modules: `tkinter`, `socket`, `subprocess`

### ▶️ To run from source:

```bash
python network_gui.py

🪄 To create the .exe (optional):

Install PyInstaller if you haven’t:

pip install pyinstaller

Then generate the EXE:

pyinstaller --onefile --windowed network_gui.py

Executable will appear in the dist/ folder.
🧾 Sample Output

When running diagnostics, the tool returns:

✅ Local IP: 192.168.1.45  
✅ Connectivity to 8.8.8.8 successful  
✅ DNS resolution working  

Or error messages like:

❌ Could not ping 8.8.8.8  
❌ DNS resolution failed  

📁 Files Included

    network_gui.py — Python source code

    network_gui.exe — Compiled executable (optional, not versioned)

    README.md — This documentation

    screenshots/ — Optional GUI screenshot(s)

✍️ Author

    Name: David Vargas

    Role: IT Support Specialist (UCF Graduate)

    Date: July 17, 2025

💡 Future Ideas

    Add traceroute and gateway ping

    Export results to .txt or .log

    Auto-repair DNS with fallback (e.g., switch to 1.1.1.1)

    Integrate system info panel (OS, hostname, uptime)

📜 License

This project is released under the MIT License.


---

Let me know if you'd like this turned into a downloadable ZIP with the `README`, `.py`, and scr
