# 💽 IT Incident Report: Disk Full – Windows 11

## 📌 Incident Overview
- **Title:** Unable to Save or Install Due to Full Disk  
- **Environment:** Windows 11 Pro x64  
- **User Impact:** User cannot save files, install updates, or run certain applications.

---

## 🧾 Problem Description
The user reported that they were unable to save documents in Microsoft Word and were receiving low disk space warnings. Some applications (e.g., Chrome and Outlook) were also crashing unexpectedly.

---

## 🔍 Troubleshooting Steps

| Step | Action/Command | Result | Interpretation |
|------|----------------|--------|----------------|
| 1 | Checked disk usage via **Settings → System → Storage** | C:\ drive at 99% usage | Disk is critically full |
| 2 | Opened **File Explorer → This PC** | Red bar on C:\ drive | Visual confirmation of low disk space |
| 3 | Opened **Storage Sense** under Settings | Several GBs used by Temporary Files | Possible to recover space automatically |
| 4 | Ran `cleanmgr` as admin | Cleanup options loaded | Can delete temp files, recycle bin, old Windows files |
| 5 | Checked `C:\Users\%USERNAME%\Downloads` | 15+ GB of old files | User storage hogging space |
| 6 | Opened `WinDirStat` or `TreeSize Free` | Found large log files in `C:\ProgramData\...` | Hidden files taking up disk space |

---

## 🧩 Root Cause
The C:\ drive was nearly full due to a combination of:
- Accumulated temporary files and system cache
- Large files in Downloads and Videos folders
- Log files from applications not set to auto-clean

---

## 🛠️ Solution Applied

       1. Cleared unnecessary files using Disk Cleanup:
       ``powershell

       cleanmgr /verylowdisk

        Enabled Storage Sense to run automatically every week:

        Start → Settings → System → Storage → Storage Sense → Enable

        Deleted user files from:

        Downloads

        Videos

        AppData\Local\Temp

        Uninstalled unused applications via:

        Control Panel → Programs and Features

        Created a scheduled task to clear temp files monthly.

## ✅ Final Result

    25+ GB of disk space recovered

    User can save files and install updates normally

    No more disk space warnings

    PC performance improved

## 📌 Recommendations

    Educate users to periodically clean Downloads and Temp folders

    Use WinDirStat or TreeSize for deeper storage analysis

    Consider partitioning or adding a secondary drive for user data

    Enable Storage Sense as default on all endpoints

✅ Logged and resolved by: [Your Name]
🗓️ Date: [Insert Date]
🖥️ System: Windows 11 Pro – Build [e.g., 22631.3155]
