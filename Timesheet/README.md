# 🧪 QA-Sigmatech Automation Framework

Enterprise-grade automation testing framework for **Sigmatech ERP System** built using:

- 🐍 Python 3.10+
- 🎭 Playwright
- 🧪 Pytest
- ⚙️ CLI-driven configuration

---

# 📌 Overview

This repository provides end-to-end automation coverage for the Sigmatech ERP System.

## 👨‍💼 Employee Module
- ✅ Timesheet Creation
- ✅ Leave Request

## 👩‍💼 HR Module
- ✅ Holiday Management
- ✅ Timesheet Approval (Approve / Reject)
- ✅ Leave Cancellation

The framework is fully parameterized via CLI arguments and supports dynamic scenario execution.

Supported system formats:

* Sigmatech
* InfoSys BRI
* InfoSys CIMB
* Mandiri Inhealth

---

# 🏗 Project Structure
```bash
February-26/
├── employee/
│   ├── File_test/
│   │   └── img_dummy.png
│   ├── __init__.py
│   ├── conftest.py
│   ├── employee_timesheet_download.py
│   ├── employee_timesheet_merged.py
│   ├── leave_date.json
│   └── leave_merged.py
│
├── hr/
│   ├── __init__.py
│   ├── cancel_leave.py
│   ├── conftest.py
│   ├── format.json
│   ├── holiday_merged.py
│   ├── hr_timesheet_merged.py
│   ├── leave_date.json
│   └── set_format.json
│
├── venv/
├── credentials.json
└── requirements.txt
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd QA-Automation-Public
```

```bash
python -m venv venv
source venv\script\activate
```

```bash
pip install -r requirements.txt
```
---

# 🚀 Execution Guide

Available Environment (ENVIRONMENT)
- dev
- stg

## 👨‍💼 EMPLOYEE AUTOMATION
### ⏱ Timesheet
📄 File: employee/timesheet_merged.py

Available Timesheet Format (TIMESHEET_FORMAT)
| Format    | Description      |
| --------- | ---------------- |
| sigmatech | Sigmatech        |
| bri       | InfoSys BRI      |
| cimb      | InfoSys CIMB     |
| mandiri   | Mandiri Inhealth |


Available Scenarios (TIMESHEET_PERIOD)
| Period    | Description    |
| --------- | -------------- |
| full      | 1–31 or 1–28   |
| halfh     | 1–15           |
| halft     | 16–31 or 16–28 |
| last      | 25–31 or 25–28 |

▶ Run Example
```bash
pytest employee\timesheet_merged.py --env=<ENVIRONMENT> --format=<TIMESHEET_FORMAT> --timesheet=<TIMESHEET_PERIOD> --headed
```

### 🌴 Leave
📄 File: employee/leave_merged.py

Available Leave Types (LEAVE_TYPES)
- unpaid
- child_wed
- sick
- baptism

Date Options (DATE_TYPE)
- begin
- end

▶ Run Example
```bash
pytest employee\leave_merged.py --env=<ENVIRONMENT> --leave=<LEAVE_TYPE> --date-type=<DATE_TYPE>
```

## 👩‍💼 HR AUTOMATION
### 📅 Holiday Management
📄 File: hr/holiday_merged.py

Avaliable Holiday Types (HOLIDAY_TYPE)
- public
- eid
- cbt
- cbp

Avaliable Date Options (DATE_TYPE)
- begin
- end

▶ Run Example
```bash
pytest hr\holiday_merged.py --env=<ENVIRONMENT> --holiday=<HOLIDAY_TYPE> --date-type=<DATE_TYPE> --slowmo=500
```

### ✅ Timesheet Approval
📄 File: hr/timesheet_merged.py

Avaliable Timesheet Actions (TIMESHEET_ACTION)
- approve
- reject

▶ Run
```bash
pytest hr\Timesheet_Merged.py --env=<ENVIRONMENT> --action=<TIMESHEET_ACTION>
```

### ❌ Leave Cancellation
📄 File: hr/cancel_leave.py

Available Leave Types (LEAVE_TYPES)
- unpaid
- child_wed
- sick
- baptism

▶ Run
```bash
pytest hr\Cancel-Leave.py --env=<ENVIRONMENT> --leave=<LEAVE_TYPE>
```

---

# 🎛 CLI Parameters
| Parameter     | Description                        |
| ------------- | ---------------------------------- |
| `--env`       | Select "dev" or "stg"              |
| `--timesheet` | Select timesheet scenario          |
| `--leave`     | Select leave type                  |
| `--date-type` | begin / end                        |
| `--holiday`   | Holiday type                       |
| `--action`    | approve / reject                   |
| `--headed`    | Run browser in UI mode             |
| `--headless`  | Run browser in CLI mode            |
| `--slowmo`    | Slow down execution (milliseconds) |

```bash
pytest -s --log-cli-level=INFO Timesheet\local.py --env= --username= --password= --headed
```