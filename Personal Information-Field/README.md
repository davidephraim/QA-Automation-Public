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
├── .pytest_cache
├── screenshots/
├── conftest.py
├── README.md
├── set_personal_info (old_ver).py
├── set_personal_info.py
│
└── File_test/
    ├── sample.jpg
    └── sample.pdf
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
docker build -t playwright-personal-info .
```

### 2. Check docker image
```bash
docker images ls
```

### 3. Code execution
```bash
docker run --rm <IMG_ID> \ 
pytest -s --log-cli-level=INFO "Personal Information-Field/set_test.py" \ 
--env=<ENVIRONMENT> \
--username=<USER_EMAIL> \
--password=<USER_PASSWD> \
--name=<USER_NAME>
```

<br>

## 📊 Sample Output
```bash
Personal Information-Field/set_test.py::test_set_profile

-------------------------------- live log call ---------------------------------
INFO     root:set_test.py:47 general_personal completed successfully.
INFO     root:set_test.py:47 npwp completed successfully.
INFO     root:set_test.py:47 family completed successfully.
INFO     root:set_test.py:47 formal education completed successfully.
INFO     root:set_test.py:47 informal education completed successfully.
INFO     root:set_test.py:47 foreign lang completed successfully.
INFO     root:set_test.py:47 activity completed successfully.
INFO     root:set_test.py:47 working completed successfully.
INFO     root:set_test.py:47 questionnair completed successfully.
INFO     root:set_test.py:47 attachment completed successfully.
INFO     root:set_test.py:47 ptkp completed successfully.
PASSED

============================== 1 passed in 47.12s ==============================
```

---

## 📌 Notes
- Ensure valid credentials are configured in credentials.json.
- Static test data is loaded from static_data.json.
- Execution time may vary depending on environment performance.
- NPWP setup runs in a separate browser session (HR role).

docker image ls
