# 🛠️ Incident 1: No Internet Connection (Ubuntu VM)

## 🧾 Problem Description

This incident involved a network outage on an **Ubuntu virtual machine**. The system was unable to access websites or respond to external ping requests, suggesting a deeper connectivity issue.

---

## 🔍 Troubleshooting Steps

| Step | Command              | Output                                                                 | Interpretation                                 |
|------|----------------------|------------------------------------------------------------------------|------------------------------------------------|
| 1    | `ip a`               | Only loopback interface (127.0.0.1) active. `enp0s3` is **DOWN**.      | No valid IP assigned; network interface is down. |
| 2    | `ip route`           | *No output*                                                            | No default route (gateway) is configured.     |
| 3    | `ping 127.0.0.1`     | Responds successfully                                                  | Local TCP/IP stack is functioning.            |
| 4    | `ping 8.8.8.8`       | `Network is unreachable`                                               | No external connectivity or default route.    |
| 5    | `ping google.com`    | `Temporary failure in name resolution`                                | DNS resolution failed due to lack of network. |
| 6    | `cat /etc/resolv.conf` | Configured with `127.0.0.53` (systemd-resolved)                      | DNS config looks correct, but network is down.|

---

## 🧩 Root Cause

    The primary network interface `enp0s3` was found to be **manually disabled**, likely due to a misconfiguration or a user action.

    ``bash
    sudo ip link set enp0s3 down

## 🛠️ Solution Applied

    The interface was re-enabled using the following command:

    sudo ip link set enp0s3 up


## ✅ Final Result

    Network connectivity was restored.

    The system was able to:
 
    Obtain a valid IP address

    Access external websites

    Resolve domain names via DNS

This issue highlights the importance of checking interface status and routing configuration early in the troubleshooting process.


✅ Logged and resolved by: David Vargas 🗓️ Date: 7/17/2025 🖥️ System: Ubuntu - Linux
