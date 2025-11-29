# Automated Honeypot Farm

A Kubernetes-native honeypot deployment system for studying opportunistic network threats.

## 🎯 Overview

This project deploys multiple SSH/Telnet honeypots with different personas to capture and analyze automated network attacks. Built with Kubernetes for scalability and modern DevOps practices.

## 🏗️ Architecture

### Honeypot Types
- **Web Server** (`web-prod-us-east-1a`) - Mimics production web server
- **Edge Router** (`edge-router-nyc-01`) - Mimics Cisco network device  
- **Domain Controller** (`DC-PRIMARY-001`) - Mimics Windows infrastructure

### Technology Stack
- **Honeypot**: Cowrie SSH/Telnet honeypot
- **Container Runtime**: Docker
- **Orchestration**: Kubernetes (AWS EKS)
- **Log Aggregation**: Loki + Promtail
- **Visualization**: Grafana
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions

## 📊 Project Status

- [x] Docker containerization
- [x] Multi-honeypot docker-compose setup
- [ ] Kubernetes local deployment (Minikube)
- [ ] ConfigMaps and persistent storage
- [ ] Monitoring stack (Loki/Grafana)
- [ ] Terraform for AWS EKS
- [ ] CI/CD pipeline
- [ ] Production cloud deployment

## 🚀 Quick Start

### Local
### Prerequisites
- Docker & Docker Compose
- (Later: kubectl, minikube, terraform, AWS CLI)

### Local Development (Current)
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/automated-honeypot-farm.git
cd automated-honeypot-farm

# Create log directories with correct permissions
mkdir -p logs/{web-server,edge-router,domain-controller}
sudo chown -R 999:999 logs/
chmod 755 logs/

# Start honeypots
docker-compose up -d

# View logs
docker-compose logs -f

# Test honeypots
ssh -p 2222 root@localhost  # web-server (try password: admin)
ssh -p 2223 root@localhost  # edge-router (try password: cisco)
ssh -p 2224 root@localhost  # domain-controller (try password: Administrator)

# Check collected logs
cat logs/web-server/cowrie.json | jq .
cat logs/edge-router/cowrie.json | jq .
cat logs/domain-controller/cowrie.json | jq .

# Stop honeypots
docker-compose down
```

### Kubernetes Deployment (Coming Soon)
```bash
# Deploy to local Kubernetes
kubectl apply -k kubernetes/base/

# Deploy monitoring stack
kubectl apply -f kubernetes/monitoring/
```
## On AWS with EKS
### Prerequisites
- AWS Account with credentials configured
- Terraform >= 1.0
- kubectl
- Helm 3

### Deploy Infrastructure
```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/automated-honeypot-farm.git
cd automated-honeypot-farm

# 2. Deploy AWS infrastructure
cd terraform/aws
terraform init
terraform apply  # Takes ~15 minutes

# 3. Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name honeypot-farm

# 4. Verify cluster
kubectl get nodes

# 5. Deploy honeypots
cd ../..
kubectl apply -f k8s/base/

# 6. Get LoadBalancer URLs (takes 2-3 minutes)
kubectl get services
```

### Monitor Logs
```bash
# View real-time logs
kubectl logs -f deployment/honeypot-web-server

# Count login attempts
kubectl logs deployment/honeypot-web-server | grep "login attempt" | wc -l

