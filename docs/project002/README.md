# Project 002 - Automated BIG-IP LTM Deployment

## Overview

Project 002 demonstrates Infrastructure as Code (IaC) by automatically deploying a complete F5 BIG-IP LTM application using Ansible.

The automation configures:

- HTTP Health Monitor
- Load Balancing Pool
- Pool Members
- HTTP Virtual Server (VIP)
- SNAT Automap
- Active/Standby Configuration Synchronization

---

## Environment

| Component | Quantity |
|-----------|---------:|
| BIG-IP VE | 2 |
| Ubuntu Web Servers | 3 |
| Virtual Server | 1 |
| HTTP Monitor | 1 |
| Pool | 1 |

---

## Features Demonstrated

- Infrastructure as Code
- Idempotent Playbooks
- Active/Standby BIG-IP HA
- Automatic Configuration Synchronization
- Health Monitoring
- Automatic Removal of Failed Pool Members
- Automatic Recovery of Restored Pool Members
- Round-Robin Load Balancing

---

## Documentation

| Document | Description |
|----------|-------------|
| README.md | Project overview |
| Architecture.md | Network topology and design |
| Deployment.md | Deployment workflow |
| Validation.md | Test procedures and results |

---

## Result

The deployment is fully automated using Ansible and can be executed repeatedly with no configuration drift.

The completed deployment includes:

- HTTP Monitor
- Pool
- Pool Members
- Virtual Server
- SNAT Automap
- Automatic Health Monitoring
- BIG-IP High Availability Synchronization

Project Status:

**Complete**
