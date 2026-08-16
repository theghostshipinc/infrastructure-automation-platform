# TheGhostShipInc Infrastructure Automation Architecture

## Overview

TheGhostShipInc Infrastructure Automation project is a reusable infrastructure and network automation platform designed to manage, validate, document, and eventually deploy multi-vendor infrastructure through code.

F5 BIG-IP is the first production-style use case for the platform, but the architecture is intentionally designed to expand beyond F5.

The long-term objective is to create a common automation framework capable of supporting:

- F5 BIG-IP
- Cisco network infrastructure
- Arista network infrastructure
- Linux systems
- Cloud networking
- Infrastructure validation
- Configuration generation
- Infrastructure as Code
- CI/CD workflows
- Monitoring and reporting

The project is being developed incrementally, beginning with safe read-only discovery before progressing to configuration management and automated deployment.

---

# Current Architecture

The current automation environment consists of a dedicated Ubuntu automation controller connected to a virtual enterprise network running inside GNS3.

```text
                         Internet
                            |
                       GNS3 NAT
                            |
                     +-------------+
                     | automation01|
                     | Ubuntu 26.04|
                     +-------------+
                       |         |
              Internet |         | Lab Management
                 ens3  |         | ens4
                       |         |
              192.168.124.0/24   10.10.10.0/24
                                 |
                  +--------------+--------------+
                  |                             |
             +----------+                  +----------+
             |  F5-01   |                  |  F5-02   |
             |  Active  |                  | Standby  |
             +----------+                  +----------+
             10.10.10.10                   10.10.10.9
                  |                             |
                  +-------------+---------------+
                                |
                         HA / ConfigSync
                          10.10.13.0/24
                                |
                         Application Networks
                                |
                        +---------------+
                        | Apache Server |
                        | 10.10.11.16   |
                        +---------------+
```

---

# Automation Controller

## automation01

`automation01` is the central automation controller.

Operating system:

```text
Ubuntu 26.04 LTS
```

Network interfaces:

```text
ens3
192.168.124.0/24
Purpose: Internet access and package management

ens4
10.10.10.100/24
Purpose: Lab management and infrastructure automation
```

Installed automation components include:

- Git
- Python 3.14
- Python virtual environments
- Ansible Core
- F5 Ansible Collection
- Ansible Vault
- jq
- SSH tools
- Standard Linux development utilities

The automation toolchain is isolated inside a Python virtual environment.

```text
~/Projects/Infrastructure/.venv
```

---

# Repository Architecture

```text
Infrastructure
|
+-- README.md
+-- requirements.txt
+-- .gitignore
|
+-- ansible
|   |
|   +-- ansible.cfg
|   |
|   +-- inventories
|   |   +-- lab
|   |       +-- group_vars
|   |       +-- host_vars
|   |       +-- hosts.yml
|   |
|   +-- playbooks
|   |   +-- f5-device-info.yml
|   |   +-- f5-discovery.yml
|   |
|   +-- roles
|   +-- templates
|   +-- files
|   +-- requirements.yml
|
+-- docs
|
+-- scripts
|
+-- tests
```

The repository separates:

- Inventory
- Variables
- Playbooks
- Secrets
- Documentation
- Reusable roles
- Templates
- Scripts
- Testing

This structure is intended to support additional infrastructure platforms without redesigning the repository.

---

# Credential Management

Infrastructure credentials are managed using Ansible Vault.

Public source control does not contain plaintext infrastructure credentials.

The local Vault file is excluded from Git:

```text
ansible/inventories/lab/group_vars/f5/vault.yml
```

The local Python virtual environment is also excluded:

```text
.venv/
```

Non-secret variable mappings remain version controlled.

---

# Current F5 Automation

The first implemented automation domain is F5 BIG-IP.

The environment contains an Active / Standby BIG-IP HA pair.

```text
F5-01
Management: 10.10.10.10
State: Active
ConfigSync: 10.10.13.2

F5-02
Management: 10.10.10.9
State: Standby
ConfigSync: 10.10.13.3
```

Current automation is intentionally read-only.

Ansible currently discovers:

- BIG-IP software version
- Platform information
- HA device state
- Device groups
- Interfaces
- VLANs
- Self IPs
- Virtual servers
- LTM pools
- Pool members
- Nodes

The discovery workflow completes against both BIG-IP appliances without making configuration changes.

Example:

```text
F5-01 : ok=6 changed=0 unreachable=0 failed=0
F5-02 : ok=6 changed=0 unreachable=0 failed=0
```

---

# Current Application Stack

The F5 configuration currently includes:

## Virtual Server

```text
Name: vs_apache_http
VIP: 10.10.12.100:80
Pool: pool_apache_http
```

