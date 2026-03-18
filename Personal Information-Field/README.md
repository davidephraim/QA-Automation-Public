# 📌 Set Personal Information

## 🧩 Overview

This feature automates the process of setting or updating user personal information through end-to-end (E2E) automated tests.

It supports multiple environments and dynamic user credentials via CLI parameters, enabling flexible and scalable test execution.

> 💡 Ideal for regression testing, onboarding simulation, and automated data setup.

<br>

## ✅ Status

**Stable** – Fully tested and ready for daily automation usage 🚀

<br>

## ✨ Key Features

- 🔄 Full E2E automation flow (Employee + HR interaction)
- 🌐 Supports multi-environment execution (`dev`, `stg`, etc.)
- 🔐 Dynamic login via CLI parameters
- 📊 Real-time step-by-step logging
- 📁 Handles file uploads (image & PDF)
- 🧱 Modular function design (easy to maintain & extend)

---

## 📂 File Structure
`set_personal_info.py`

<br>

## 🧪 Test Type

**Automation / End-to-End (E2E Test)**

<br>

## ⚙️ Parameters

| Parameter         | Description                       |
|------------------|-----------------------------------|
| `--log-cli-level`| Enable logging output in terminal |
| `--env`          | Target environment (`dev`, `stg`) |
| `--username`     | User login email                  |
| `--password`     | User password                     |
| `--name`         | User full name                    |
| `--headed`       | Run browser in UI mode            |

---

## 🚀 Execution

```bash
pytest -s --log-cli-level=INFO \
  set_personal_info.py \
  --env=<ENVIRONMENT> \
  --username=<USER_EMAIL> \
  --password=<USER_PASSWD> \
  --name=<USER_NAME> \
  --headed
```

<br>

## 📊 Sample Output
```bash
set_personal_info.py::test_set_profile[chromium]

---------------------------------------------------- live log call ----------------------------------------------------

INFO     root:set_personal_info.py:30 General Personal Information setup completed successfully.
INFO     root:set_personal_info.py:30 NPWP setup completed successfully.
INFO     root:set_personal_info.py:30 Family Information setup completed successfully.
INFO     root:set_personal_info.py:30 Education formal and informal setup completed successfully.
INFO     root:set_personal_info.py:30 Education course training setup completed successfully.
INFO     root:set_personal_info.py:30 Foreign language setup completed successfully.
INFO     root:set_personal_info.py:30 Activity setup completed successfully.
INFO     root:set_personal_info.py:30 Working Experience setup completed successfully.
INFO     root:set_personal_info.py:30 Questionnair setup completed successfully.
INFO     root:set_personal_info.py:30 Attachment setup completed successfully.
INFO     root:set_personal_info.py:30 PTKP status setup completed successfully.

PASSED

================================================= 1 passed in 39.79s ==================================================
```

---

## 📌 Notes
- Ensure valid credentials are configured in credentials.json.
- Static test data is loaded from static_data.json.
- Execution time may vary depending on environment performance.
- NPWP setup runs in a separate browser session (HR role).