# DevOps Monitoring System with InfluxDB + Grafana

## Overview
A complete monitoring solution featuring:
- **Metrics collection** (CPU, Memory, Disk, Network)
- **Alerting system** with email notifications
- **Visualization dashboard** in Grafana

## Prerequisites
- Docker & Docker Compose
- Python 3.8+
- Gmail account (for alert notifications)

## Quick Start
```bash
# Clone repository
git clone https://github.com/DeviNKondeti/system-monitoring-solution.git
cd devops-monitoring

# Start services
docker-compose up -d

# Run metrics collector
python scripts/monitor.py
```
## System Components
1. InfluxDB (Metrics Storage)
Port: 8086

Credentials:
Admin: admin/admin123
Grafana user: grafana/grafana123
Database: metrics

2. Grafana (Visualization)
URL: http://localhost:3000

Login: admin/admin
Preconfigured:
InfluxDB datasource
System dashboard

3. Monitor Script
Collects every 10 seconds:

CPU, Memory, Disk, Network metrics → InfluxDB
Alert Configuration

Preconfigured alerts (edit in Grafana):
CPU: >85% for 5m
Memory: >90% for 15m
Disk: >85% immediate


## InfluxQL queries for CPU, MEMORY, DISK, NETWORK TRAFFIC and SYSTEM HEALTH alon with their Dashboard Visualizations

1. CPU:
SELECT mean("cpu") AS "CPU Usage" 
FROM "system_metrics" 
WHERE $timeFilter 
GROUP BY time(10s) fill(linear)

2. MEMORY:
SELECT mean("memory") AS "Memory Usage" 
FROM "system_metrics" 
WHERE $timeFilter 
GROUP BY time(10s) fill(linear)

3. DISK:
SELECT mean("disk") AS "Disk Usage" 
FROM "system_metrics" 
WHERE $timeFilter 
GROUP BY time(10s) fill(linear)

Grafana Dashboard visualizations of CPU, MEMORY and DISK
![Screenshot (18)](https://github.com/user-attachments/assets/38457776-1b41-4266-8ca7-bac4b3f872bd)

5. NETWORK TRAFFIC:
SELECT non_negative_derivative(mean("net_sent"), 1s) AS "Network Sent (bytes/s)",
       non_negative_derivative(mean("net_recv"), 1s) AS "Network Received (bytes/s)"
FROM "system_metrics" 
WHERE $timeFilter 
GROUP BY time(10s) fill(linear)

Grafana Dashboard visualizations of NETWORK TRAFFIC
![Screenshot (17)](https://github.com/user-attachments/assets/3cfe7258-e705-47f7-b7a4-c946f52b1cf3)

7. SYSTEM HEALTH:
SELECT mean("cpu") AS "CPU", 
       mean("memory") AS "Memory", 
       mean("disk") AS "Disk"
FROM "system_metrics" 
WHERE $timeFilter 
GROUP BY time(1m) fill(previous)

Grafana Dashboard visualizations of SYSTEM HEALTH
![Screenshot (16)](https://github.com/user-attachments/assets/4028fee7-44f4-4e16-bb50-09c423df1385)


## Alerts and related screenshots

![Screenshot (23)](https://github.com/user-attachments/assets/b0761933-32ef-4116-9d9e-52033201f7f6)

Created 3 alerts,
1. High CPU Utilization alert
   ![Screenshot (24)](https://github.com/user-attachments/assets/a7f5b904-4b31-46a4-96dc-efae35399120)

2. High Memory Allocation
   ![Screenshot (25)](https://github.com/user-attachments/assets/b251dacd-d36b-4eb4-bede-cb3304e85481)

3. Low Disk Space
   ![Screenshot (26)](https://github.com/user-attachments/assets/55cb8204-9027-434b-b578-a24a0c6c42dc)


## Email Alerts 

1. Purpose of Email Alerts
In a system monitoring setup, email alerts serve as a primary notification channel to:
    1. Detect anomalies (e.g., CPU spikes, disk full, service downtime)
    2. Trigger immediate response
    3. Maintain audit logs (historical record of incidents)

2. SMTP (Simple Mail Transfer Protocol)
Role: Delivers emails from Grafana to recipients.
Components:
SMTP Server (e.g., Gmail)
Authentication (username + password or API key(generated while email 2 step verification setup))
Encryption

3. Key Configuration Requirements
For Grafana to send alerts via email:
SMTP Server Details
Host (smtp.gmail.com:587)
Valid credentials (username + password/app token)
"From" address

Alert Rules
    1. Define thresholds (e.g., CPU > 85% for 5 minutes)
    2. Set severity levels (Warning, Critical)
    3. Configure notification policies (who receives which alerts)
    4. Security Considerations
    5. App Passwords (for Gmail)
    6. Rate Limiting (prevent email flooding)

**How It Works in the system monitoring Project**
    Grafana evaluates metrics from InfluxDB.
    When a threshold is breached:
    Grafana formats an email with alert details (metric, time, severity).
    Connects to the SMTP server (configured in docker-compose.yml).
    Sends the email to predefined recipients.
    ![Screenshot (21)](https://github.com/user-attachments/assets/f8d87e61-2c22-4a86-b4ce-556520652100)
    ![Screenshot (27)](https://github.com/user-attachments/assets/07ca35e3-97a1-4a39-a1f7-44b8339b3505)

