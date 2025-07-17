

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
Step	Action/Command	Result	Interpretation
1	ping 127.0.0.1	Success	Local TCP/IP stack working
2	ping 8.8.8.8	Success	Internet connection is active
3	ping google.com	Fails with "Ping request could not find host"	DNS resolution failing
4	ipconfig /all	Shows DNS set to static IP (e.g., 192.168.0.5)	Misconfigured DNS
5	nslookup google.com	Timed out or returns error	Confirms DNS is not responding
6	Checked Network Settings → IPv4 Properties	DNS set manually	Incorrect or unreachable DNS server

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
