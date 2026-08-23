# Project 002 - Deployment Guide

## Overview

Project 002 deploys a complete F5 BIG-IP Local Traffic Manager (LTM) application using Ansible.

Deployment is performed only against the active BIG-IP device. High Availability synchronization automatically replicates the configuration to the standby appliance.

---

# Deployment Prerequisites

The following components must already exist:

- Active/Standby BIG-IP HA pair
- Device Trust established
- Sync-Failover Device Group configured
- Three Ubuntu web servers
- Apache installed and running
- SSH connectivity from the automation server
- Ansible Vault configured
- F5 Ansible Collection installed

---

# Inventory

Deployment targets the Active BIG-IP group.

```bash
ansible-inventory --graph
```

Result:

```
@f5_active
    F5-01
```

---

# Syntax Validation

Before deployment, validate the playbook.

```bash
ansible-playbook --syntax-check \
ansible/playbooks/project002-ltm-build.yml
```

---

# Deployment

Execute the deployment.

```bash
ansible-playbook \
ansible/playbooks/project002-ltm-build.yml \
--ask-vault-pass
```

The playbook performs the following tasks:

1. Create HTTP Monitor
2. Create Pool
3. Add Pool Members
4. Create Virtual Server
5. Save BIG-IP Configuration

---

# Objects Created

The deployment creates:

| Object | Name |
|---------|------|
| HTTP Monitor | project002-http-monitor |
| Pool | project002-web-pool |
| Pool Members | web01, web02, web03 |
| Virtual Server | project002-web-vip |

---

# High Availability

Configuration changes are synchronized automatically through the configured Sync-Failover Device Group.

Verification:

```bash
tmsh show cm sync-status
```

Expected Result:

```
Status: In Sync
```

---

# Idempotency

The deployment is idempotent.

Running the playbook multiple times results in:

```
changed=0
failed=0
```

when no configuration changes are required.

---

# Outcome

The deployment provisions a fully functional, highly available F5 BIG-IP LTM application using Infrastructure as Code principles.
