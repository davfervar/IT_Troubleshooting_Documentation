import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import platform
import socket
from datetime import datetime

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "2", host]
    try:
        subprocess.check_output(command, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def check_dns(domain="google.com"):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def run_diagnostics():
    results = []
    log = ""

    tests = {
        "Localhost (127.0.0.1)": ping("127.0.0.1"),
        "Default Gateway (192.168.1.1)": ping("192.168.1.1"),
        "Public IP (8.8.8.8)": ping("8.8.8.8"),
        "DNS Resolution (google.com)": check_dns()
    }

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log += f"{timestamp} - Network Diagnostic Results\n"

    for test, result in tests.items():
        status = "✅ OK" if result else "❌ FAIL"
        line = f"{test}: {status}"
        results.append(line)
        log += f"{line}\n"

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "\n".join(results))
    save_log(log)

def save_log(log_text):
    with open("network_diagnostic_gui_log.txt", "a") as file:
        file.write(log_text + "\n\n")

# GUI setup
window = tk.Tk()
window.title("Network Diagnostic Tool")
window.geometry("500x350")
window.resizable(False, False)

label = tk.Label(window, text="Click the button to run network diagnostics", font=("Arial", 12))
label.pack(pady=10)

button = tk.Button(window, text="Run Diagnostics", command=run_diagnostics, font=("Arial", 11), bg="#4CAF50", fg="white")
button.pack(pady=5)

output_text = scrolledtext.ScrolledText(window, width=60, height=12, font=("Consolas", 10))
output_text.pack(padx=10, pady=10)

window.mainloop()
