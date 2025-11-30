#!/bin/bash

echo "=== Honeypot Analysis ==="

LOG=$1

echo "Total connections: $(grep 'New connection' $LOG | wc -l)"
echo "Unique IPs: $(grep 'New connection' $LOG | awk '{print $8}' | sort -u | wc -l)"
echo "Login attempts: $(grep 'login attempt' $LOG | wc -l)"
echo "Successful logins: $(grep 'succeeded' $LOG | wc -l)"

echo ""
echo "Top 10 usernames:"
grep "login attempt" $LOG | grep -o "b'[^']*'" | head -1000 | sort | uniq -c | sort -rn | head -10

echo ""
echo "Top 10 passwords:"
grep "login attempt" $LOG | grep -o "b'[^']*'" | tail -1000 | sort | uniq -c | sort -rn | head -10