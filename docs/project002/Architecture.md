# Project 002 - Architecture

## Objective

Project 002 demonstrates automated deployment and validation of an F5 BIG-IP LTM application delivery configuration using Ansible.

The design provides:

- A highly available BIG-IP pair
- A dedicated HTTP virtual server
- A load-balancing pool
- Three backend web servers
- HTTP health monitoring
- Automated failure detection and recovery
- Configuration synchronization between BIG-IP devices

---

# Logical Traffic Flow

```
                Client
                   |
                   |
        10.10.12.100:80
      project002-web-vip
                   |
                   |
        project002-web-pool
          /       |       \
         /        |        \
        /         |         \
 web01          web02      web03
10.10.11.16   10.10.11.17 10.10.11.18
```

The BIG-IP continuously monitors each backend server using an HTTP health monitor.

Only healthy servers receive production traffic.

---

# BIG-IP High Availability

```
              Sync-Failover Device Group
              --------------------------

      ATL-F5-01                     ATL-F5-02
        Active                        Standby
     10.10.10.10                  10.10.10.9
            \                        /
             \______________________/
                Auto Configuration
                     Synchronization
```

Device Group:

- F5-Device-Group
- Auto Sync Enabled
- Save on Auto Sync Enabled

---

# Network Design

## Management Network

```
10.10.10.0/24
```

Purpose:

- BIG-IP management
- SSH
- Ansible automation
- Web server administration

---

## Application Network

```
10.10.11.0/24
```

Purpose:

- BIG-IP to Web Server communication

Backend Servers

| Server | Application IP |
|---------|----------------|
| web01 | 10.10.11.16 |
| web02 | 10.10.11.17 |
| web03 | 10.10.11.18 |

---

## Virtual Server Network

```
10.10.12.0/24
```

Virtual Server

| Object | Address |
|---------|---------|
| project002-web-vip | 10.10.12.100:80 |

---

# LTM Objects Created

| Object Type | Name |
|--------------|--------------------------|
| HTTP Monitor | project002-http-monitor |
| Pool | project002-web-pool |
| Virtual Server | project002-web-vip |
| Pool Members | web01, web02, web03 |

---

# Health Monitoring

Monitor Type:

- HTTP

Configuration

- Interval: 5 seconds
- Timeout: 16 seconds
- Expected Response: 200 OK

Failed servers are automatically removed from the load-balancing pool.

Recovered servers automatically return to service.

---

# Load Balancing

Method:

- Round Robin

Traffic is distributed evenly across all healthy backend servers.

Example rotation:

```
Client Request 1 -> web01
Client Request 2 -> web02
Client Request 3 -> web03
Client Request 4 -> web01
Client Request 5 -> web02
Client Request 6 -> web03
```

---

# Source Address Translation

The virtual server uses:

```
SNAT Automap
```

This ensures return traffic always flows back through the BIG-IP.

---

# Validation Performed

The following validation steps were successfully completed:

- Deployed the HTTP monitor using Ansible
- Created the LTM pool
- Added three backend pool members
- Created the HTTP virtual server
- Verified configuration synchronization to the standby BIG-IP
- Verified HTTP traffic distribution across all backend servers
- Simulated backend server failure by stopping Apache on web02
- Verified automatic removal of the failed server from load balancing
- Restarted Apache on web02
- Verified automatic recovery and reinsertion into the pool
- Confirmed idempotent Ansible playbook execution with zero changes on subsequent runs

---

# Outcome

Project 002 successfully demonstrates Infrastructure as Code (IaC) principles using Ansible to automate deployment of an enterprise F5 BIG-IP Local Traffic Manager environment.

The deployment is fully repeatable, idempotent, highly available, and capable of automatically detecting backend failures while maintaining uninterrupted application availability.
