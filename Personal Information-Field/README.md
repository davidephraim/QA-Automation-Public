[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
# 📌 Set Personal Information

## 🧩 Overview

This feature automates the process of setting or updating <b>employee personal information</b> through <b>end-to-end (E2E) automated tests</b> using Playwright + Pytest.

It supports <b>multi-environment execution</b> and <b>dynamic credentials via CLI parameters</b>, making it suitable for scalable automation workflows. <b>Built with:</b>

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/-playwright-%232EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

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
├── screenshots/                # Auto-generated screenshots
│
├── conftest.py                 # Pytest configuration & CLI options
├── local.py                    # Entry point for local execution (headed)
├── README.md
├── set_personal_info (old_ver).py
└── set_personal_info.py        # Main automation script runs on Docker
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

| Parameter        | Description                       |
|------------------|-----------------------------------|
| `--log-cli-level`| Enable logging output in terminal |
| `--env`          | Target environment (`dev`, `stg`) |
| `--username`     | User login email                  |
| `--password`     | User password                     |
| `--headed`       | Run browser in UI mode            |
| `--headless`     | Run browser in CLI mode           |
| `--slowmo`       | Slow down execution (milliseconds)|

---

## 🚀 Setup & Execution Guide
This project can be run using `Docker` or locally by installing all dependencies in a virtual environment (`venv`). Follow the steps below to set it up:

### 🐳 Docker Setup
#### 1. Setup `credentials.json`
Open `credentials.template.json` and fill all the information about link, username, password, then rename file to `credentials.json`.

#### 2. Build docker image
```bash
docker build -t playwright-space .
```

#### 3. Verify Docker image
```docker image ls``` <b>or</b> ```bash docker images ```

#### 4. Run automation
```bash
docker run -it --rm <IMG_ID> \ 
pytest -s --log-cli-level=INFO "Personal Information-Field/set_personal_info.py" \ 
--env=<ENVIRONMENT> \
--username=<USER_EMAIL> \
--password=<USER_PASSWD>
```

---

### 💻 Local Setup (Headed Mode)
#### 1. Setup `credentials.json`
Open `credentials.template.json` and fill all the information about link, username, password, then rename file to `credentials.json`.

#### 2. Create virtual environment
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

#### 3. Run automation (headed browser)
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
Personal Information-Field/set_personal_info.py::test_set_profile Skip company regulation - checkbox count: 0

---------------------------------------------------- live log call -----------------------------------------------------
INFO     root:set_personal_info.py:41 Get Employee Name completed successfully.
INFO     root:set_personal_info.py:439 Employee name detected: Dedi Kurniawan
INFO     root:set_personal_info.py:41 Set Bank Account by HR completed successfully.
INFO     root:set_personal_info.py:41 Set NPWP by HR completed successfully.
INFO     root:set_personal_info.py:41 General—Personal completed successfully.
INFO     root:set_personal_info.py:41 General—Family completed successfully.
INFO     root:set_personal_info.py:41 Education—Formal & Informal completed successfully.
INFO     root:set_personal_info.py:41 Education—Course completed successfully.
INFO     root:set_personal_info.py:41 Foreign Language completed successfully.
INFO     root:set_personal_info.py:41 Activity completed successfully.
INFO     root:set_personal_info.py:41 Working Experience completed successfully.
INFO     root:set_personal_info.py:41 Additional—Questionnair completed successfully.
INFO     root:set_personal_info.py:41 Additional—Attachment completed successfully.
INFO     root:set_personal_info.py:41 Additional—PTKP completed successfully.
PASSED

================================================== 1 passed in 49.65s ==================================================
```

### Local 💻
```bash
Personal Information-Field/local.py::test_set_profile Skip company regulation - checkbox count: 0

---------------------------------------------------- live log call ----------------------------------------------------
INFO     root:local.py:41 Get Employee Name completed successfully.
INFO     root:local.py:439 Employee name detected: Dedi Kurniawan
INFO     root:local.py:41 Set Bank Account by HR completed successfully.
INFO     root:local.py:41 Set NPWP by HR completed successfully.
INFO     root:local.py:41 General—Personal completed successfully.
INFO     root:local.py:41 General—Family completed successfully.
INFO     root:local.py:41 Education—Formal & Informal completed successfully.
INFO     root:local.py:41 Education—Course completed successfully.
INFO     root:local.py:41 Foreign Language completed successfully.
INFO     root:local.py:41 Activity completed successfully.
INFO     root:local.py:41 Working Experience completed successfully.
INFO     root:local.py:41 Additional—Questionnair completed successfully.
INFO     root:local.py:41 Additional—Attachment completed successfully.
INFO     root:local.py:41 Additional—PTKP completed successfully.
PASSED

================================================= 1 passed in 55.94s ==================================================
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

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/davidephraim/QA-Automation-Public.svg?style=for-the-badge
[contributors-url]: https://github.com/davidephraim/QA-Automation-Public/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/davidephraim/QA-Automation-Public.svg?style=for-the-badge
[forks-url]: https://github.com/davidephraim/QA-Automation-Public/network/members
[stars-shield]: https://img.shields.io/github/stars/davidephraim/QA-Automation-Public.svg?style=for-the-badge
[stars-url]: https://github.com/davidephraim/QA-Automation-Public/stargazers
[issues-shield]: https://img.shields.io/github/issues/davidephraim/QA-Automation-Public.svg?style=for-the-badge
[issues-url]: https://github.com/davidephraim/QA-Automation-Public/issues
[linkedin-shield]: https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://linkedin.com/in/david--ephraim/
<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
<!-- https://github.com/Ileriayo/markdown-badges -->