# 📌 Set Personal Information

## 🧩 Overview

This feature automates the process of setting or updating <b>employee personal information</b> through <b>end-to-end (E2E) automated tests</b> using Playwright + Pytest.

It supports <b>multi-environment execution</b> and <b>dynamic credentials via CLI parameters</b>, making it suitable for scalable automation workflows.

> 💡 Ideal for regression testing, onboarding simulation, and automated data setup.

<br>

## ✅ Status

**Stable**—Fully tested and ready for daily automation usage.

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
- 📸 Automatic screenshot capture per step

---

## 📂 File Structure

```
Personal Information-Field/
│
├── __pycache__/
├── .pytest_cache/
├── screenshots/                # Auto-generated screenshots
│
├── conftest.py                 # Pytest configuration & CLI options
├── local.py                    # Entry point for local execution (headed)
├── README.md
├── set_personal_info (old_ver).py
└── set_personal_info.py        # Main automation script
```

<br>

## 🧪 Test Type

**Automation / End-to-End (E2E Test)**

Covers full workflow:

1. HR sets NPWP
2. Employee completes personal information
3. Employee fills supporting data
4. Employee uploads attachments

<br>

## ⚙️ Parameters

| Parameter         | Description                       |
|------------------|-----------------------------------|
| `--log-cli-level`| Enable logging output in terminal |
| `--env`          | Target environment (`dev`, `stg`) |
| `--username`     | User login email                  |
| `--password`     | User password                     |

---

## 🚀 Setup & Execution Guide
“This project can be run using `Docker` or locally by installing all dependencies in a virtual environment (`venv`). Follow the steps below to set it up:”

### 🐳 Docker Setup
#### 1. Build docker image
```bash
docker build -t playwright-space .
```

#### 2. Verify Docker image
```docker image ls``` <b>or</b> ```bash docker images ```

#### 3. Run automation
```bash
docker run --rm <IMG_ID> \ 
pytest -s --log-cli-level=INFO "Personal Information-Field/set_personal_info.py" \ 
--env=<ENVIRONMENT> \
--username=<USER_EMAIL> \
--password=<USER_PASSWD>
```

---

### 💻 Local Setup (Headed Mode)
#### 1. Create virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

#### 2. Run automation (headed browser)
```bash
pytest -s --log-cli-level=INFO "Personal Information-Field/local.py" \
--env=<ENVIRONMENT> \
--username=<USER_EMAIL> \
--password=<USER_PASSWD>
```

<br>

## 📊 Sample Output
### Docker 🐳
```bash
Personal Information-Field/set_personal_info.py::test_set_profile

-------------------------------- live log call ---------------------------------
INFO     root:set_personal_info.py:47 E-sign—company regulation completed successfully.
Skip company regulation - checkbox count: 0
INFO     root:set_personal_info.py:47 Get Employee Name completed successfully.
INFO     root:set_personal_info.py:428 Employee name detected: Tongcai
INFO     root:set_personal_info.py:47 Set Bank Account by HR completed successfully.
INFO     root:set_personal_info.py:47 Set NPWP by HR completed successfully.
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

============================== 1 passed in 56.50s ==============================
```

### Local 💻
```bash
Personal Information-Field/local.py::test_set_profile

---------------------------------------------------- live log call ----------------------------------------------------
INFO     root:local.py:47 E-sign—company regulation completed successfully.
Skip company regulation - checkbox count: 0
INFO     root:local.py:47 Get Employee Name completed successfully.
INFO     root:local.py:428 Employee name detected: Caipo
INFO     root:local.py:47 Set Bank Account by HR completed successfully.
INFO     root:local.py:47 Set NPWP by HR completed successfully.
INFO     root:local.py:47 General—Personal completed successfully.
INFO     root:local.py:47 General—Family completed successfully.
INFO     root:local.py:47 Education—Formal & Informal completed successfully.
INFO     root:local.py:47 Education—Course completed successfully.
INFO     root:local.py:47 Foreign Language completed successfully.
INFO     root:local.py:47 Activity completed successfully.
INFO     root:local.py:47 Working Experience completed successfully.
INFO     root:local.py:47 Additional—Questionnair completed successfully.
INFO     root:local.py:47 Additional—Attachment completed successfully.
INFO     root:local.py:47 Additional—PTKP completed successfully.
PASSED

================================================= 1 passed in 57.30s ==================================================
```

---

## 📌 Notes
- Ensure valid credentials are configured in `credentials.json`.
- Static test data is loaded from `static_data.json`.
- NPWP configuration is executed using a separate browser session (HR role).
- Screenshot will be generated automatically for each completed step.
- Execution duration may vary or fail depending on the environment performance.
- Repeat the [Docker Setup](#-docker-setup) after changing the code.
---

## 🤝 Contributing
>🐛 Found an issue? Please open an issue or submit a pull request. Thank you so much 🫡.