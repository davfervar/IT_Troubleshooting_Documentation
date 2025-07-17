# -*- coding: utf-8 -*-

"""
IT-Toolkit: Network Tools for Technicians
Version 3.3 - English Language Version
"""

import subprocess
import re
import socket
import threading
import os
import urllib.request
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import ttk, font, scrolledtext, messagebox
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFont as font
    import ScrolledText as scrolledtext

# --- GLOBAL CONFIGURATION ---
# This STARTUP_INFO object prevents cmd windows from appearing
STARTUP_INFO = subprocess.STARTUPINFO()
STARTUP_INFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
STARTUP_INFO.wShowWindow = subprocess.SW_HIDE

# --- BACKEND FUNCTIONS (LOGIC) ---

def run_command(command):
    """Executes a system command and returns its output."""
    try:
        return subprocess.check_output(command, shell=True, text=True, stderr=subprocess.PIPE, startupinfo=STARTUP_INFO)
    except Exception as e:
        return f"Error executing command: {e}"

def get_network_info():
    """Gets detailed network information using 'ipconfig /all'."""
    info = {
        "ipv4": "Not found",
        "gateway": "Not found",
        "mac_address": "Not found",
        "dhcp_server": "N/A",
        "dns_servers": []
    }
    output = run_command("ipconfig /all")
    
    # Find the active adapter section (the one with a gateway)
    active_adapter_section = None
    if "Default Gateway" in output or "Puerta de enlace predeterminada" in output:
        adapters = re.split(r'\n\s*\n', output)
        for adapter in adapters:
            if re.search(r"(?:Default Gateway|Puerta de enlace predeterminada)[\s.:]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", adapter):
                active_adapter_section = adapter
                break
    
    if active_adapter_section:
        # Search for info only within the active adapter's section
        ipv4_match = re.search(r"(?:IPv4 Address|Dirección IPv4)[\s.:]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", active_adapter_section)
        if ipv4_match: info["ipv4"] = ipv4_match.group(1).strip()

        gateway_match = re.search(r"(?:Default Gateway|Puerta de enlace predeterminada)[\s.:]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", active_adapter_section)
        if gateway_match: info["gateway"] = gateway_match.group(1).strip()
        
        mac_match = re.search(r"(?:Physical Address|Dirección física)[\s.:]+([0-9A-Fa-f-]+)", active_adapter_section)
        if mac_match: info["mac_address"] = mac_match.group(1).strip()
        
        dhcp_match = re.search(r"(?:DHCP Server|Servidor DHCP)[\s.:]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", active_adapter_section)
        if dhcp_match: info["dhcp_server"] = dhcp_match.group(1).strip()
        
        dns_matches = re.findall(r"(?:DNS Servers|Servidores DNS)[\s.:]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", active_adapter_section)
        if dns_matches: info["dns_servers"] = [dns.strip() for dns in dns_matches]

    return info

def get_public_ip():
    """Gets the public IP address."""
    try:
        return urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode('utf-8')
    except:
        return "Could not retrieve"

def ping_host(hostname):
    """Pings a host and returns latency."""
    output = run_command(f'ping -n 2 {hostname}')
    avg_latency_match = re.search(r"(?:Media|Average) = (\d+)", output)
    if avg_latency_match: return True, f"{avg_latency_match.group(1)} ms"
    if "TTL=" in output: return True, "Reply OK"
    return False, "Host unreachable"

def trace_route(hostname, output_widget):
    """Runs tracert and displays results in real-time."""
    output_widget.delete('1.0', tk.END)
    output_widget.insert(tk.END, f"--- Tracing route to {hostname} ---\n\n")
    try:
        process = subprocess.Popen(['tracert', hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, startupinfo=STARTUP_INFO, bufsize=1, universal_newlines=True)
        for line in iter(process.stdout.readline, ''):
            output_widget.insert(tk.END, line)
            output_widget.see(tk.END)
            output_widget.update_idletasks()
        process.stdout.close()
        process.wait()
    except Exception as e:
        output_widget.insert(tk.END, f"\nError running tracert: {e}")

def scan_ports(hostname, ports_str, output_widget):
    """Scans ports on a host."""
    output_widget.delete('1.0', tk.END)
    output_widget.insert(tk.END, f"--- Scanning ports on {hostname} ---\n")
    try:
        target_ip = socket.gethostbyname(hostname)
        output_widget.insert(tk.END, f"Resolved IP: {target_ip}\n\n")
        ports = []
        # Parse the port string (e.g., "80, 443, 8080-8085")
        for part in ports_str.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part.strip()))

        for port in ports:
            output_widget.update_idletasks()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = sock.connect_ex((target_ip, port))
            status = "Open" if result == 0 else "Closed"
            output_widget.insert(tk.END, f"Port {port}: {status}\n", 'ok' if status == "Open" else 'fail')
            sock.close()
    except socket.gaierror:
        output_widget.insert(tk.END, "Error: Could not resolve hostname.\n", 'fail')
    except Exception as e:
        output_widget.insert(tk.END, f"Error: {e}\n", 'fail')

