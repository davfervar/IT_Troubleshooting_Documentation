

# 🌐 IT Incident Report: DNS Misconfiguration – Windows 11

## 📌 Incident Overview
- **Title:** DNS Misconfiguration Causing Internet Issues  
- **Environment:** Windows 11 Pro x64  
- **User Impact:** User can access some websites via IP but cannot resolve domain names (e.g., google.com)

---

## 🧾 Problem Description
User reported that websites were not loading in any browser. Error messages included:

> *“DNS server isn’t responding”*  
> *“Hmm… can’t reach this page”*

However, when testing via IP addresses, some services were accessible. For example:

``powershell
ping 8.8.8.8  → Success  
ping google.com  → Failed (host not found)

## 🔍 Troubleshooting Steps

| Step | Action/Command | Result | Interpretation |
|------|----------------|--------|----------------|
| 1 | Checked disk usage via **Settings → System → Storage** | C:\ drive at 99% usage | Disk is critically full |
| 2 | Opened **File Explorer → This PC** | Red bar on C:\ drive | Visual confirmation of low disk space |
| 3 | Opened **Storage Sense** under Settings | Several GBs used by Temporary Files | Possible to recover space automatically |
| 4 | Ran `cleanmgr` as admin | Cleanup options loaded | Can delete temp files, recycle bin, old Windows files |
| 5 | Checked `C:\Users\%USERNAME%\Downloads` | 15+ GB of old files | User storage hogging space |
| 6 | Opened `WinDirStat` or `TreeSize Free` | Found large log files in `C:\ProgramData\...` | Hidden files taking up disk space |

## 🧩 Root Cause

    The system was using a static DNS IP (192.168.0.5) that was either:

    Not reachable

    Misconfigured

    Not running a DNS service

    This prevented name resolution for all domains, despite having working internet access.

## 🛠️ Solution Applied

    Opened Control Panel → Network and Internet → Network Connections

    Right-clicked the active network adapter → Properties

    Selected Internet Protocol Version 4 (TCP/IPv4) → Properties

    Changed DNS settings from manual to automatic (Obtain DNS server address automatically)

        Alternatively, entered public DNS manually:

    Preferred DNS: 8.8.8.8  
    Alternate DNS: 1.1.1.1

    Flushed DNS cache and renewed IP:

    ipconfig /flushdns
    ipconfig /release
    ipconfig /renew

    Retested with:

    ping google.com → Success  
    nslookup google.com → Returns IP address

## ✅  Final Result


    DNS resolution restored

    User can browse the internet normally

    No more errors in browser

    System resolves both internal and external domains

## 📌 Recomendatios

    Avoid setting static DNS manually unless required by the network

    Use reliable public DNS like Google (8.8.8.8) or Cloudflare (1.1.1.1)

    Train users to report "DNS server not responding" errors promptly

    Consider using DHCP reservations and enforced DNS policies via Group Policy in corporate environments

✅ Logged and resolved by: [Your Name]
🗓️ Date: [Insert Date]
🖥️ System: Windows 11 Pro – Build [e.g., 22631.3155]
