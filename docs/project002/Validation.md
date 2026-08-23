# Project 002 - Validation

## Objective

The purpose of validation was to confirm that the automated deployment successfully created all required BIG-IP LTM objects and that the application behaved correctly under normal and failure conditions.

---

# Test 1 - Playbook Execution

Command

```bash
ansible-playbook \
ansible/playbooks/project002-ltm-build.yml \
--ask-vault-pass
```

Expected Result

- Playbook completes successfully.
- No failed tasks.

Result

**PASS**

---

# Test 2 - Pool Verification

Command

```bash
tmsh list ltm pool project002-web-pool
```

Expected Result

Pool exists with three members.

Result

**PASS**

Members

- web01
- web02
- web03

---

# Test 3 - Monitor Verification

Command

```bash
tmsh list ltm monitor http project002-http-monitor
```

Expected Result

HTTP monitor created successfully.

Result

**PASS**

---

# Test 4 - Virtual Server Verification

Command

```bash
tmsh list ltm virtual project002-web-vip
```

Expected Result

Virtual Server exists.

VIP

```
10.10.12.100:80
```

Result

**PASS**

---

# Test 5 - Load Balancing

Command

```bash
for i in {1..9}; do
curl -s http://10.10.12.100 | grep "Backend Server"
done
```

Expected Result

Traffic rotates between all three backend servers.

Observed

- web01
- web02
- web03

Result

**PASS**

---

# Test 6 - Health Monitoring

Action

Stopped Apache on web02.

```bash
ansible web02 \
-b \
-m service \
-a "name=apache2 state=stopped"
```

Expected Result

BIG-IP removes web02 from service.

Observed

Traffic was distributed only to:

- web01
- web03

Result

**PASS**

---

# Test 7 - Recovery

Action

Restarted Apache.

```bash
ansible web02 \
-b \
-m service \
-a "name=apache2 state=started"
```

Expected Result

web02 automatically returns to service.

Observed

Traffic resumed across:

- web01
- web02
- web03

Result

**PASS**

---

# Test 8 - Configuration Synchronization

Command

```bash
tmsh show cm sync-status
```

Expected Result

```
Status: In Sync
```

Result

**PASS**

Configuration automatically synchronized to ATL-F5-02.

---

# Test 9 - Idempotency

Command

```bash
ansible-playbook \
ansible/playbooks/project002-ltm-build.yml \
--ask-vault-pass
```

Expected Result

```
changed=0
failed=0
```

Result

**PASS**

No configuration drift detected.

---

# Validation Summary

| Validation | Status |
|------------|--------|
| HTTP Monitor | PASS |
| Pool | PASS |
| Pool Members | PASS |
| Virtual Server | PASS |
| Load Balancing | PASS |
| Health Monitoring | PASS |
| Automatic Recovery | PASS |
| HA Synchronization | PASS |
| Idempotency | PASS |

---

# Conclusion

Project 002 successfully demonstrates an enterprise Infrastructure as Code workflow using Ansible to automate deployment of an F5 BIG-IP Local Traffic Manager application.

The deployment is repeatable, idempotent, highly available, automatically synchronized between BIG-IP devices, and resilient to backend server failures.
