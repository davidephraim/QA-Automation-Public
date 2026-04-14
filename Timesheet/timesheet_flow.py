# ================= LIBRARY =================

import json
import logging
from pathlib import Path
import employee, hr, checksum
from playwright.sync_api import Playwright


# ================= PATH SETUP =================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"
STATIC_PATH = PROJECT_ROOT / "static_data.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)

with open(STATIC_PATH) as fp:
    stat = json.load(fp)
    

# ================= LOGGING =================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def log_step(page, step_name):
    screenshot_dir = BASE_DIR / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)

    page.screenshot(path=screenshot_dir / f"{step_name}.png")

    logging.info(f"{step_name} completed successfully.")

    
# ================= EMPLOYEE: CREATE TIMESHEET =================

def timesheet_flow(playwright: Playwright, env, username, password):
    browser = playwright.chromium.launch(
        headless=True,
        args=[
            "--disable-dev-shm-usage",
            "--no-sandbox"
        ]
    )
    
    # ================= GET EMPLOYEE NAME =================
    employee_name = employee.get_employee_name(browser, env, username, password)

    logger.info(f"Employee: {employee_name}")

    timesheet_formats = stat["timesheet_format"]
    timesheet_types = stat["timesheet_type"]

    # ================= LOOP FORMAT =================
    for fmt, format_data in timesheet_formats.items():
        format_id = format_data["id"]
        if not format_id:
            logger.info(f"Skip {fmt} (no format id)")
            continue

        logger.info(f"FORMAT: {fmt}")

        # ================= HR SET FORMAT =================
        hr_context = browser.new_context()
        hr_page = hr_context.new_page()

        hr.login_page(hr_page, env)
        hr.work_information(hr_page, employee_name)
        hr.set_format(hr_page, employee_name, format_id)
        hr.submit_update(hr_page)

        # ================= DS ON =================
        hr.toggle_approval_using_space(hr_page, True)
        hr.submit_update(hr_page)

        hr_context.close()


        # ================= LOOP TIMESHEET TYPE =================
        for ts_type in timesheet_types:
            logger.info(f"{fmt} | TYPE: {ts_type}")

            # ================= EMPLOYEE CREATE =================
            emp_context = browser.new_context()
            emp_page = emp_context.new_page()

            employee.login_page(emp_page, env, username, password)
            employee.create_timesheet(emp_page, ts_type, fmt)
            employee.download_timesheet(emp_page, env, fmt, ts_type)

            emp_context.close()

            # ================= HR APPROVAL =================
            hr_context = browser.new_context()
            hr_page = hr_context.new_page()

            hr.login_page(hr_page, env)
            hr.approve_timesheet(hr_page)
            hr.download_timesheet(hr_page, env, fmt, ts_type)

            hr_context.close()

            # ================= CHECKSUM =================
            checksum.process_checksum(fmt)

    browser.close()
    logger.info(f"Timesheet : {fmt}")