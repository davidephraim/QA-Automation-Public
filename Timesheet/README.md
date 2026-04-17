# 📌 Timesheet Flow

## 🧩 Overview

This feature automates the process of setting or updating <b>timesheet format</b> and create timesheet through <b>end-to-end (E2E) automated tests</b> using Playwright + Pytest.

It supports <b>multi-environment execution</b> and <b>dynamic credentials via CLI parameters</b>, making it suitable for scalable automation workflows.

> 💡 Ideal for regression testing, onboarding simulation, and automated data setup.

<br>

## 🚧 Status

**In Progress**—The automation is working for regular use, but some parts are still being improved. There's a known non-critical issue that will be fixed in a future update.

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
Timesheet/
├── Downloaded_timesheet/
│   ├── employee/
│   └── hr
│
├── screenshots/                # Auto-generated screenshots
│
├── checksum.py
├── conftest.py                 # Pytest configuration & CLI options
├── employee.py
├── hr.json
├── leave_date.json
├── local.py                    # Entry point for local execution (headed)
├── README.md
├── timesheet_flow.py
└── timesheet_format.json       # Main automation script
```
<br>

## 🧪 Test Type

**Automation / End-to-End (E2E Test)**

Covers full workflow:

1. HR sets employee timesheet format
2. Employee create timesheet on 4 different periods
3. Employee download timesheet
4. Wait for DS approval (DS on), auto checksum (DS off)
5. HR Approve, download, reject timesheet.

<br>

## ⚙️ Parameters

| Parameter        | Description                       |
|------------------|-----------------------------------|
| `--log-cli-level`| Enable logging output in terminal |
| `--env`          | Target environment (`dev`, `stg`) |
| `--format`       | Timesheet format (`full`, `bri`, `cimb`, ...) |
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
pytest -s --log-cli-level=INFO "Timesheet/timesheet_flow.py" \ 
--env=<ENVIRONMENT> \
--format=<TIMESHEET_FORMAT> \
--username=<USER_EMAIL> \
--password="<USER_PASSWD>"
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
pytest -s --log-cli-level=INFO "Timesheet/local.py" \
--env=<ENVIRONMENT> \
--format=<TIMESHEET_FORMAT> \
--username=<USER_EMAIL> \
--password="<USER_PASSWD>"
--headed
```

<br>

