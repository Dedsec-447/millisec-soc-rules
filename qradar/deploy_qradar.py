#!/usr/bin/env python3
"""
MilliSec SOC - QRadar rule deployer via REST API
Usage: python3 deploy_qradar.py --host https://QRADAR_IP --user admin --file rules.json
Creates custom rules in QRadar Content Management. Rules must be enabled in UI after import.
"""
import argparse, json, sys, urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_rules(path):
    with open(path) as f:
        return json.load(f)["rules"]

def deploy(host, user, password, rules):
    session = requests.Session()
    session.auth = (user, password)
    session.verify = False
    ok = fail = 0
    for rule in rules:
        payload = {
            "name": rule["name"],
            "description": f"MITRE ATT&CK: {rule['mitre']}. Logic: {rule['logic'][:200]}",
            "enabled": rule["enabled"],
            "rule_type": "EVENT",
            "origin": "SYSTEM",
            "base_rule_ids": [],
            "rule_json": json.dumps({"test": {"operator": "and", "conditions": [{"parameter": "rulelogic", "value": rule["logic"]}]}}, separators=(",", ":"))
        }
        try:
            r = session.post(f"{host}/api/analytics/rules", json=payload, headers={"Version": "12.0", "Content-Type": "application/json"}, timeout=30)
            if r.status_code in (200, 201):
                print(f"[OK]   {rule['name']}"); ok += 1
            else:
                print(f"[FAIL] {rule['name']} -> HTTP {r.status_code}: {r.text[:120]}"); fail += 1
        except Exception as e:
            print(f"[FAIL] {rule['name']} -> {e}"); fail += 1
    print(f"\nDone: {ok} deployed, {fail} failed")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", required=True, help="QRadar console URL, e.g. https://10.0.20.40")
    p.add_argument("--user", default="admin")
    p.add_argument("--file", default="rules.json")
    args = p.parse_args()
    import getpass; pw = getpass.getpass("QRadar password: ")
    sys.exit(deploy(args.host, args.user, pw, load_rules(args.file)))
