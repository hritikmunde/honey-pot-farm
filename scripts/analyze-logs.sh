#!/usr/bin/env python3
import sys
import re
from collections import Counter

def analyze_log(filename):
    with open(filename) as f:
        content = f.read()
    
    # Extract data
    connections = re.findall(r'New connection: ([\d\.]+):', content)
    external_ips = [ip for ip in connections if not ip.startswith('10.0.')]
    
    login_attempts = re.findall(r"login attempt \[b'([^']+)'/b'([^']+)'\]", content)
    usernames = [u for u, p in login_attempts]
    passwords = [p for u, p in login_attempts]
    
    # Print results
    print(f"\n{'='*50}")
    print(f"Analysis: {filename}")
    print(f"{'='*50}")
    print(f"Total connections: {len(connections)}")
    print(f"External IPs: {len(external_ips)} unique: {len(set(external_ips))}")
    print(f"Login attempts: {len(login_attempts)}")
    
    print(f"\nTop 10 usernames:")
    for user, count in Counter(usernames).most_common(10):
        print(f"  {user}: {count}")
    
    print(f"\nTop 10 passwords:")
    for pwd, count in Counter(passwords).most_common(10):
        print(f"  {pwd}: {count}")

if __name__ == "__main__":
    for logfile in sys.argv[1:]:
        analyze_log(logfile)