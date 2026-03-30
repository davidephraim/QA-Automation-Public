# 📌 Set Personal Information

## 🧩 Overview

This feature automates the process of setting or updating user personal information through end-to-end (E2E) automated tests.

It supports multiple environments and dynamic user credentials via CLI parameters, enabling flexible and scalable test execution.

> 💡 Ideal for regression testing, onboarding simulation, and automated data setup.

<br>

## 🚧 Status

**In Progress**—The automation is working for regular use, but some parts are still being improved. There’s a known non-critical issue that will be fixed in a future update.

<br>

## ✨ Key Features

- 🔄 Full E2E automation flow (Employee + HR interaction)
- 🌐 Supports multi-environment execution (`dev`, `stg`)
- 🔐 Dynamic login via CLI parameters
- 📊 Step-by-step logging output
- 📁 Supports upload file automation (image & PDF)
- 🧱 Modular function structure (easy to extend)
- 🐳 Fully containerized using Docker
- 💻 Cross-platform (Windows, Linux, CI/CD)

---

## 📂 File Structure
<b>`set_personal_info.py`</b>

```
Personal Information-Field/
│
├── __pycache__
├── screenshots/
├── conftest.py
├── README.md
├── set_personal_info (old_ver).py
└── set_personal_info.py
```

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

---

## 🐳 Docker Setup & Execution

### 1. Build docker image
```bash
docker build -t playwright-space:set_personal_info .
```

### 2. Check docker image
```docker image ls``` <b>or</b> ```bash docker images ```

### 3. Code execution
```bash
docker run --rm <IMG_ID> \ 
pytest -s --log-cli-level=INFO "Personal Information-Field/set_personal_info.py" \ 
--env=<ENVIRONMENT> \
--username=<USER_EMAIL> \
--password=<USER_PASSWD> \
--name=<USER_NAME>
```

<br>

## 📊 Sample Output
```bash
Personal Information-Field/set_personal_info.py::test_set_profile

-------------------------------- live log call ---------------------------------
INFO     root:set_personal_info.py:47 Set NPWP by HR completed successfully.
INFO     root:set_personal_info.py:47 E-sign—company regulation completed successfully.
INFO     root:set_personal_info.py:47 General—Personal completed successfully.
INFO     root:set_personal_info.py:47 General—Family completed successfully.
INFO     root:set_personal_info.py:47 Education—Formal & Informal completed successfully.
INFO     root:set_personal_info.py:47 Education—Course completed successfully.
INFO     root:set_personal_info.py:47 Foreign Language completed successfully.
INFO     root:set_personal_info.py:47 Activity completed successfully.
INFO     root:set_personal_info.py:47 Working Experience completed successfully.
INFO     root:set_personal_info.py:47 Additional—Questionnair completed successfully.
INFO     root:set_personal_info.py:47 Additional—Attachment completed successfully.
INFO     root:set_personal_info.py:47 Additional—PTKP completed successfully.
PASSED

============================== 1 passed in 37.60s ==============================
```

---

## 📌 Notes
- Ensure valid credentials are configured in credentials.json.
- Static test data is loaded from static_data.json.
- Execution time may vary depending on environment performance.
- NPWP setup runs in a separate browser session (HR role).
- Repeat the [Docker Setup](#-docker-setup--execution) after changing the code.