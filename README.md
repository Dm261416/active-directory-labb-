# 🏢 Active Directory Home Lab

> A fully documented Active Directory lab environment built on Windows Server 2022, simulating a small enterprise network with domain services, user management, Group Policy, and security hardening.

---

## 📋 Project Overview

This lab demonstrates real-world Active Directory administration skills including domain setup, organizational unit design, bulk user provisioning, GPO enforcement, and security hardening — all scripted with PowerShell.

---

## 🗺️ Lab Architecture
<img width="868" height="560" alt="image" src="https://github.com/user-attachments/assets/7be8aa15-b1c1-4255-b9ac-63790b2b1949" />

```
┌─────────────────────────────────────────────────────────────────┐
│                        LAB NETWORK (192.168.10.0/24)            │
│                                                                  │
│   ┌──────────────────────┐       ┌──────────────────────────┐   │
│   │   DC01 (Primary DC)  │       │   DC02 (Secondary DC)    │   │
│   │  Windows Server 2022 │◄─────►│  Windows Server 2022     │   │
│   │  IP: 192.168.10.10   │       │  IP: 192.168.10.11       │   │
│   │  Roles:              │       │  Roles:                  │   │
│   │   • AD DS            │       │   • AD DS (Replica)      │   │
│   │   • DNS              │       │   • DNS                  │   │
│   │   • DHCP             │       │   • Read-Only DC         │   │
│   └──────────┬───────────┘       └──────────────────────────┘   │
│              │                                                    │
│    ┌─────────┴──────────────────────────┐                        │
│    │         DOMAIN: CORP.LOCAL         │                        │
│    └─────────┬──────────────────────────┘                        │
│              │                                                    │
│    ┌─────────┴──────────┐    ┌──────────────────────┐           │
│    │  WIN10-CLIENT-01   │    │  WIN10-CLIENT-02     │           │
│    │  192.168.10.101    │    │  192.168.10.102      │           │
│    │  Domain Joined     │    │  Domain Joined       │           │
│    └────────────────────┘    └──────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Organizational Unit Structure

```
CORP.LOCAL
├── _CORP
│   ├── Computers
│   │   ├── Desktops
│   │   ├── Laptops
│   │   └── Servers
│   ├── Users
│   │   ├── HR
│   │   ├── IT
│   │   ├── Finance
│   │   └── Management
│   ├── Groups
│   │   ├── Security Groups
│   │   └── Distribution Groups
│   └── Service Accounts
└── _ADMIN
    ├── Tier0 (Domain Admins)
    ├── Tier1 (Server Admins)
    └── Tier2 (Workstation Admins)
```

---

## 🔐 Group Policy Objects (GPOs)

| GPO Name | Scope | Description |
|---|---|---|
| Password Policy | Domain | Min 12 chars, complexity, 90-day expiry |
| Account Lockout | Domain | 5 attempts, 30-min lockout |
| Logon Banner | Domain | Legal warning on login screen |
| Disable USB Storage | Computers OU | Block removable media |
| Audit Policy | Domain | Logon, object access, privilege use |
| RDP Hardening | Servers OU | NLA required, idle timeout |
| AppLocker | Workstations OU | Whitelist approved applications |

---

## 🛡️ Security Hardening Applied

- ✅ NTLM authentication restricted (Kerberos enforced)
- ✅ SMBv1 disabled across all machines
- ✅ Default Administrator account renamed & disabled
- ✅ Tiered administration model (Tier 0/1/2)
- ✅ Fine-grained password policies per OU
- ✅ Advanced audit logging enabled
- ✅ LAPS (Local Administrator Password Solution) deployed
- ✅ Protected Users security group utilized

---

## 📂 Repository Structure

```
active-directory-lab/
├── setup/
│   ├── 01-install-ad-ds.ps1        # Install AD DS role
│   ├── 02-configure-domain.ps1     # Promote to Domain Controller
│   ├── 03-configure-dns.ps1        # DNS zones and records
│   ├── 04-configure-dhcp.ps1       # DHCP scopes and options
│   └── 05-create-ou-structure.ps1  # Build full OU tree
├── users/
│   ├── bulk-create-users.ps1       # Create 50+ users from CSV
│   ├── users-template.csv          # User data template
│   └── create-groups.ps1           # Security & distribution groups
├── gpo/
│   ├── password-policy.ps1         # Password & lockout GPO
│   ├── logon-banner.ps1            # Legal logon banner GPO
│   ├── disable-usb.ps1             # USB storage restriction GPO
│   └── audit-policy.ps1            # Advanced audit policy GPO
├── security/
│   ├── disable-ntlm.ps1            # Restrict NTLM, enforce Kerberos
│   ├── disable-smbv1.ps1           # Disable legacy SMB protocol
│   ├── tiered-admin-model.ps1      # Implement Tier 0/1/2 admin model
│   ├── enable-laps.ps1             # Deploy LAPS
│   └── security-audit.ps1          # Run security baseline check
├── docs/
│   ├── lab-setup-guide.md          # Step-by-step build guide
│   ├── network-topology.md         # Detailed network docs
│   └── troubleshooting.md          # Common issues & fixes
└── screenshots/
    ├── architecture-diagram.md     # Full ASCII architecture
    ├── ou-structure.md             # OU tree visual
    └── gpo-layout.md               # GPO hierarchy diagram
```

---

## 🖥️ Lab Environment

| Component | Details |
|---|---|
| Hypervisor | VMware Workstation Pro / VirtualBox |
| DC OS | Windows Server 2022 Datacenter |
| Client OS | Windows 10 Enterprise (x2) |
| Domain Name | CORP.LOCAL |
| Forest/Domain Level | Windows Server 2016 |
| IP Scheme | 192.168.10.0/24 |
| RAM Required | 16GB minimum |
| Storage Required | 150GB minimum |

---

## 🚀 Quick Start

```powershell
# 1. Clone this repo
git clone https://github.com/Dm261416/active-directory-lab.git

# 2. Run on a fresh Windows Server 2022 VM as Administrator
cd active-directory-lab\setup

# 3. Install AD DS role
.\01-install-ad-ds.ps1

# 4. Promote to Domain Controller (reboot will occur)
.\02-configure-domain.ps1

# 5. After reboot - configure DNS, DHCP, OUs
.\03-configure-dns.ps1
.\04-configure-dhcp.ps1
.\05-create-ou-structure.ps1

# 6. Create users and groups
cd ..\users
.\bulk-create-users.ps1
.\create-groups.ps1

# 7. Apply GPOs
cd ..\gpo
.\password-policy.ps1
.\logon-banner.ps1
.\audit-policy.ps1

# 8. Harden the environment
cd ..\security
.\disable-ntlm.ps1
.\disable-smbv1.ps1
.\tiered-admin-model.ps1
.\enable-laps.ps1
```

---

## 📊 Skills Demonstrated

- **Active Directory DS** — Forest/domain design, DC promotion, replication
- **PowerShell Scripting** — Automation of all admin tasks
- **DNS & DHCP** — Enterprise network services configuration
- **Group Policy** — Security baseline enforcement via GPO
- **Security Hardening** — NTLM restriction, SMBv1 removal, LAPS, tiered admin
- **Identity Management** — Bulk user provisioning, OU design, RBAC groups
- **Documentation** — Network diagrams, runbooks, troubleshooting guides

---

## 👤 Author

**GitHub:** [@Dm261416](https://github.com/Dm261416)  
**Project Type:** IT Home Lab | Active Directory | Windows Server Administration
