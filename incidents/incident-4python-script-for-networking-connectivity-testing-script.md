# 🐍 IT Incident Report: Python Network Diagnostic Script – Windows 11

## 📌 Incident Overview
- **Title:** Python Script for Automated Network Troubleshooting  
- **Environment:** Windows 11 Pro x64  
- **Use Case:** Helpdesk or system administrators can quickly diagnose connectivity and DNS issues using a simple Python tool.

---

## 🧾 Problem Description
Manual troubleshooting of network issues can be time-consuming. This script aims to automate common checks such as:
- Local interface availability
- Gateway reachability
- Internet access
- DNS resolution

---

## 🛠️ Python Script: `network_diagnostic.py`

-----> [script download](scripts/network_diagnostic.py)

## 🧪 Sample Output (Console)
    
    🔍 Starting network diagnostics...
    
    Localhost (127.0.0.1): ✅ OK  
    Default Gateway (192.168.1.1): ✅ OK  
    Public IP (8.8.8.8): ❌ FAIL  
    DNS Resolution (google.com): ❌ FAIL  

    📄 Results saved to 'network_diagnostic_log.txt'

## ✅ Final Result

    Script correctly identifies whether issues are local, gateway-related, DNS-based or full internet outage.

    Outputs a readable summary in console and saves a log file for Helpdesk reference.

✅ Logged and created by: David Vargas
🗓️ Date: 7/17/2025
📁 File: network_diagnostic.py
