# 🛠️ IT Incident Report: Network Diagnostic GUI Tool – Windows 11

## 📌 Incident Overview
- **Title:** IT Toolkit v3.3 – Graphical Network Diagnostic Utility  
- **Environment:** Windows 11 Pro (Build 22631.xxxx)  
- **User Impact:** Helpdesk staff required a centralized tool to run basic and advanced network diagnostics through a user-friendly interface.

---

## 🧾 Problem Description

Helpdesk technicians were relying on separate CLI tools (`ping`, `ipconfig`, `nslookup`, `tracert`, etc.), making it inefficient and error-prone to troubleshoot user issues. A unified GUI-based toolkit was needed to streamline common network troubleshooting tasks.

---

## 🔍 Troubleshooting & Design Steps

A Python script was developed using `tkinter` for the GUI. Features included:

- 📋 Display of full adapter info (`ipconfig /all`)
- 🌐 Local and public IP retrieval
- 📶 Ping to gateway and external addresses
- 🛣️ Traceroute to external domains
- 🔍 Port scanning utility (basic)
- 💡 Wake-on-LAN functionality
- 🔄 Flush DNS, release/renew IP
- 📊 Tab view for ARP table, active connections, and interface metrics

---

## 🧩 Root Cause

The lack of a centralized diagnostic tool led to increased time and reduced consistency across helpdesk operations. Multiple windows and commands made troubleshooting inefficient and inconsistent.

---

## 🛠️ Solution Applied

1. Created a `network_gui.py` script using `tkinter`, modularized into logical diagnostic sections.
2. Implemented multi-threading to prevent GUI from freezing during scans or pings.
3. Used `subprocess` with `STARTUPINFO` to suppress command prompt windows.
4. Integrated friendly pop-up messages (`messagebox`) and organized tables with `ttk.Treeview`.
5. Compiled into a `.exe` using:
   ```powershell
   pyinstaller --onefile --windowed network_gui.py

    Final .exe placed in dist/ and tested across multiple Windows 11 systems successfully.

✅ Final Result

    Fully functional, self-contained executable.

    Improved response time for diagnosing network problems.

    Easier onboarding for non-technical support agents.

    Reduced tool-switching and human error in diagnostics.

📌 Recommendations

    Digitally sign the executable for corporate-wide distribution.

    Implement optional email reporting or auto-logging to a file.

    Add VPN and proxy detection in future versions.

    Include in SCCM or Intune for automatic deployment.

✅ Logged and created by: David Vargas
🗓️ Date: July 17, 2025