def send_wol_packet(mac_address):
    """Sends a Wake-on-LAN packet."""
    try:
        mac_address = mac_address.replace('-', '').replace(':', '')
        if len(mac_address) != 12:
            messagebox.showerror("Error", "Invalid MAC address format. Must be 12 hex characters.")
            return
        data = bytes.fromhex('FF' * 6 + mac_address * 16)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data, ('<broadcast>', 9))
        messagebox.showinfo("Success", f"Wake-on-LAN packet sent to {mac_address}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not send packet: {e}")


# --- MAIN APPLICATION CLASS (GUI) ---

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Toolkit v3.3")
        self.root.geometry("800x600")
        
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", rowheight=25, font=('Helvetica', 10))
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.create_dashboard_tab()
        self.create_tools_tab()
        self.create_commands_tab()
        self.create_info_tab()

    def create_threaded_action(self, action, *args):
        """Generic function to run actions in a separate thread."""
        thread = threading.Thread(target=action, args=args)
        thread.daemon = True
        thread.start()

    # --- Tab 1: Dashboard ---
    def create_dashboard_tab(self):
        diag_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(diag_frame, text='Dashboard')
        
        ttk.Label(diag_frame, text="Network Control Panel", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        tree_frame = ttk.Frame(diag_frame)
        tree_frame.pack(fill='both', expand=True)

        self.diag_tree = ttk.Treeview(tree_frame, columns=("param", "value", "status"), show="headings")
        self.diag_tree.heading("param", text="Parameter")
        self.diag_tree.heading("value", text="Value")
        self.diag_tree.heading("status", text="Status")
        
        self.diag_tree.column("param", width=200)
        self.diag_tree.column("value", width=300)
        self.diag_tree.column("status", width=100, anchor='center')
        self.diag_tree.pack(fill='both', expand=True)

        self.diag_tree.tag_configure('ok', foreground='green')
        self.diag_tree.tag_configure('fail', foreground='red')
        self.diag_tree.tag_configure('info', foreground='blue')

        self.diag_items = {}
        tests = {
            "public_ip": "Public IP Address", "ipv4": "Local IP Address (IPv4)",
            "mac": "Physical Address (MAC)", "gateway": "Default Gateway",
            "dhcp": "DHCP Server", "dns": "DNS Servers",
            "separator": "---", "ping_gateway": "Ping Default Gateway",
            "ping_internet": "Ping Internet (8.8.8.8)"
        }
        for key, text in tests.items():
            if "separator" in key:
                self.diag_items[key] = self.diag_tree.insert("", "end", values=("---", "---", "---"))
            else:
                self.diag_items[key] = self.diag_tree.insert("", "end", values=(text, "Pending...", ""))

        run_button = ttk.Button(diag_frame, text="Run Diagnostics", command=lambda: self.create_threaded_action(self.run_quick_diag))
        run_button.pack(pady=20)

    def update_diag_item(self, key, value, status="", tag='info'):
        item_id = self.diag_items[key]
        current_param = self.diag_tree.item(item_id, "values")[0]
        self.diag_tree.item(item_id, values=(current_param, value, status), tags=(tag,))

    def run_quick_diag(self):
        # Clear table
        for key in self.diag_items:
            if "separator" not in key:
                self.update_diag_item(key, "Testing...", "")

        # Get network information
        net_info = get_network_info()
        self.update_diag_item("ipv4", net_info["ipv4"], "OK", "info")
        self.update_diag_item("mac", net_info["mac_address"], "OK", "info")
        self.update_diag_item("gateway", net_info["gateway"], "OK", "info")
        self.update_diag_item("dhcp", net_info["dhcp_server"], "OK", "info")
        dns_str = ", ".join(net_info["dns_servers"]) if net_info["dns_servers"] else "Not found"
        self.update_diag_item("dns", dns_str, "OK", "info")

        # Get public IP
        public_ip = get_public_ip()
        public_ip_ok = "Could not" not in public_ip
        self.update_diag_item("public_ip", public_ip, "✅" if public_ip_ok else "❌", 'ok' if public_ip_ok else 'fail')

        # Ping tests
        gateway_ip = net_info["gateway"]
        if gateway_ip != "Not found":
            gw_ok, gw_res = ping_host(gateway_ip)
            self.update_diag_item("ping_gateway", gw_res, "✅" if gw_ok else "❌", 'ok' if gw_ok else 'fail')
        else:
            self.update_diag_item("ping_gateway", "No gateway found", "❌", 'fail')

        inet_ok, inet_res = ping_host("8.8.8.8")
        self.update_diag_item("ping_internet", inet_res, "✅" if inet_ok else "❌", 'ok' if inet_ok else 'fail')

    # --- Tab 2: Network Tools ---
    def create_tools_tab(self):
        tools_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tools_frame, text='Network Tools')
        
        trace_frame = ttk.LabelFrame(tools_frame, text="Traceroute", padding=10)
        trace_frame.pack(fill='x', pady=5)
        ttk.Label(trace_frame, text="Host or IP:").grid(row=0, column=0, padx=5, pady=5)
        trace_host = ttk.Entry(trace_frame)
        trace_host.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        trace_frame.columnconfigure(1, weight=1)
        
        scan_frame = ttk.LabelFrame(tools_frame, text="Port Scanner", padding=10)
        scan_frame.pack(fill='x', pady=5)
        ttk.Label(scan_frame, text="Host or IP:").grid(row=0, column=0, padx=5, pady=5)
        scan_host = ttk.Entry(scan_frame)
        scan_host.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(scan_frame, text="Ports (e.g. 80,443,100-200):").grid(row=1, column=0, padx=5, pady=5)
        scan_ports_entry = ttk.Entry(scan_frame)
        scan_ports_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        scan_frame.columnconfigure(1, weight=1)

        wol_frame = ttk.LabelFrame(tools_frame, text="Wake-on-LAN", padding=10)
        wol_frame.pack(fill='x', pady=5)
        ttk.Label(wol_frame, text="MAC Address:").grid(row=0, column=0, padx=5, pady=5)
        wol_mac = ttk.Entry(wol_frame)
        wol_mac.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        wol_button = ttk.Button(wol_frame, text="Send WOL Packet", command=lambda: send_wol_packet(wol_mac.get()))
        wol_button.grid(row=0, column=2, padx=5, pady=5)
        wol_frame.columnconfigure(1, weight=1)

        output_frame = ttk.Frame(tools_frame)
        output_frame.pack(fill='both', expand=True, pady=10)
        output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Courier New", 9))
        output_text.pack(fill='both', expand=True)
        output_text.tag_config('ok', foreground='green')
        output_text.tag_config('fail', foreground='red')

        trace_button = ttk.Button(trace_frame, text="Trace Route", command=lambda: self.create_threaded_action(trace_route, trace_host.get(), output_text))
        trace_button.grid(row=0, column=2, padx=5, pady=5)
        
        scan_button = ttk.Button(scan_frame, text="Scan Ports", command=lambda: self.create_threaded_action(scan_ports, scan_host.get(), scan_ports_entry.get(), output_text))
        scan_button.grid(row=1, column=2, padx=5, pady=5)

    # --- Tab 3: Quick Commands ---
    def create_commands_tab(self):
        cmd_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(cmd_frame, text='Quick Commands')
        
        def run_and_show(command, title):
            output = run_command(command)
            messagebox.showinfo(title, output if output else "Command executed successfully.")

        btn1 = ttk.Button(cmd_frame, text="Release & Renew IP Address", command=lambda: self.create_threaded_action(run_and_show, "ipconfig /release & ipconfig /renew", "IP Renew Result"))
        btn1.pack(pady=10, fill='x', padx=20, ipady=10)
        
        btn2 = ttk.Button(cmd_frame, text="Flush DNS Cache", command=lambda: self.create_threaded_action(run_and_show, "ipconfig /flushdns", "Flush DNS Result"))
        btn2.pack(pady=10, fill='x', padx=20, ipady=10)
    
    # --- Tab 4: Local Info ---
    def create_info_tab(self):
        info_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(info_frame, text='Local Info')
        
        output_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, font=("Courier New", 9))
        output_text.pack(fill='both', expand=True, pady=10)

        def show_info(command, title):
            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, f"--- {title} ---\n\n")
            output_text.insert(tk.END, run_command(command))

        btn_frame = ttk.Frame(info_frame)
        btn_frame.pack(fill='x', side='bottom', pady=5)
        
        btn_arp = ttk.Button(btn_frame, text="View ARP Table", command=lambda: show_info("arp -a", "ARP Table"))
        btn_arp.pack(side='left', expand=True, fill='x', padx=5)
        
        btn_netstat = ttk.Button(btn_frame, text="View Active Connections", command=lambda: show_info("netstat -an", "Active Connections"))
        btn_netstat.pack(side='left', expand=True, fill='x', padx=5)
        
        btn_ipconfig = ttk.Button(btn_frame, text="View Full IP Configuration", command=lambda: show_info("ipconfig /all", "Full IP Configuration"))
        btn_ipconfig.pack(side='left', expand=True, fill='x', padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()