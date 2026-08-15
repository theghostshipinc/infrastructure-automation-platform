# Infrastructure Automation Platform

[![Release](https://img.shields.io/badge/release-v0.1.0-0A66C2)](https://github.com/theghostshipinc/infrastructure-automation-platform/releases/tag/v0.1.0)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Ansible](https://img.shields.io/badge/Ansible-2.21-EE0000?logo=ansible&logoColor=white)](https://www.ansible.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A production-style infrastructure automation portfolio built around an F5 BIG-IP high-availability lab. The platform combines Ansible, Python, testing, secure credential handling, configuration backups, and engineering documentation in a foundation designed to expand across vendors.

> **Current release:** v0.1.0 — F5 automation foundation  
> **Engineering principle:** discover, back up, validate, and test before introducing configuration changes.

## Why this project exists

Infrastructure automation is more than writing scripts. It requires repeatable workflows, protected credentials, recoverable configuration, automated validation, clear documentation, and code that can evolve safely.

This repository demonstrates that full engineering lifecycle:

1. Discover infrastructure without changing it.
2. Capture UCS and SCF recovery artifacts.
3. Keep raw device output and credentials out of source control.
4. Sanitize configuration data for safer review.
5. Test security-sensitive transformation logic.
6. Validate Ansible content before deployment.
7. Document architecture, decisions, and future milestones.

## Implemented capabilities

### F5 BIG-IP discovery

Read-only discovery across an active/standby BIG-IP pair includes:

- Platform and software version
- HA state and ConfigSync information
- Interfaces, VLANs, and Self IPs
- Virtual servers
- LTM pools and pool members
- Nodes

### Backup and recovery

A reusable Ansible role orchestrates:

- UCS archive creation
- SCF configuration export
- Per-device, date-based backup organization
- Separation of generated artifacts from version-controlled source

### Secure configuration review

The Python SCF sanitizer:

- Removes certificate and private-key blocks
- Redacts passwords, passphrases, secrets, and master keys
- Preserves non-sensitive LTM configuration
- Produces reviewable output without committing generated device configurations

### Automated quality controls

The v0.1.0 release is validated with:

- Four passing `pytest` unit tests
- Production-profile `ansible-lint`
- Ansible syntax checks
- Git ignore rules for Vault data, raw backups, sanitized reports, and local runtime files

## Architecture

```text
                         GitHub
                            |
                  versioned source and docs
                            |
                    +---------------+
                    | automation01  |
                    | Ubuntu / Git  |
                    | Python        |
                    | Ansible       |
                    +-------+-------+
                            |
                     Lab management
                            |
              +-------------+-------------+
              |                           |
        +-----+-----+               +-----+-----+
        | BIG-IP 01 | <--- HA --->  | BIG-IP 02 |
        | Active    |   ConfigSync  | Standby   |
        +-----+-----+               +-----+-----+
              |                           |
              +-------------+-------------+
                            |
                   Application networks
```

See [the architecture document](docs/ARCHITECTURE.md) for the detailed environment, design principles, and multi-vendor vision.

## Repository structure

```text
.
├── ansible/
│   ├── inventories/lab/          # Lab inventory and non-secret variables
│   ├── playbooks/                # Discovery and backup entry points
│   ├── roles/f5_backup/          # Reusable UCS and SCF backup role
│   ├── ansible.cfg
│   └── requirements.yml
├── backups/.gitkeep              # Runtime destination; backup data ignored
├── docs/
│   ├── ARCHITECTURE.md
│   └── f5-discovery-results.md
├── python/sanitize/f5.py         # SCF sanitization utility
├── reports/sanitized-config/     # Generated reports ignored
├── tests/test_f5_sanitizer.py    # Sanitizer unit tests
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── pytest.ini
├── requirements-dev.txt
└── requirements.txt
```

## Security model

The repository is intentionally structured to prevent operational data from being published.

| Data | Protection |
|---|---|
| Device credentials | Stored locally with Ansible Vault |
| Vault file | Explicitly excluded by `.gitignore` |
| UCS and SCF backups | Written beneath ignored runtime directories |
| Sanitized SCF reports | Generated locally and excluded from Git |
| Private keys and certificates | Removed by the sanitizer |
| Password-like values | Replaced with `<REDACTED>` |
| Python environment | Local `.venv` excluded from source control |

No plaintext infrastructure credentials or raw device backups are intended to be committed.

## Getting started

### 1. Create the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Install Ansible collections

```bash
ansible-galaxy collection install -r ansible/requirements.yml
```

### 3. Configure local inventory secrets

Create the locally ignored Vault file:

```text
ansible/inventories/lab/group_vars/f5/vault.yml
```

Encrypt it with Ansible Vault and never commit the plaintext values.

### 4. Run discovery

```bash
cd ansible
ansible-playbook playbooks/f5-discovery.yml --ask-vault-pass
```

### 5. Run backups

```bash
ansible-playbook playbooks/f5-backup.yml --ask-vault-pass
```

### 6. Sanitize an SCF for review

From the repository root:

```bash
python -m python.sanitize.f5 \
  --input backups/DEVICE/DATE/device.scf \
  --output reports/sanitized-config/device.scf
```

## Validation

Run the unit tests:

```bash
pytest -v
```

Run Ansible linting and syntax validation from the Ansible project directory:

```bash
cd ansible

ansible-lint playbooks/f5-backup.yml
ansible-lint playbooks/f5-device-info.yml
ansible-lint playbooks/f5-discovery.yml
ansible-lint playbooks/f5-scf-backup.yml

ansible-playbook --syntax-check playbooks/f5-backup.yml
ansible-playbook --syntax-check playbooks/f5-device-info.yml
ansible-playbook --syntax-check playbooks/f5-discovery.yml
ansible-playbook --syntax-check playbooks/f5-scf-backup.yml
```

Validated for v0.1.0:

```text
pytest:              4 passed
ansible-lint:        production profile
syntax validation:   4 playbooks passed
working tree:        clean
```

## Roadmap

| Milestone | Direction |
|---|---|
| v0.2.0 | CI/CD, automated linting, tests, and syntax validation on every push |
| v0.3.0 | Structured inventory, health reporting, and drift detection |
| v0.4.0 | Cisco IOS-XE, Cisco NX-OS, and Arista EOS discovery |
| v0.5.0 | Reusable Infrastructure as Code patterns and reporting |
| v1.0.0 | Extensible multi-vendor infrastructure engineering platform |

## Project status

This is an independently developed lab and educational project. F5 BIG-IP is the first implemented automation domain; the architecture is designed to extend to Cisco, Arista, Linux, cloud networking, and Terraform-driven workflows.

See the [changelog](CHANGELOG.md) for release history.

---

**Greg Mitchell · TheGhostShipInc**  
Practical enterprise networking, application delivery, and infrastructure automation.