## 📊 Sample Output
### Docker 🐳
```bash
Timesheet/timesheet_flow.py::test_timesheet_flow 2026-04-15 08:47:41,199 - INFO - Get Employee Name completed successfully.

---------------------------------------------------- live log call ----------------------------------------------------
INFO     root:employee.py:36 Get Employee Name completed successfully.
2026-04-15 08:47:41,235 - INFO - Employee: Cappuccino
INFO     timesheet_flow:timesheet_flow.py:119 Employee: Cappuccino
2026-04-15 08:47:50,905 - INFO - DS ON
INFO     timesheet_flow:timesheet_flow.py:148 DS ON
2026-04-15 08:47:52,426 - INFO - [DS ON] CIMB | FULL
INFO     timesheet_flow:timesheet_flow.py:161 [DS ON] CIMB | FULL
2026-04-15 08:47:58,998 - INFO - Timesheet Existed. Reject timesheet using HR to retry completed successfully.
INFO     root:employee.py:36 Timesheet Existed. Reject timesheet using HR to retry completed successfully.
Press ENTER to continue...
Complete DS approval, then press ENTER...
2026-04-15 08:50:21,767 - INFO - timeout_hr_cimb_full completed successfully..
INFO     root:timesheet_flow.py:48 timeout_hr_cimb_full completed successfully..
2026-04-15 08:50:21,776 - WARNING - Timeout after 30s at step: HR Approve & Download
WARNING  timesheet_flow:timesheet_flow.py:29 Timeout after 30s at step: HR Approve & Download
Server is full. Make sure server is normal, then press ENTER to continue...
Complete DS approval, then press ENTER...
2026-04-15 08:54:53,506 - INFO - Renamed file to: DEV - HR - CIMB - full - Timesheet-Cappuccino-Februari-2026- Revision 238 - approved_1.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - CIMB - full - Timesheet-Cappuccino-Februari-2026- Revision 238 - approved_1.pdf
2026-04-15 08:55:03,013 - INFO - [DS ON] CIMB | HALFH
INFO     timesheet_flow:timesheet_flow.py:161 [DS ON] CIMB | HALFH
Complete DS approval, then press ENTER...
2026-04-15 08:55:23,685 - WARNING - Timesheet has been approved. Continue the process...
WARNING  root:hr.py:45 Timesheet has been approved. Continue the process...
2026-04-15 08:55:54,572 - INFO - timeout_hr_cimb_halfh completed successfully..
INFO     root:timesheet_flow.py:48 timeout_hr_cimb_halfh completed successfully..
2026-04-15 08:55:54,572 - WARNING - Timeout after 30s at step: HR Approve & Download
WARNING  timesheet_flow:timesheet_flow.py:29 Timeout after 30s at step: HR Approve & Download
Server is full. Make sure server is normal, then press ENTER to continue...
Complete DS approval, then press ENTER...
2026-04-15 08:56:27,637 - INFO - Renamed file to: DEV - HR - CIMB - halfh - Timesheet-Cappuccino-Februari-2026- Revision 239 - approved_1.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - CIMB - halfh - Timesheet-Cappuccino-Februari-2026- Revision 239 - approved_1.pdf
2026-04-15 08:56:36,220 - INFO - [DS ON] CIMB | HALFT
INFO     timesheet_flow:timesheet_flow.py:161 [DS ON] CIMB | HALFT
Complete DS approval, then press ENTER...
2026-04-15 08:57:23,243 - INFO - Renamed file to: DEV - HR - CIMB - halft - Timesheet-Cappuccino-Februari-2026- Revision 240 - approved_1.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - CIMB - halft - Timesheet-Cappuccino-Februari-2026- Revision 240 - approved_1.pdf
2026-04-15 08:57:32,569 - INFO - [DS ON] CIMB | LAST
INFO     timesheet_flow:timesheet_flow.py:161 [DS ON] CIMB | LAST
Complete DS approval, then press ENTER...
2026-04-15 08:58:51,643 - INFO - Renamed file to: DEV - HR - CIMB - last - Timesheet-Cappuccino-Februari-2026- Revision 241 - approved_1.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - CIMB - last - Timesheet-Cappuccino-Februari-2026- Revision 241 - approved_1.pdf
2026-04-15 08:59:08,799 - INFO - DS OFF
INFO     timesheet_flow:timesheet_flow.py:243 DS OFF
2026-04-15 08:59:10,252 - INFO - [DS OFF] CIMB | FULL
INFO     timesheet_flow:timesheet_flow.py:256 [DS OFF] CIMB | FULL
2026-04-15 08:59:37,275 - INFO - Renamed file to: DEV - HR - CIMB - full - Timesheet-Cappuccino-Februari-2026- Revision 242 - approved_ds_off.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - CIMB - full - Timesheet-Cappuccino-Februari-2026- Revision 242 - approved_ds_off.pdf
2026-04-15 08:59:37,304 - INFO - Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:31 Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 08:59:37,304 - INFO - Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:32 Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 08:59:37,304 - INFO - CHECKSUM PASSED
INFO     checksum:checksum.py:35 CHECKSUM PASSED
2026-04-15 08:59:37,304 - INFO - CHECKSUM RESULT: PASS (cimb-full)
INFO     timesheet_flow:timesheet_flow.py:63 CHECKSUM RESULT: PASS (cimb-full)
2026-04-15 08:59:41,971 - INFO - [DS OFF] CIMB | HALFH
INFO     timesheet_flow:timesheet_flow.py:256 [DS OFF] CIMB | HALFH
2026-04-15 09:00:08,840 - INFO - Renamed file to: DEV - HR - CIMB - halfh - Timesheet-Cappuccino-Februari-2026- Revision 243 - approved_ds_off.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - CIMB - halfh - Timesheet-Cappuccino-Februari-2026- Revision 243 - approved_ds_off.pdf
2026-04-15 09:00:08,847 - INFO - Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:31 Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 09:00:08,847 - INFO - Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:32 Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 09:00:08,848 - INFO - CHECKSUM PASSED
INFO     checksum:checksum.py:35 CHECKSUM PASSED
2026-04-15 09:00:08,848 - INFO - CHECKSUM RESULT: PASS (cimb-halfh)
INFO     timesheet_flow:timesheet_flow.py:63 CHECKSUM RESULT: PASS (cimb-halfh)
2026-04-15 09:00:13,478 - INFO - [DS OFF] CIMB | HALFT
INFO     timesheet_flow:timesheet_flow.py:256 [DS OFF] CIMB | HALFT
2026-04-15 09:00:41,859 - INFO - Renamed file to: DEV - HR - CIMB - halft - Timesheet-Cappuccino-Februari-2026- Revision 244 - approved_ds_off.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - CIMB - halft - Timesheet-Cappuccino-Februari-2026- Revision 244 - approved_ds_off.pdf
2026-04-15 09:00:41,866 - INFO - Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:31 Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 09:00:41,866 - INFO - Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:32 Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 09:00:41,866 - INFO - CHECKSUM PASSED
INFO     checksum:checksum.py:35 CHECKSUM PASSED
2026-04-15 09:00:41,866 - INFO - CHECKSUM RESULT: PASS (cimb-halft)
INFO     timesheet_flow:timesheet_flow.py:63 CHECKSUM RESULT: PASS (cimb-halft)
2026-04-15 09:00:46,549 - INFO - [DS OFF] CIMB | LAST
INFO     timesheet_flow:timesheet_flow.py:256 [DS OFF] CIMB | LAST
2026-04-15 09:01:16,251 - INFO - Renamed file to: DEV - HR - CIMB - last - Timesheet-Cappuccino-Februari-2026- Revision 245 - approved_ds_off.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - CIMB - last - Timesheet-Cappuccino-Februari-2026- Revision 245 - approved_ds_off.pdf
2026-04-15 09:01:16,257 - INFO - Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:31 Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 09:01:16,257 - INFO - Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:32 Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 09:01:16,257 - INFO - CHECKSUM PASSED
INFO     checksum:checksum.py:35 CHECKSUM PASSED
2026-04-15 09:01:16,257 - INFO - CHECKSUM RESULT: PASS (cimb-last)
INFO     timesheet_flow:timesheet_flow.py:63 CHECKSUM RESULT: PASS (cimb-last)
2026-04-15 09:01:20,936 - INFO - ========== END FORMAT: CIMB ==========

INFO     timesheet_flow:timesheet_flow.py:319 ========== END FORMAT: CIMB ==========

PASSED

============================================ 1 passed in 828.40s (0:13:48) ============================================
```

