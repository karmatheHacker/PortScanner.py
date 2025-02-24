import socket
import threading
import sys
from queue import Queue

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Alt"
}

port_queue = Queue()
open_ports = []
print_lock = threading.Lock()

def scan_port(host, port, timeout, verbose=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        if result == 0:
            banner = grab_banner(sock)
            service = COMMON_PORTS.get(port, "Unknown")
            with print_lock:
                open_ports.append((port, service, banner))
                print(f"Port {port} ({service}) is open. Banner: {banner}")
        elif verbose:
            with print_lock:
                print(f"Port {port} is closed")
        sock.close()
    except Exception as e:
        if verbose:
            with print_lock:
                print(f"Error scanning port {port}: {e}")

def grab_banner(sock):
    try:
        sock.send(b"GET / HTTP/1.1\r\n\r\n")
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return "No banner"

def worker(host, timeout, verbose):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(host, port, timeout, verbose)
        port_queue.task_done()

def ping_host(host):
    try:
        # Try to connect to a common port (e.g., port 80 for HTTP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((host, 80))  # Port 80 is commonly used for HTTP
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False

def main():
    if len(sys.argv) < 5:
        print("Usage: python port_scanner.py <host> <start_port> <end_port> <timeout> [--verbose] [--output <file>]")
        sys.exit(1)

    host = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    timeout = float(sys.argv[4])
    verbose = "--verbose" in sys.argv
    output_file = None
    if "--output" in sys.argv:
        output_file = sys.argv[sys.argv.index("--output") + 1]

    if start_port > end_port or start_port < 1 or end_port > 65535:
        print("Invalid port range. Please ensure start port is less than or equal to end port, and both are within 1-65535.")
        sys.exit(1)

    if not ping_host(host):
        print(f"Host {host} is unreachable. Exiting.")
        sys.exit(1)

    print(f"Scanning {host} from port {start_port} to {end_port}...\n")

    # Fill the queue with ports to scan
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Create and start threads
    threads = []
    for _ in range(100):  # Number of threads
        thread = threading.Thread(target=worker, args=(host, timeout, verbose))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    port_queue.join()

    # Print summary
    print("\nScan complete.")
    if open_ports:
        print("Open ports:")
        for port, service, banner in open_ports:
            print(f"Port {port} ({service}): {banner}")
        if output_file:
            with open(output_file, "w") as f:
                for port, service, banner in open_ports:
                    f.write(f"Port {port} ({service}): {banner}\n")
            print(f"Results saved to {output_file}")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
