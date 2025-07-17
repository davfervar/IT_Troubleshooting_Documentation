🛠️ IT Incident 1 Report: Network Connectivity Issue on Ubuntu VM
📌 Incident Overview

Title: Loss of Internet Connectivity
Environment: Ubuntu 22.04 Virtual Machine (VirtualBox)
User Impact: Unable to browse the web, ping external IPs, or resolve domains.
🧾 Problem Description

The Ubuntu VM was experiencing a full network outage. The user reported inability to access the internet. No webpages would load, and pinging known IPs (like 8.8.8.8) failed.
🔍 Troubleshooting Steps
Step	Command	Output	Interpretation
1	ip a	Only loopback (127.0.0.1); enp0s3 is DOWN	Network interface disabled
2	ip route	No output	No routes configured; no default gateway
3	ping 127.0.0.1	Success	Local stack is working
4	ping 8.8.8.8	Network is unreachable	No route to internet
5	ping google.com	Temporary failure in name resolution	No DNS; due to no internet
6	cat /etc/resolv.conf	Shows 127.0.0.53; managed by systemd	Normal setup; DNS not the root cause
🧩 Root Cause

The network interface enp0s3 was manually disabled, possibly due to misconfiguration or user error. Without an active interface, no IP or route is assigned.

Command that caused the issue:

sudo ip link set enp0s3 down

🛠️ Solution Applied

The interface was re-enabled with:

sudo ip link set enp0s3 up

Afterward, DHCP assigned an IP and route automatically.
✅ Outcome

    Internet access restored

    DNS resolution working

    All services functional

📌 Recommendations

    Avoid manually disabling interfaces unless required.

    Use nmcli or network manager for safer interface control.

    Consider enabling systemd-networkd or NetworkManager for automatic recovery.
