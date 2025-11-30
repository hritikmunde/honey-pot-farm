#!/bin/bash

mkdir -p analysis/logs

echo "Downloading logs..."

kubectl logs deployment/honeypot-web-server > analysis/logs/web-server.log
kubectl logs deployment/honeypot-edge-router > analysis/logs/edge-router.log
kubectl logs deployment/honeypot-domain-controller > analysis/logs/domain-controller.log

echo "✓ Logs downloaded to analysis/logs/"
echo ""
echo "Quick stats:"
wc -l analysis/logs/*.log