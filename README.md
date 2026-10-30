# MilliSec SOC Detection Rules

Central repository for SIEM detection content. All rules are version-controlled
here and deployed to SIEM platforms via REST API. Manual edits in the SIEM are
prohibited — every change starts with a commit in this repo.

## Structure

splunk/ – 15 saved searches (alerts) deployed via Splunk REST API qradar/ – 10 custom offense rules deployed via QRadar REST API

## Deployment
- Splunk: `splunk/deploy_splunk.ps1` – parses savedsearches.conf, creates alerts via /servicesNS endpoint
- QRadar: `qradar/deploy_qradar.py` – imports rule definitions via content management API

## Splunk Rules (15)
| # | Rule | Index | MITRE | Severity |
|---|------|-------|-------|----------|
| 1 | CRITICAL - Canary Honeytoken Authentication | wineventlog | T1078 | CRITICAL |
| 2 | Honeypot IP Detected in Corporate Systems | tpot+all | T1595 | HIGH |
| 3 | SQL Injection Attempt Blocked by WAF | waf | T1190 | HIGH |
| 4 | XSS Attempt Blocked by WAF | waf | T1059.007 | HIGH |
| 5 | Sensitive File Access Attempt | waf | T1083 | HIGH |
| 6 | API Brute Force - Multiple 401 | api | T1110 | HIGH |
| 7 | Impossible Travel - Multi-Country Logins | api,waf | T1078 | MEDIUM |
| 8 | Potential DDoS - Request Rate Spike | waf | T1498 | HIGH |
| 9 | Malware Attachment Quarantined | mail | T1566.001 | HIGH |
| 10 | Malicious DNS Request Blocked | pihole | T1071.004 | HIGH |
| 11 | Data Exfiltration Attempt via USB | xdr | T1052.001 | HIGH |
| 12 | Backup Job Failed | backup | T1490 | MEDIUM |
| 13 | Ransomware Behavior - Mass File Operations | wineventlog | T1486 | CRITICAL |
| 14 | New AD User Account Created | wineventlog | T1136.002 | HIGH |
| 15 | User Added to Privileged Group | wineventlog | T1098.007 | HIGH |

## QRadar Offense Rules (10)
AD account lifecycle, Sysmon injection detection, PowerShell abuse,
lateral movement, DNS sinkhole hits, mail gateway quarantine.

## Change Policy
1. Edit rule in this repo (branch + commit)
2. Run deploy script (API pushes update to SIEM)
3. Verify triggered state in SIEM UI
