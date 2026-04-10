# ================= LIBRARY =================

import json
import logging
from pathlib import Path
import employee, hr, checksum
from playwright.sync_api import Playwright


# ================= PATH SETUP =================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"
STATIC_PATH = PROJECT_ROOT / "static_data.json"

with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as fc:
    cred = json.load(fc)

with open(STATIC_PATH, 'r', encoding='utf-8') as fp:
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

    logging.info(f"{step_name} completed successfully..")

    
# ================= EMPLOYEE: CREATE TIMESHEET =================

def test_timesheet_flow(playwright: Playwright, env_config, username, password):
    browser = playwright.chromium.launch(
        headless=False,
        args=[
            "--disable-dev-shm-usage",
            "--no-sandbox"
        ]
    )
    
    # ================= GET EMPLOYEE NAME =================
    employee_name = employee.get_employee_name(browser, env_config, username, password)

    logger.info(f"Employee: {employee_name}")

    timesheet_formats = stat["timesheet_format"]
    timesheet_types = stat["timesheet_type"]

    # ================= LOOP FORMAT =================
    for fmt, format_data in timesheet_formats.items():
        format_id = format_data["id"]
        if not format_id:
            logger.info(f"Skip {fmt} (no format id)")
            continue

        # ================= HR SET FORMAT =================
        hr_context = browser.new_context()
        hr_page = hr_context.new_page()

        hr.login_page(hr_page, env_config)
        hr.work_information(hr_page, employee_name)
        
        hr.set_format(hr_page, format_id)
        logger.info(f"Set Timesheet Format: {fmt.upper()}")

        # ================= DS ON =================
        hr.toggle_approval_using_space(hr_page, True)
        logger.info(f"Set Approval Space: ON completed successfully.")
        
        hr.submit_update(hr_page)
        logger.info(f"Update Employee Work History completed successfully.")

        hr_context.close()

        # ================= LOOP TIMESHEET TYPE =================
        for ts_type in timesheet_types:
            logger.info(f"{fmt.upper()} | TYPE: {ts_type.upper()}")

            # ================= EMPLOYEE CREATE =================
            emp_context = browser.new_context()
            emp_page = emp_context.new_page()

            employee.login_page(emp_page, env_config, username, password)
            employee.create_timesheet(emp_page, ts_type, fmt)
            logger.info(f"Create timesheet {fmt.upper()}-{ts_type.upper()} completed successfully.")
            
            emp_context.close()
            
            emp_context = browser.new_context()
            emp_page = emp_context.new_page()
            
            employee.login_page(emp_page, env_config, username, password)
            employee.download_timesheet(emp_page, env_config, fmt, ts_type)
            logger.info(f"Employee Download timesheet-{fmt.upper()}-{ts_type.upper()} completed successfully.")

            emp_context.close()

            # ================= HR APPROVAL =================
            hr_context = browser.new_context()
            hr_page = hr_context.new_page()

            hr.login_page(hr_page, env_config)
            
            input(logging.info("DS Approval action needed. Complete the DS process, then press ENTER to continue... "))

            hr.approve_timesheet(hr_page)
            logger.info(f"Timesheet approved by HR completed successfully.")
            
            hr.download_timesheet(hr_page, env_config, fmt, ts_type)
            logger.info(f"HR Download timesheet-{fmt.upper()}-{ts_type.upper()} completed successfully.")
            
            hr.reject_timesheet(hr_page)
            logger.info(f"Timesheet rejected by HR completed successfully.")
            
            hr_context.close()

            # ================= CHECKSUM =================
            # checksum.process_checksum(fmt)
            logger.info(f"Timesheet {fmt.upper()} Test completed successfully.\n")

    browser.close()