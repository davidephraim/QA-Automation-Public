# 📌 Set Personal Information

## 🧩 Overview
This feature automates the process of setting or updating user personal information through automated tests.

It supports multiple environments and dynamic user credentials via CLI parameters.

#### ✅ Status: Stable
Fully tested and ready for regular use.

---

## 📦 File
`set_personal_info.py`

## 🧪 Test Type
Automation / E2E Test

## ⚙️ Parameters

| Parameter   | Description                    |
|-------------|--------------------------------|
| `--env`     | Target environment (dev / stg) |
| `--username`| User login email               |
| `--password`| User password                  |
| `--name`    | User full name                 |
| `--headed`  | Run browser in UI mode         |

## 🚀 Execution

```bash
pytest set_personal_info.py \
  --env=<ENVIRONMENT> \
  --username=<USER_EMAIL> \
  --password=<USER_PASSWD> \
  --name=<USER_NAME> \
  --headed