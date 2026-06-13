#!/usr/bin/env python3
"""
Pure200Checker - A fast multi-threaded tool to filter alive subdomains
Author: Your Name
"""

import requests
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

BANNER = r"""
  ____               ____  ___   ___  ____ _               _             
 |  _ \ _   _ _ __ ___|_  / / _ \ / _ \/ ___| |__   ___  ___| | _____ _ __ 
 | |_) | | | | '__/ _ \ / / | | | | | | |   | '_ \ / _ \/ __| |/ / _ \ '__|
 |  __/| |_| | | |  __// /| |_| | |_| | |___| | | |  __/ (__|   <  __/ |   
 |_|    \__,_|_|  \___/_____\___/ \___/ \____|_| |_|\___|\___|_|\_\___|_|   
                                                                             
        Fast Multi-Threaded Subdomain Alive Checker | 200 OK Filter
"""

def parse_args():
    parser = argparse.ArgumentParser(
        description="Pure200Checker - A fast multi-threaded tool to filter alive subdomains",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-f", "--file",    required=True,      help="Path to the raw subdomains file (e.g., subs_raw.txt)")
    parser.add_argument("-o", "--output",  default="alive_subs.txt", help="Path to save the alive subdomains (default: alive_subs.txt)")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Timeout per request in seconds (default: 5)")
    parser.add_argument("-w", "--workers", type=int, default=20, help="Number of concurrent threads (default: 20)")
    parser.add_argument("--https",         action="store_true", help="Also try HTTPS if HTTP fails")
    parser.add_argument("--status-codes",  default="200",       help="Comma-separated status codes to accept (default: 200)")
    return parser.parse_args()


def check_subdomain(sub, timeout, try_https, accepted_codes):
    """Check if a subdomain returns an accepted HTTP status code."""
    protocols = ["http"]
    if try_https:
        protocols.append("https")

    for proto in protocols:
        url = f"{proto}://{sub}"
        try:
            response = requests.get(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers={"User-Agent": "Pure200Checker/1.0"}
            )
            if response.status_code in accepted_codes:
                return sub, response.status_code, url
        except requests.RequestException:
            continue

    return None, None, None


def main():
    print(BANNER)
    args = parse_args()

    # Parse accepted status codes
    try:
        accepted_codes = set(int(c.strip()) for c in args.status_codes.split(","))
    except ValueError:
        print("[-] Error: --status-codes must be a comma-separated list of integers (e.g., 200,301)")
        sys.exit(1)

    print(f"[*] Started at     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Input File     : {args.file}")
    print(f"[*] Output File    : {args.output}")
    print(f"[*] Threads        : {args.workers}")
    print(f"[*] Timeout        : {args.timeout}s")
    print(f"[*] HTTPS Fallback : {'Yes' if args.https else 'No'}")
    print(f"[*] Accepted Codes : {sorted(accepted_codes)}")
    print("-" * 55)

    # Load subdomains
    try:
        with open(args.file, "r") as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Error: File '{args.file}' not found!")
        sys.exit(1)

    if not subdomains:
        print("[-] No subdomains found in input file.")
        sys.exit(1)

    print(f"[+] Loaded {len(subdomains)} subdomains. Scanning...\n")

    # Clear / create output file
    open(args.output, "w").close()
    count = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(check_subdomain, sub, args.timeout, args.https, accepted_codes): sub
            for sub in subdomains
        }

        for future in as_completed(futures):
            sub, code, url = future.result()
            if sub:
                print(f"  [{code}] {url}")
                count += 1
                with open(args.output, "a") as out:
                    out.write(f"{url}\n")

    print("\n" + "-" * 55)
    print(f"[+] Scan complete!")
    print(f"[+] Found   : {count} alive subdomain(s)")
    print(f"[+] Saved to: {args.output}")
    print(f"[*] Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
