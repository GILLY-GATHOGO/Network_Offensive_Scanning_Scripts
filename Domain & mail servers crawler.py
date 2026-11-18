#How to run this is by typing python3 "Domain & mail servers crawler.py" ke  on the terminal or ug or tz 
#!/usr/bin/env python3
import sys
import dns.resolver

def resolve_domain(domain, record_type='A'):
    """Attempt to resolve the given domain name for the specified record type.
       Returns a list of IP addresses (or other record data) if found, or None.
    """
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [rdata.to_text() for rdata in answers]
    except Exception:
        return None

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
    common_subs = [
        "mx", "mx1", "mx2",
        "smtp", "smtp1", "smtp2",
        "imap", "pop",
        "mail1", "mail2",
        "exchange"
    ]

    print("\nChecking common mail server subdomains:")
    found = False
    for sub in common_subs:
        full_domain = f"{sub}.{base_domain}"
        ips = resolve_domain(full_domain, 'A')
        if ips:
            print(f"  {full_domain} -> {ips}")
            found = True

    if not found:
        print("  No additional subdomains resolved using the common prefixes.")

    # 3. Optionally, list the MX records for the base domain.
    print("\nMX records for the base domain:")
    mx_records = resolve_domain(base_domain, 'MX')
    if mx_records:
        for record in mx_records:
            # MX record data usually includes a preference and an exchange.
            print("  ", record)
    else:
        print("  No MX records found for the base domain.")

if __name__ == "__main__":
    main()
