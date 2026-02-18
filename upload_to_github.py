#!/usr/bin/env python3
"""
Upload Active Directory Lab to GitHub
Creates repo and pushes all files via GitHub API
"""

import os
import base64
import json
import urllib.request
import urllib.error

TOKEN    = "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"
USERNAME = "Dm261416"
REPO     = "active-directory-lab"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def gh_request(method, path, data=None):
    url = f"https://api.github.com{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()), resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return json.loads(body) if body else {}, e.code

def create_repo():
    print(f"Creating repository: {USERNAME}/{REPO}...")
    data = {
        "name": REPO,
        "description": "🏢 Active Directory Home Lab — Windows Server 2022, PowerShell automation, GPO, security hardening, LAPS, tiered admin model",
        "private": False,
        "auto_init": False,
        "has_issues": True,
        "has_wiki": True
    }
    resp, status = gh_request("POST", "/user/repos", data)
    if status == 201:
        print(f"  ✓ Repo created: https://github.com/{USERNAME}/{REPO}")
        return True
    elif status == 422:
        print(f"  ~ Repo already exists, continuing...")
        return True
    else:
        print(f"  ✗ Failed to create repo: {resp}")
        return False

def upload_file(filepath, repo_path):
    with open(filepath, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    # Check if file exists (for update)
    existing, status = gh_request("GET", f"/repos/{USERNAME}/{REPO}/contents/{repo_path}")
    
    data = {
        "message": f"Add {repo_path}",
        "content": content
    }
    
    if status == 200 and "sha" in existing:
        data["sha"] = existing["sha"]
        data["message"] = f"Update {repo_path}"

    resp, status = gh_request("PUT", f"/repos/{USERNAME}/{REPO}/contents/{repo_path}", data)
    
    if status in (200, 201):
        print(f"  ✓ {repo_path}")
        return True
    else:
        print(f"  ✗ {repo_path} — {resp.get('message', 'Unknown error')}")
        return False

def collect_files(base_dir):
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        # Skip hidden dirs and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for filename in filenames:
            if filename.startswith('.') or filename == os.path.basename(__file__):
                continue
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, base_dir).replace(os.sep, '/')
            files.append((full_path, rel_path))
    return sorted(files)

def main():
    print("=" * 55)
    print("  ACTIVE DIRECTORY LAB — GITHUB UPLOAD")
    print("=" * 55)
    
    if not create_repo():
        print("Aborting.")
        return

    files = collect_files(BASE_DIR)
    print(f"\nUploading {len(files)} files...\n")

    success = 0
    failed  = 0

    for full_path, rel_path in files:
        if upload_file(full_path, rel_path):
            success += 1
        else:
            failed += 1

    # Set repo topics
    print("\nSetting repository topics...")
    gh_request("PUT", f"/repos/{USERNAME}/{REPO}/topics", {
        "names": ["active-directory", "windows-server", "powershell", "cybersecurity", "homelab", "gpo", "sysadmin", "laps", "kerberos", "it-resume"]
    })
    print("  ✓ Topics set")

    print("\n" + "=" * 55)
    print(f"  COMPLETE: {success} uploaded, {failed} failed")
    print(f"  VIEW AT:  https://github.com/{USERNAME}/{REPO}")
    print("=" * 55)

if __name__ == "__main__":
    main()