### Local 💻
```bash
Timesheet/timesheet_flow.py::test_timesheet_flow 2026-04-15 13:20:53,947 - INFO - Get Employee Name completed successfully.

---------------------------------------------------- live log call ----------------------------------------------------
INFO     root:employee.py:36 Get Employee Name completed successfully.
2026-04-15 13:20:53,959 - INFO - Employee: Cappuccino
INFO     timesheet_flow:timesheet_flow.py:119 Employee: Cappuccino
2026-04-15 13:21:19,696 - INFO - DS ON
INFO     timesheet_flow:timesheet_flow.py:148 DS ON
2026-04-15 13:21:21,078 - INFO - [DS ON] BRI | FULL
INFO     timesheet_flow:timesheet_flow.py:161 [DS ON] BRI | FULL
2026-04-15 13:21:34,412 - INFO - Timesheet Existed. Reject timesheet using HR to retry completed successfully.
INFO     root:employee.py:36 Timesheet Existed. Reject timesheet using HR to retry completed successfully.
Press ENTER to continue...
Complete DS approval, then press ENTER...
2026-04-15 13:25:16,477 - INFO - Renamed file to: DEV - HR - BRI - full - Timesheet-Cappuccino-Februari-2026- Revision 213 - approved_1.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - BRI - full - Timesheet-Cappuccino-Februari-2026- Revision 213 - approved_1.pdf
2026-04-15 13:25:58,056 - INFO - [DS ON] BRI | HALFH
INFO     timesheet_flow:timesheet_flow.py:161 [DS ON] BRI | HALFH
Complete DS approval, then press ENTER...
2026-04-15 13:28:12,092 - INFO - Renamed file to: DEV - HR - BRI - halfh - Timesheet-Cappuccino-Februari-2026- Revision 214 - approved_1.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - BRI - halfh - Timesheet-Cappuccino-Februari-2026- Revision 214 - approved_1.pdf
2026-04-15 13:28:53,761 - INFO - [DS ON] BRI | HALFT
INFO     timesheet_flow:timesheet_flow.py:161 [DS ON] BRI | HALFT
Complete DS approval, then press ENTER...
2026-04-15 13:30:59,002 - INFO - Renamed file to: DEV - HR - BRI - halft - Timesheet-Cappuccino-Februari-2026- Revision 215 - approved_1.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - BRI - halft - Timesheet-Cappuccino-Februari-2026- Revision 215 - approved_1.pdf
2026-04-15 13:31:34,229 - INFO - [DS ON] BRI | LAST
INFO     timesheet_flow:timesheet_flow.py:161 [DS ON] BRI | LAST
Complete DS approval, then press ENTER...
2026-04-15 13:33:07,935 - INFO - Renamed file to: DEV - HR - BRI - last - Timesheet-Cappuccino-Februari-2026- Revision 216 - approved_1.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - BRI - last - Timesheet-Cappuccino-Februari-2026- Revision 216 - approved_1.pdf
2026-04-15 13:33:58,909 - INFO - DS OFF
INFO     timesheet_flow:timesheet_flow.py:243 DS OFF
2026-04-15 13:34:00,631 - INFO - [DS OFF] BRI | FULL
INFO     timesheet_flow:timesheet_flow.py:256 [DS OFF] BRI | FULL
2026-04-15 13:35:29,959 - INFO - Renamed file to: DEV - HR - BRI - full - Timesheet-Cappuccino-Februari-2026- Revision 217 - approved_ds_off.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - BRI - full - Timesheet-Cappuccino-Februari-2026- Revision 217 - approved_ds_off.pdf
2026-04-15 13:35:30,015 - INFO - Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:31 Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 13:35:30,016 - INFO - Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:32 Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 13:35:30,016 - INFO - CHECKSUM PASSED
INFO     checksum:checksum.py:35 CHECKSUM PASSED
2026-04-15 13:35:30,017 - INFO - CHECKSUM RESULT: PASS (bri-full)
INFO     timesheet_flow:timesheet_flow.py:63 CHECKSUM RESULT: PASS (bri-full)
2026-04-15 13:35:35,076 - INFO - [DS OFF] BRI | HALFH
INFO     timesheet_flow:timesheet_flow.py:256 [DS OFF] BRI | HALFH
2026-04-15 13:37:16,796 - INFO - Renamed file to: DEV - HR - BRI - halfh - Timesheet-Cappuccino-Februari-2026- Revision 218 - approved_ds_off.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - BRI - halfh - Timesheet-Cappuccino-Februari-2026- Revision 218 - approved_ds_off.pdf
2026-04-15 13:37:16,818 - INFO - Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:31 Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 13:37:16,818 - INFO - Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:32 Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 13:37:16,819 - INFO - CHECKSUM PASSED
INFO     checksum:checksum.py:35 CHECKSUM PASSED
2026-04-15 13:37:16,819 - INFO - CHECKSUM RESULT: PASS (bri-halfh)
INFO     timesheet_flow:timesheet_flow.py:63 CHECKSUM RESULT: PASS (bri-halfh)
2026-04-15 13:37:21,292 - INFO - [DS OFF] BRI | HALFT
INFO     timesheet_flow:timesheet_flow.py:256 [DS OFF] BRI | HALFT
2026-04-15 13:39:01,424 - INFO - Renamed file to: DEV - HR - BRI - halft - Timesheet-Cappuccino-Februari-2026- Revision 219 - approved_ds_off.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - BRI - halft - Timesheet-Cappuccino-Februari-2026- Revision 219 - approved_ds_off.pdf
2026-04-15 13:39:01,437 - INFO - Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:31 Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 13:39:01,438 - INFO - Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:32 Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 13:39:01,438 - INFO - CHECKSUM PASSED
INFO     checksum:checksum.py:35 CHECKSUM PASSED
2026-04-15 13:39:01,438 - INFO - CHECKSUM RESULT: PASS (bri-halft)
INFO     timesheet_flow:timesheet_flow.py:63 CHECKSUM RESULT: PASS (bri-halft)
2026-04-15 13:39:06,779 - INFO - [DS OFF] BRI | LAST
INFO     timesheet_flow:timesheet_flow.py:256 [DS OFF] BRI | LAST
2026-04-15 13:40:40,791 - INFO - Renamed file to: DEV - HR - BRI - last - Timesheet-Cappuccino-Februari-2026- Revision 220 - approved_ds_off.pdf
INFO     timesheet_flow:timesheet_flow.py:100 Renamed file to: DEV - HR - BRI - last - Timesheet-Cappuccino-Februari-2026- Revision 220 - approved_ds_off.pdf
2026-04-15 13:40:40,808 - INFO - Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:31 Static Hash     : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 13:40:40,809 - INFO - Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
INFO     checksum:checksum.py:32 Downloaded Hash : 38c9792d725c45dd431699e6a3b0f0f8e17c63c9ac7331387ee30dcc6e42a511
2026-04-15 13:40:40,809 - INFO - CHECKSUM PASSED
INFO     checksum:checksum.py:35 CHECKSUM PASSED
2026-04-15 13:40:40,809 - INFO - CHECKSUM RESULT: PASS (bri-last)
INFO     timesheet_flow:timesheet_flow.py:63 CHECKSUM RESULT: PASS (bri-last)
2026-04-15 13:40:45,300 - INFO - ========== END FORMAT: BRI ==========

INFO     timesheet_flow:timesheet_flow.py:319 ========== END FORMAT: BRI ==========
```

---

## 📌 Notes
- Ensure valid credentials are configured in `credentials.json`.
- Static test data is loaded from `static_data.json`.
- Screenshot will be generated automatically for each completed step.
- Execution duration may vary or fail depending on the environment performance.
- Repeat the [Docker Setup](#-docker-setup) after changing the code.
---

## 🤝 Contributing
>🐛 Found an issue? Please open an issue or submit a pull request. Thank you so much 🫡.
