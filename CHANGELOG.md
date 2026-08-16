# Changelog

All significant changes to TheGhostShipInc Infrastructure Automation project are documented in this file.

---

## [0.1.0] - 2026-08-15

### Automation Foundation

Initial portfolio release of the infrastructure automation platform.

### Added

- Ubuntu 26.04 automation controller
- Dual-homed automation networking
- Python 3.14 virtual environment
- Ansible Core 2.21.3
- F5 Ansible Collection 1.43.0
- Structured YAML inventories
- Ansible Vault credential management
- Project-specific Ansible configuration
- Git repository structure
- Dependency requirements
- F5 BIG-IP discovery playbook
- F5 BIG-IP system information discovery
- HA pair discovery
- Interface discovery
- VLAN discovery
- Self IP discovery
- Virtual server discovery
- LTM pool discovery
- Pool member discovery
- Node discovery
- Read-only operational validation
- Architecture documentation
- Sanitized discovery documentation

### Infrastructure

Automation controller:

```text
automation01
Ubuntu 26.04 LTS
Python 3.14
Ansible Core 2.21.3
```

F5 environment:

```text
F5-01 - Active
F5-02 - Standby
BIG-IP 16.0.0.1
```

### Validation

Successful discovery completed against both BIG-IP appliances:

```text
F5-01 : ok=6 changed=0 unreachable=0 failed=0
F5-02 : ok=6 changed=0 unreachable=0 failed=0
```

No infrastructure configuration was modified during discovery.

---

## Planned

### 0.2.0

Infrastructure validation and automated reporting.

### 0.3.0

F5 configuration automation.

### 0.4.0

Multi-vendor infrastructure discovery.

### 0.5.0

Infrastructure as Code and CI/CD integration.
