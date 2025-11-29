#!/bin/bash

echo "======================================"
echo "  Honeypot Activity Monitor"
echo "======================================"
echo ""

for deployment in web-server edge-router domain-controller; do
    echo "--- honeypot-${deployment} ---"
    
    POD=$(kubectl get pods -l type=${deployment} -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    
    if [ -z "$POD" ]; then
        echo "❌ No pod found"
        continue
    fi
    
    TOTAL=$(kubectl logs $POD 2>/dev/null | grep "New connection" | wc -l)
    EXTERNAL=$(kubectl logs $POD 2>/dev/null | grep "New connection" | grep -v "10.0." | wc -l)
    ATTEMPTS=$(kubectl logs $POD 2>/dev/null | grep "login attempt" | wc -l)
    SUCCESS=$(kubectl logs $POD 2>/dev/null | grep "login attempt.*succeeded" | wc -l)
    
    echo "  Total connections: $TOTAL"
    echo "  External IPs: $EXTERNAL"
    echo "  Login attempts: $ATTEMPTS"
    echo "  Successful logins: $SUCCESS"
    echo ""
done

echo "Last updated: $(date)"