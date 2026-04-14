# ================= LIBRARY =================

import json
import logging
from pathlib import Path
import employee, hr, checksum
from playwright.sync_api import Playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# ================= PATH SETUP =================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"
STATIC_PATH = PROJECT_ROOT / "static_data.json"

with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as fc:
    cred = json.load(fc)

with open(STATIC_PATH, 'r', encoding='utf-8') as fp:
    stat = json.load(fp)
    

# ================= TIMEOUT HANDLER =================

def wait_if_timeout(step_name):
    logger.warning(f"Timeout after 30s at step: {step_name}")
    input("Server is full. Make sure server is normal, then press ENTER to continue...")
    
    
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

def test_timesheet_flow(playwright: Playwright, env_config, username, password, company_format):
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
        # FILTER FORMAT
        if company_format != "full" and fmt != company_format:
            continue
        
        format_id = format_data["id"]
        if not format_id:
            logger.info(f"Skip {fmt} (no format id)")
            continue

        # ================= HR LOGIN =================
        while True:
            try:
                hr_context = browser.new_context()
                hr_page = hr_context.new_page()
                hr.login_page(hr_page, env_config)
                break
            except PlaywrightTimeoutError:
                log_step(hr_page, f"timeout_hr_login")
                wait_if_timeout(f"HR Login")
                hr_context.close()
                
        while True:
            try:
                hr.work_information(hr_page, employee_name)
                break
            except PlaywrightTimeoutError:
                log_step(hr_page, f"timeout_hr_work_information")
                wait_if_timeout(f"HR Work Information")
                
        while True:
            try:
                hr.set_format(hr_page, format_id)
                logger.info(f"Set Timesheet Format: {fmt.upper()}")
                break
            except PlaywrightTimeoutError:
                log_step(hr_page, f"timeout_hr_set_format")
                wait_if_timeout(f"HR Set format")
                

        # ================= DS ON =================
        while True:
            try:
                hr.toggle_approval_using_space(hr_page, True)
                logger.info(f"Set Approval Space: ON completed successfully.")
                break
            except PlaywrightTimeoutError:
                log_step(hr_page, f"timeout_hr_approval_space")
                wait_if_timeout(f"HR Approval using Space")
        
        while True:
            try:
                hr.submit_update(hr_page)
                logger.info(f"Update Employee Work History completed successfully.")
                break
            except PlaywrightTimeoutError:
                log_step(hr_page, f"timeout_hr_submit_update")
                wait_if_timeout(f"HR sbmit update")

        hr_context.close()

        # ================= LOOP TIMESHEET TYPE =================
        for ts_type in timesheet_types:
            logger.info(f"{fmt.upper()} | TYPE: {ts_type.upper()}")

            
            # ================= EMPLOYEE CREATE TIMESHEET =================

            # Emloyee Login
            while True:
                try:
                    emp_context = browser.new_context()
                    emp_page = emp_context.new_page()
                    employee.login_page(emp_page, env_config, username, password)
                    break
                except PlaywrightTimeoutError:
                    log_step(emp_page, f"timeout_employee_login")
                    wait_if_timeout(f"Employee Login")
                    emp_context.close()
            
            # Employee Create Timesheet
            while True:
                try:
                    employee.create_timesheet(emp_page, ts_type, fmt)
                    logger.info(f"Create timesheet {fmt.upper()}-{ts_type.upper()} completed successfully.")
                    break
                except PlaywrightTimeoutError:
                    log_step(emp_page, f"timeout_employee_create{fmt}_{ts_type}")
                    wait_if_timeout(f"Create Timesheet {fmt}-{ts_type}")
            
            emp_context.close()
            
            
            # ================= EMPLOYEE DOWNLOAD TIMESHEET =================
            
            # Employee Login
            while True:
                try:
                    emp_context = browser.new_context()
                    emp_page = emp_context.new_page()
                    employee.login_page(emp_page, env_config, username, password)
                    break
                except PlaywrightTimeoutError:
                    log_step(emp_page, f"timeout_employee_login")
                    wait_if_timeout(f"Employee Login")
                    emp_context.close()
            
            # Employee Timesheet Download
            while True:
                try:
                    employee.download_timesheet(emp_page, env_config, fmt, ts_type)
                    logger.info(f"Employee Download timesheet-{fmt.upper()}-{ts_type.upper()} completed successfully.")
                    break
                except PlaywrightTimeoutError:
                    log_step(emp_page, f"timeout_employee_download_{fmt}_{ts_type}")
                    wait_if_timeout(f"Employee Download Timesheet")

            emp_context.close()


            # HR Login
            while True:
                try:
                    hr_context = browser.new_context()
                    hr_page = hr_context.new_page()
                    hr.login_page(hr_page, env_config)
                    break
                except PlaywrightTimeoutError:
                    log_step(hr_page, f"timeout_hr_login")
                    wait_if_timeout(f"HR Login")
                    hr_context.close()
            
            # HR DS Approval wait
            logger.info("DS Approval action needed. Complete the DS process, then press ENTER to continue...")
            input("Press ENTER to continue...")
            
            # HR Timesheet approve
            while True:
                try:
                    hr.approve_timesheet(hr_page)
                    logger.info(f"Timesheet approved by HR completed successfully.")
                    break
                except PlaywrightTimeoutError:
                    log_step(hr_page, f"timeout_hr_approval")
                    wait_if_timeout(f"Timesheet approved")
            
            
            # HR Timesheet Downlaod
            while True:
                try:
                    hr.download_timesheet(hr_page, env_config, fmt, ts_type)
                    logger.info(f"HR Download timesheet-{fmt.upper()}-{ts_type.upper()} completed successfully.")
                    break
                except PlaywrightTimeoutError:
                    log_step(hr_page, f"timeout_hr_download_{fmt}_{ts_type}")
                    wait_if_timeout(f"HR Download Timesheet")
                    
            
            # HR Timesheet Reject
            while True:
                try:
                    hr.reject_timesheet(hr_page)
                    logger.info(f"Timesheet rejected by HR completed successfully.")
                    break
                except PlaywrightTimeoutError:
                    log_step(hr_page, f"timeout_hr_reject_{fmt}_{ts_type}")
                    wait_if_timeout(f"Timesheet rejected")
            
            hr_context.close()

            # ================= CHECKSUM =================
            # checksum.process_checksum(fmt)
            logger.info(f"Timesheet {fmt.upper()} Test completed successfully.\n")

    browser.close()