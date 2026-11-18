
#!/usr/bin/env python3
import socket
import requests
import time

def is_port_open(ip, port, timeout=5):
    """
    Check if a TCP port on the given IP is open.
    Returns True if the connection succeeds, otherwise False.
    """
    try:
        with socket.create_connection((ip, port), timeout):
            return True
    except Exception:
        return False

def check_ports(ip):
    """
    Returns a tuple of booleans indicating whether port 80 and port 22 are open.
    """
    port_80_open = is_port_open(ip, 80)
    port_22_open = is_port_open(ip, 22)
    return port_80_open, port_22_open

def main():
    # Replace with your server's public IP address.
    server_ip = "196.207.24.206"
    # Create a persistent session for HTTP connections
    session = requests.Session()
    print(f"Monitoring server {server_ip} for open ports 80 and 22...")

    try:
        while True:
            open80, open22 = check_ports(server_ip)
            if open80 and open22:
                try:
                    # Establish an HTTP connection by sending a GET request.
                    response = session.get(f"http://{server_ip}", timeout=5)
                    print(f"[{time.ctime()}] HTTP GET successful, status code: {response.status_code}")
                except requests.RequestException as err:
                    print(f"[{time.ctime()}] HTTP connection error: {err}")
            else:
                print(f"[{time.ctime()}] Conditions not met: Port 80 open: {open80}, Port 22 open: {open22}")
            
            # Wait for a short period before checking again.
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nExiting monitoring loop.")

if __name__ == "__main__":
    main()

