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
