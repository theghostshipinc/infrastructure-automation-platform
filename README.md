# TheGhostShipInc Infrastructure Automation

A hands-on network automation project built around a virtual F5 BIG-IP HA environment.

The project demonstrates the development of a reusable automation workflow using Linux, Python, Ansible, Ansible Vault, Git, and F5 BIG-IP.

---

# Current Capabilities

The automation platform currently supports read-only discovery of an F5 BIG-IP HA pair, including:

- BIG-IP platform and software version
- Active / Standby device state
- Device and ConfigSync information
- Interfaces
- VLANs
- Self IPs
- Virtual Servers
- LTM Pools
- Pool Members
- Nodes

---

# Environment

## Automation Controller

- Ubuntu 26.04 LTS
- Python 3.14
- Python Virtual Environment
- Ansible Core 2.21.3
- f5networks.f5_modules 1.43.0

## F5 Environment

- Two BIG-IP Virtual Edition appliances
- Active / Standby HA
- BIG-IP 16.0.0.1
- GNS3-based lab topology

---

# Repository Structure

```text
.
... ansible
.   ... ansible.cfg
.   ... inventories
.   .   ... lab
.   .       ... group_vars
.   .       ... host_vars
.   .       ... hosts.yml
.   ... playbooks
.   .   ... f5-device-info.yml
.   .   ... f5-discovery.yml
.   ... roles
.   ... templates
.   ... requirements.yml
... docs
... scripts
... tests
... requirements.txt
... README.md
```

---

# Security

Credentials are stored using Ansible Vault.

The encrypted vault file is excluded from the public repository.

The local Python virtual environment is also excluded from Git.

---

# Discovery Workflow

Run the discovery playbook:

```bash
ansible-playbook playbooks/f5-discovery.yml --ask-vault-pass
```

The workflow performs read-only discovery of both BIG-IP appliances.

A successful run returns:

```text
F5-01 : ok=6 changed=0 unreachable=0 failed=0
F5-02 : ok=6 changed=0 unreachable=0 failed=0
```

---

# Current Milestone

## v0.1 . F5 Discovery

Completed:

- Ubuntu automation controller
- Python virtual environment
- Git configuration
- Ansible installation
- F5 Ansible Collection
- Structured inventory
- Ansible Vault integration
- Dual-homed networking
- API connectivity
- BIG-IP HA discovery
- Virtual Server discovery
- Pool discovery
- Node discovery
- Read-only validation

---

# Roadmap

Future development includes:

- Automated Node creation
- Automated Pool creation
- Automated Virtual Server deployment
- Configuration validation
- Health verification
- Reusable Ansible Roles
- Automated reporting
- GitHub CI/CD integration

---

# Author

Greg Mitchell

TheGhostShipInc