# Download logs for analysis
kubectl logs deployment/honeypot-web-server > web-server.log
```

### Clean Up (Stop AWS Charges)
```bash
cd terraform/aws
terraform destroy  # Removes all AWS resources
```

## 📁 Project Structure
```
.
├── docker/                 # Container definitions
│   ├── Dockerfile         # Cowrie honeypot image
│   └── configs/           # Honeypot configurations
│       ├── web-server.cfg
│       ├── edge-router.cfg
│       └── domain-controller.cfg
├── kubernetes/            # Kubernetes manifests
│   ├── base/             # Base deployments
│   │   ├── deployment-*.yaml
│   │   ├── configmap-*.yaml
│   │   └── service.yaml
│   └── monitoring/       # Monitoring stack
│       ├── loki.yaml
│       ├── promtail.yaml
│       └── grafana.yaml
├── terraform/            # Infrastructure as Code
│   └── aws/             # AWS EKS cluster setup
│       ├── main.tf
│       ├── vpc.tf
│       └── security-groups.tf
├── scripts/             # Utility scripts
│   └── analyze-logs.py
├── docs/                # Documentation
│   └── proposal.md
├── docker-compose.yml   # Local development setup
└── README.md           # This file
```

## 🎓 Learning Objectives

This project demonstrates:
- Container orchestration with Kubernetes
- Infrastructure as Code with Terraform
- DevOps-native log aggregation (Loki/Grafana)
- Network security and isolation
- CI/CD pipeline implementation
- Cloud deployment best practices (AWS EKS)

## 📈 Metrics & Analysis

The honeypots collect:
- Login attempts (username/password pairs)
- Source IP addresses
- Command execution attempts
- Malware download URLs
- Session transcripts

Analysis scripts provide:
- Attack frequency over time
- Geographic distribution of attackers
- Most common credentials
- Command patterns
- IDS detection coverage

## 📝 Documentation

- [Project Proposal](docs/proposal.md) - Original project goals and objectives

## 📊 Deployment Status

**Live Since:** November 29, 2024  
**Platform:** AWS EKS (us-east-1)  
**Status:** 🟢 Active - Collecting Data

### Current Statistics
- **Honeypots Running:** 3 types (web-server, edge-router, domain-controller)
- **Replicas:** 2 per type (6 pods total)
- **Data Collection:** 24-48 hours
- **Log Storage:** AWS EBS (PersistentVolumes)

*Statistics will be updated after data collection period.*

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────┐
│                    Internet                         │
└───────────────────┬─────────────────────────────────┘
                        │
            ┌───────────┼───────────┐
            │           │           │
            ▼           ▼           ▼
        [AWS NLB]   [AWS NLB]   [AWS NLB]
        Port 22     Port 22     Port 22/23
            │           │           │
    ┌───────┴───────────┴───────────┴────────┐
    │         AWS EKS Cluster                │
    │  ┌──────────────────────────────────┐  │
    │  │    Honeypot Deployments          │  │
    │  │  ┌────────────────────────────┐  │  │
    │  │  │ Web Server (2 replicas)    │  │  │
    │  │  │ Edge Router (2 replicas)   │  │  │
    │  │  │ Domain Controller (2 reps) │  │  │
    │  │  └────────────────────────────┘  │  │
    │  │           │                      │  │
    │  │           ▼                      │  │
    │  │  ┌────────────────────────────┐  │  │
    │  │  │  PersistentVolumes (EBS)   │  │  │
    │  │  │  - Logs stored here        │  │  │
    │  │  └────────────────────────────┘  │  │
    │  └──────────────────────────────────┘  │
    └────────────────────────────────────────┘
```

## 🔒 Security Considerations

### Network Isolation
- **NetworkPolicies:** Block all outbound traffic except DNS
- **AWS Security Groups:** Restrict management access
- **Egress Filtering:** Prevent honeypots from attacking other systems

### Data Protection
- All logs stored on encrypted EBS volumes
- No production data or credentials exposed
- IP addresses will be anonymized in published reports

### Ethical Considerations
- Honeypots are isolated and cannot harm other systems
- Complies with university research policies
- No active scanning or offensive operations

## 👤 Author

**Hritik Satish Munde**  
Master of Science, Computer Science  
Indiana University Bloomington  
Email: hmunde@iu.edu

## 📄 License

This project is for educational purposes as part of the "Security for Networked Systems" course at Indiana University.

## ⚠️ Disclaimer

This honeypot system is for research and educational purposes only. Ensure proper network isolation and comply with all applicable university and legal policies when deploying to cloud environments.

## 🙏 Acknowledgments

- [Cowrie Honeypot](https://github.com/cowrie/cowrie) - SSH/Telnet honeypot
- Course: Security for Networked Systems - Indiana University Bloomington