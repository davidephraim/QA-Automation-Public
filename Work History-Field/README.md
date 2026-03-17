# 📌 Set Work History

## 🧩 Overview
This feature automates the process of setting or updating user work history through automated tests.

It supports multiple environments and dynamic user credentials via CLI parameters.

#### 🚧 Status: In Progress
On hold.

---

## 📦 File
`set_work_history.py`

## 🧪 Test Type
Automation / E2E Test

## ⚙️ Parameters

| Parameter   | Description                    |
|-------------|--------------------------------|
| `--env`     | Target environment (dev / stg) |
| `--name`    | User full name                 |
| `--format`  | Timesheet format               |
| `--ds`      | Use DS (yes / no)              |
| `--headed`  | Run browser in UI mode         |

## 🚀 Execution

```bash
pytest set_work_history.py \
  --env=<ENVIRONMENT> \
  --name=<USER_NAME> \
  --format=<TIMESHEET_FORMAT> \
  --ds=<DS_CONFIG> \
  --headed