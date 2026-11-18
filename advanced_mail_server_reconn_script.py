
#!/usr/bin/env python3
import sys
import dns.resolver
import socket
import threading

# Common mail server ports
MAIL_PORTS = [25, 465, 587, 110, 995, 143, 993]

def resolve_domain(domain, record_type='A'):
    """Attempt to resolve the given domain name for the specified record type."""
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [rdata.to_text() for rdata in answers]
    except Exception:
        return None

def scan_ports(host):
    """Scan common mail-related ports on the given host."""
    open_ports = []
    
    def check_port(port):
        """Attempt to connect to a port to check if it's open."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            if s.connect_ex((host, port)) == 0:
                open_ports.append(port)

    # Multi-threading for faster scanning
    threads = []
    for port in MAIL_PORTS:
        thread = threading.Thread(target=check_port, args=(port,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return open_ports

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <country_code>")
        sys.exit(1)

    country = sys.argv[1].strip()
    base_domain = f"mail.mod.go.{country}"
    print(f"Scanning domain: {base_domain}\n")

    # 1. Resolve the base domain itself.
    base_ips = resolve_domain(base_domain, 'A')
    if base_ips:
        print(f"{base_domain} resolves to: {base_ips}")
    else:
        print(f"Could not resolve {base_domain}.")

    # 2. Try a list of common mail server subdomains under the base domain.
    common_subs = ["mx", "smtp", "imap", "pop", "mail1", "mail2", "exchange"]
    
    print("\nChecking common mail server subdomains:")
    found_servers = {}
    
    for sub in common_subs:
        full_domain = f"{sub}.{base_domain}"
        ips = resolve_domain(full_domain, 'A')
        if ips:
            found_servers[full_domain] = ips
            print(f"  {full_domain} -> {ips}")

    # 3. Get MX records
    print("\nMX records for the base domain:")
    mx_records = resolve_domain(base_domain, 'MX')
    if mx_records:
        for record in mx_records:
            print("  ", record)
            mx_host = record.split()[-1]  # Extract hostname from MX record
            mx_ips = resolve_domain(mx_host, 'A')
            if mx_ips:
                found_servers[mx_host] = mx_ips
    else:
        print("  No MX records found for the base domain.")

    # 4. Scan for open mail server ports
    print("\nScanning for open mail server ports:")
    for server, ips in found_servers.items():
        for ip in ips:
            print(f"  Scanning {server} ({ip})...")
            open_ports = scan_ports(ip)
            if open_ports:
                print(f"    Open ports: {open_ports}")
            else:
                print("    No open mail-related ports found.")

if __name__ == "__main__":
    main()
