# 🛠️ IT Incident Report: DNS Misconfiguration on Windows 11

## 📌 Incident Overview

- **Title:** DNS Not Resolving Domain Names  
- **Environment:** Windows 11 Pro (Build 22631.3155)  
- **User Impact:** User cannot browse the web or resolve domains, despite having internet connectivity.

---

## 🧾 Problem Description

A user reported that they could not open websites in any browser. Pinging known IP addresses (e.g., `8.8.8.8`) worked, but domain names like `google.com` would not resolve. Applications relying on domain names (such as Teams and Outlook) also failed to connect.

---

## 🔍 Troubleshooting Steps

| Step | Command/Action | Output | Interpretation |
|------|----------------|--------|----------------|
| 1 | `ping 127.0.0.1` | Success | Local TCP/IP stack is working |
| 2 | `ping 8.8.8.8` | Success | Internet connection is active |
| 3 | `ping google.com` | Ping request could not find host | DNS resolution is failing |
| 4 | `ipconfig /all` | DNS server set to `192.168.0.5` | Static DNS server configured |
| 5 | `nslookup google.com` | Timed out or error | DNS server is unreachable or misconfigured |
| 6 | Checked IPv4 settings in Control Panel | DNS set manually to 192.168.0.5 | DNS is not responding or is incorrect |

---

## 🧩 Root Cause

The computer had a manually configured DNS server (`192.168.0.5`) that was either offline, misconfigured, or non-existent. As a result, the system was unable to resolve domain names, even though the internet connection itself was functioning.

---

## 🛠️ Solution Applied

Reverted DNS settings to automatic, or used public DNS manually:

1. Opened:

Control Panel → Network and Internet → Network Connections


2. Right-clicked active adapter → **Properties**

3. Selected:

Internet Protocol Version 4 (TCP/IPv4) → Properties


4. Changed from:

Use the following DNS server addresses → to → Obtain DNS server address automatically


Or set:

Preferred DNS: 8.8.8.8
Alternate DNS: 1.1.1.1


5. Flushed DNS cache and renewed IP:
```powershell
ipconfig /flushdns
ipconfig /release
ipconfig /renew

✅ Final Result

    DNS resolution functional

    Browsers and apps working normally

    System can resolve both internal and external domains

📌 Recommendations

    Avoid manually setting DNS unless required for specific environments

    Prefer using public DNS (e.g., Google 8.8.8.8 or Cloudflare 1.1.1.1) if needed

    Use DHCP and Group Policy to manage DNS centrally in enterprise environments

    Include DNS checks in automated diagnostic scripts

✅ Logged and resolved by: David Vargas
🗓️ Date: 7/17/2025
