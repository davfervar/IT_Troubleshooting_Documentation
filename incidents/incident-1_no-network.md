# 🛠️ IT Incident Report: Network Connectivity Issue on Ubuntu VM

## 📌 Incident Overview
- **Title:** Loss of Internet Connectivity  
- **Environment:** Ubuntu 22.04 Virtual Machine (VirtualBox)  
- **User Impact:** Unable to browse the web, ping external IPs, or resolve domains.

---

## 🧾 Problem Description
The Ubuntu VM experienced a complete network outage. The user reported no internet access: websites failed to load, and even pinging external IP addresses (like `8.8.8.8`) returned errors.

---

## 🔍 Troubleshooting Steps

| Step | Command | Output | Interpretation |
|------|---------|--------|----------------|
| 1 | `ip a` | Only loopback (127.0.0.1); `enp0s3` is DOWN | Network interface is disabled |
| 2 | `ip route` | *No output* | No default gateway; routing table is empty |
| 3 | `ping 127.0.0.1` | Success | Local TCP/IP stack is working |
| 4 | `ping 8.8.8.8` | `Network is unreachable` | No route to the internet |
| 5 | `ping google.com` | `Temporary failure in name resolution` | DNS not functioning due to no internet |
| 6 | `cat /etc/resolv.conf` | `127.0.0.53`, managed by systemd | DNS setup appears normal; root issue is networking |

---

## 🧩 Root Cause
The primary network interface `enp0s3` was manually disabled using the following command:

sudo ip link set enp0s3 down

Without an active interface, the system could not obtain an IP address or default route.



## 🛠️ Solution Applied

Re-enabled the network interface using:

sudo ip link set enp0s3 up

DHCP automatically assigned a valid IP address and default gateway. Network functionality was restored.


## ✅ Final Result

    Internet connectivity successfully restored

    DNS resolution functional

    System can access external websites and respond to ping requests

## 📌 Recommendations

    Avoid manually disabling network interfaces unless troubleshooting.

    Use nmcli or GUI-based network management tools for interface control.

    Consider enabling systemd-networkd or NetworkManager to manage interfaces more reliably.

✅ Logged and resolved by: David Vargas
🗓️ Date: 7/17/2025
