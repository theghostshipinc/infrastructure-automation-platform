# F5 BIG-IP Discovery Results

## Overview

This document summarizes the information gathered by the Ansible discovery playbook.

The playbook uses the **f5networks.f5_modules.bigip_device_info** module to perform read-only discovery against both members of the BIG-IP HA pair.

No configuration changes are made during execution.

---

# HA Pair

| Device | Management IP | Version | HA State | ConfigSync |
|---------|---------------|----------|----------|------------|
| F5-01 | 10.10.10.10 | 16.0.0.1 | Active | 10.10.13.2 |
| F5-02 | 10.10.10.9 | 16.0.0.1 | Standby | 10.10.13.3 |

---

# Virtual Server

Name

```
vs_apache_http
```

VIP

```
10.10.12.100:80
```

Pool

```
pool_apache_http
```

Status

```
Offline
```

Reason

```
The children pool member(s) are down.
```

---

# Pool

Pool Name

```
pool_apache_http
```

Load Balancing Method

```
Round Robin
```

Health Monitor

```
/Common/http
```

Configured Pool Member

```
10.10.11.16:80
```

---

# Node

Node Name

```
node_ubuntu_apache
```

Address

```
10.10.11.16
```

Status

```
Monitor not currently passing.
```

---

# Discovery Validation

The discovery playbook successfully completed against both appliances.

```
F5-01
    ok=6
    changed=0
    failed=0

F5-02
    ok=6
    changed=0
    failed=0
```

The `changed=0` result confirms that the playbook is read-only and does not modify the BIG-IP configuration.

---

# Operational Findings

The discovery workflow identified the following condition:

- The virtual server is currently offline.
- The associated pool member is marked down.
- Because no healthy pool members are available, the virtual server is unavailable.

This demonstrates that the automation workflow can be used for operational validation and troubleshooting in addition to inventory collection.

---

# Next Automation Milestones

Planned enhancements include:

- Automated Node creation
- Automated Pool creation
- Automated Pool Member assignment
- Automated Virtual Server deployment
- Configuration backups
- Health validation
- Configuration compliance
- Reusable Ansible roles
- Infrastructure as Code workflows
