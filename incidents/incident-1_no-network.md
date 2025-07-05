# 🛠 Incident 1: No Internet Connection

## 🧾 Problem Description

This incident was present in a network outage on an Ubuntu virtual machine. The system was unable to access websites or respond to external ping requests.

---

## 🔍 Troubleshooting

| Step | Command | Output | Interpretation |
|------|---------|--------|----------------|
| 1 |    `ip a` | Only loopback interface active (`127.0.0.1`). `enp0s3` is DOWN. | No valid IP assigned; interface is down. |
| 2 |   `ip route` | No output | No default route is configured. |
| 3 | `ping 127.0.0.1` | Responds successfully | Local TCP/IP stack is functioning. |
| 4 | `ping 8.8.8.8` | "Network is unreachable" | No external connectivity or gateway. |
| 5 | `ping google.com` | "Temporary failure in name resolution" | DNS resolution failed due to no internet access. |
| 6 | `cat /etc/resolv.conf` | Configured with `127.0.0.53`, managed by systemd-resolved | DNS appears correctly configured, but network is down. |

---

## 🧩 Root Cause

The primary network interface `enp0s3` was manually disabled using:

```bash
sudo ip link set enp0s3 down

🛠 Solution Applied

The issue was resolved by re-enabling the interface with:

sudo ip link set enp0s3 up

✅ Final Result

Connectivity was successfully restored. The system can now access external websites and resolve domain names via DNS.
