🐍 INCIDENTE 4 – Script en Python para diagnosticar conectividad en Windows

Te voy a dar:

    ✅ El caso simulado como incidente IT (formato .md para GitHub)

    🐍 Un script funcional en Python para Windows que:

        Verifica conectividad general (localhost, gateway, internet)

        Verifica si DNS está funcionando

        Muestra resultados claros en consola

        Opcionalmente guarda un log

📝 1. Documento .md listo para tu GitHub:

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

```python
import os
import platform
import socket
import subprocess
from datetime import datetime

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "2", host]
    try:
        subprocess.check_output(command)
        return True
    except subprocess.CalledProcessError:
        return False

def check_dns(domain="google.com"):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def log_result(message):
    with open("network_diagnostic_log.txt", "a") as log:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log.write(f"{timestamp} {message}\n")

def main():
    print("🔍 Starting network diagnostics...\n")

    tests = {
        "Localhost (127.0.0.1)": ping("127.0.0.1"),
        "Default Gateway (192.168.1.1)": ping("192.168.1.1"),
        "Public IP (8.8.8.8)": ping("8.8.8.8"),
        "DNS Resolution (google.com)": check_dns()
    }

    for test, result in tests.items():
        status = "✅ OK" if result else "❌ FAIL"
        print(f"{test}: {status}")
        log_result(f"{test}: {status}")

    print("\n📄 Results saved to 'network_diagnostic_log.txt'")

if __name__ == "__main__":
    main()

🧪 Sample Output (Console)

🔍 Starting network diagnostics...

Localhost (127.0.0.1): ✅ OK  
Default Gateway (192.168.1.1): ✅ OK  
Public IP (8.8.8.8): ❌ FAIL  
DNS Resolution (google.com): ❌ FAIL  

📄 Results saved to 'network_diagnostic_log.txt'

✅ Final Result

    Script correctly identifies whether issues are local, gateway-related, DNS-based or full internet outage.

    Outputs a readable summary in console and saves a log file for Helpdesk reference.

📌 Recommendations

    Include this script in Helpdesk USB kits or shared folders

    Train junior staff to run and interpret the results

    Can be extended to test VPN status, proxy, or corporate DNS as needed

    Package as .exe with pyinstaller for easy use by non-technical users

✅ Logged and created by: [Your Name]
🗓️ Date: [Insert Date]
📁 File: network_diagnostic.py
