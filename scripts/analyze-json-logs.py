#!/usr/bin/env python3
import json
import sys
from collections import Counter

def analyze_json_log(filename):
    print(f"\n{'='*60}")
    print(f"Analysis: {filename}")
    print(f"{'='*60}")
    
    events = []
    
    # Read JSON lines
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as e:
                pass  # Skip invalid lines
    
    print(f"Total events: {len(events)}")
    
    # Connection events
    connections = [e for e in events if e.get('eventid') == 'cowrie.session.connect']
    print(f"Total connections: {len(connections)}")
    
    # External IPs (not 10.0.x.x)
    src_ips = [e.get('src_ip') for e in connections if e.get('src_ip')]
    external_ips = [ip for ip in src_ips if not ip.startswith('10.0.')]
    print(f"External connections: {len(external_ips)}")
    print(f"Unique external IPs: {len(set(external_ips))}")
    
    # Login attempts
    login_success = [e for e in events if e.get('eventid') == 'cowrie.login.success']
    login_failed = [e for e in events if e.get('eventid') == 'cowrie.login.failed']
    total_logins = len(login_success) + len(login_failed)
    
    print(f"Login attempts: {total_logins}")
    print(f"  Successful: {len(login_success)}")
    print(f"  Failed: {len(login_failed)}")
    
    # Top usernames
    usernames = [e.get('username') for e in events if e.get('username')]
    if usernames:
        print(f"\nTop 10 usernames:")
        for user, count in Counter(usernames).most_common(10):
            print(f"  {user}: {count}")
    
    # Top passwords
    passwords = [e.get('password') for e in events if e.get('password')]
    if passwords:
        print(f"\nTop 10 passwords:")
        for pwd, count in Counter(passwords).most_common(10):
            print(f"  {pwd}: {count}")
    
    # Commands executed
    commands = [e for e in events if e.get('eventid') == 'cowrie.command.input']
    if commands:
        print(f"\nCommands executed: {len(commands)}")
        cmd_list = [e.get('input') for e in commands if e.get('input')]
        if cmd_list:
            print(f"Top 10 commands:")
            for cmd, count in Counter(cmd_list).most_common(10):
                print(f"  {cmd}: {count}")
    
    # Show sample of external IPs
    if external_ips:
        unique_external = sorted(set(external_ips))
        print(f"\nSample of unique external IPs (first 20):")
        for ip in unique_external[:20]:
            count = external_ips.count(ip)
            print(f"  {ip}: {count} connections")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze-json-logs.py <logfile1> [logfile2] ...")
        sys.exit(1)
    
    for logfile in sys.argv[1:]:
        try:
            analyze_json_log(logfile)
        except FileNotFoundError:
            print(f"Error: File not found: {logfile}")
        except Exception as e:
            print(f"Error analyzing {logfile}: {e}")