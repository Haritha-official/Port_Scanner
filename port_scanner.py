import socket
import threading
import queue
import csv
from datetime import datetime
import time

class PortScanner:
    def __init__(self, host, start_port, end_port, threads=100):
        self.host = host
        self.start_port = start_port
        self.end_port = end_port
        self.threads = threads
        self.open_ports = []
        self.lock = threading.Lock()
        self.print_lock = threading.Lock()
        self.results = []
        self.start_time = None

    def scan_port(self, port):
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            # Attempt connection
            result = sock.connect_ex((self.host, port))
            
            if result == 0:
                # Get service name
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                
                # Grab banner
                banner = ""
                try:
                    sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                except:
                    try:
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    except:
                        pass
                
                # Add to results
                with self.lock:
                    self.open_ports.append(port)
                    self.results.append({
                        'port': port,
                        'service': service,
                        'banner': banner
                    })
                
                # Print progress
                with self.print_lock:
                    print(f"Port {port}/open | Service: {service} | Banner: {banner[:50]}...")
            
            sock.close()
            
        except Exception as e:
            with self.print_lock:
                print(f"Error scanning port {port}: {str(e)}")

    def worker(self, port_queue):
        while True:
            port = port_queue.get()
            if port is None:
                break
            self.scan_port(port)
            port_queue.task_done()

    def run(self):
        # Resolve hostname
        try:
            self.ip = socket.gethostbyname(self.host)
            print(f"\nResolved {self.host} → {self.ip}")
        except socket.gaierror:
            print("\nError: Hostname could not be resolved")
            return
        
        # Create port queue
        port_queue = queue.Queue()
        for port in range(self.start_port, self.end_port + 1):
            port_queue.put(port)
        
        # Start worker threads
        print(f"\nStarting scan with {self.threads} threads...")
        self.start_time = time.time()
        
        workers = []
        for _ in range(self.threads):
            worker_thread = threading.Thread(target=self.worker, args=(port_queue,))
            worker_thread.start()
            workers.append(worker_thread)
        
        # Wait for queue to empty
        port_queue.join()
        
        # Stop workers
        for _ in range(self.threads):
            port_queue.put(None)
        for worker in workers:
            worker.join()
        
        # Print results
        self.print_results()
        
        # Save results
        self.save_results()

    def print_results(self):
        duration = time.time() - self.start_time
        print("\n" + "="*50)
        print("SCAN COMPLETE")
        print("="*50)
        print(f"Host: {self.host} ({self.ip})")
        print(f"Port range: {self.start_port}-{self.end_port}")
        print(f"Open ports: {len(self.open_ports)}")
        print(f"Time taken: {duration:.2f} seconds")
        print("\nOpen Ports:")
        
        for port in sorted(self.open_ports):
            print(f"  {port}/open")
        
        print("\nDetailed Results:")
        for result in sorted(self.results, key=lambda x: x['port']):
            print(f"\nPort: {result['port']}")
            print(f"Service: {result['service']}")
            print(f"Banner: {result['banner']}")

    def save_results(self):
        filename = f"scan_{self.host}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['port', 'service', 'banner']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in sorted(self.results, key=lambda x: x['port']):
                writer.writerow(result)
        print(f"\nResults saved to {filename}")

if __name__ == "__main__":
    print("🔍 Port Scanner - Advanced Edition")
    print("=====================================")
    
    # Get user input
    host = input("Enter host to scan: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    threads = int(input("Number of threads (default 100): ") or 100)
    
    # Validate port range
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Error: Invalid port range (1-65535)")
        exit()
    
    # Run scanner
    scanner = PortScanner(host, start_port, end_port, threads)
    scanner.run()