## Pool

```text
Name: pool_apache_http
Load Balancing: Round Robin
Health Monitor: HTTP
```

## Pool Member

```text
10.10.11.16:80
```

## Node

```text
node_ubuntu_apache
10.10.11.16
```

The discovery workflow can identify both configured infrastructure and operational state.

---

# Design Philosophy

The platform follows several engineering principles.

## 1. Read Before Write

Automation begins with discovery and validation before configuration changes are introduced.

## 2. Version Everything

Automation code, inventories, templates, documentation, and infrastructure definitions are maintained in Git.

## 3. Protect Secrets

Credentials are separated from source code and protected with Ansible Vault.

## 4. Build Reusable Components

Automation will evolve from individual playbooks into reusable roles and templates.

## 5. Validate Changes

Future configuration workflows will include pre-change and post-change validation.

## 6. Remain Vendor Extensible

The repository is designed to support multiple infrastructure platforms rather than becoming an F5-only repository.

---

# Long-Term Platform Vision

The long-term architecture expands the automation controller into a multi-vendor infrastructure automation platform.

```text
                         Git / GitHub
                              |
                              |
                     CI/CD Automation
                              |
                              v
                    +------------------+
                    |   automation01   |
                    |                  |
                    | Ansible          |
                    | Python           |
                    | APIs             |
                    | Templates        |
                    | Validation       |
                    +------------------+
                       |    |    |    |
             +---------+    |    |    +----------+
             |              |    |               |
             v              v    v               v
          F5 BIG-IP       Cisco Arista         Linux
             |              |    |               |
             +--------------+----+---------------+
                            |
                            v
                     Cloud Networking
                            |
                   AWS / Azure / Hybrid
```

---

# Planned Automation Domains

## F5 BIG-IP

Planned capabilities:

- Node provisioning
- Pool provisioning
- Pool member management
- Health monitor configuration
- Virtual server provisioning
- SSL profile management
- iRule deployment
- HA validation
- Configuration backup
- Configuration synchronization
- Operational reporting

## Cisco

Planned capabilities:

- Device discovery
- Configuration collection
- VLAN management
- Interface configuration
- Routing configuration
- Configuration validation
- Compliance checking

## Arista

Planned capabilities:

- EOS discovery
- BGP validation
- EVPN/VXLAN automation
- Configuration generation
- Fabric validation
- CloudVision integration

## Linux

Planned capabilities:

- Golden-image provisioning
- Package installation
- Web-server deployment
- Docker configuration
- Monitoring agents
- System validation

## Cloud

Planned capabilities:

- Cloud networking
- VPC/VNet deployment
- Routing
- Hybrid connectivity
- Infrastructure as Code
- Terraform integration

---

# Infrastructure as Code Evolution

The project will evolve through several stages.

```text
Stage 1
Discovery
   |
   v
Stage 2
Validation
   |
   v
Stage 3
Configuration Management
   |
   v
Stage 4
Reusable Roles
   |
   v
Stage 5
Infrastructure as Code
   |
   v
Stage 6
CI/CD
   |
   v
Stage 7
Automated Multi-Vendor Infrastructure Platform
```

---

# Current Project Milestone

## v0.1.0 - Automation Foundation

Completed:

- Reusable Ubuntu automation controller
- Dual-homed management architecture
- Python virtual environment
- Git repository structure
- Ansible Core
- F5 Ansible Collection
- Structured YAML inventory
- Encrypted credential management
- BIG-IP API connectivity
- HA discovery
- Virtual server discovery
- LTM pool discovery
- Pool member discovery
- Node discovery
- Read-only operational validation
- Repository documentation
- Backup and recovery strategy

---

# Next Milestones

## v0.2.0 - Validation Framework

Planned:

- Structured health reporting
- HA validation
- Pool health validation
- Virtual server validation
- Automated reporting

## v0.3.0 - F5 Configuration Automation

Planned:

- Automated nodes
- Automated pools
- Automated pool members
- Automated virtual servers
- Idempotency validation

## v0.4.0 - Multi-Vendor Discovery

Planned:

- Cisco discovery
- Arista discovery
- Unified inventory model

## v0.5.0 - Infrastructure as Code Foundation

Planned:

- Reusable roles
- Configuration templates
- Automated testing
- CI/CD workflow

---

# Project Goal

The ultimate goal of TheGhostShipInc Infrastructure Automation project is to demonstrate how modern infrastructure engineering can combine networking, systems, automation, APIs, Infrastructure as Code, testing, and version control into a repeatable engineering platform.

F5 BIG-IP is the first implementation.

It is not the final destination.
