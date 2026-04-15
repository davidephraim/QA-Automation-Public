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
    
    
# ================= CHECKSUM =================

def run_checksum(fmt, ts_type):
    download_dir = BASE_DIR / "Downloaded_timesheet" / "hr" / fmt.upper()

    latest_file = get_latest_file(download_dir)

    static_pdf = Path(stat["file"]["pdf_1"])

    result = checksum.compare_files(static_pdf, latest_file)

    if result:
        logger.info(f"CHECKSUM RESULT: PASS ({fmt}-{ts_type})")
    else:
        logger.error(f"CHECKSUM RESULT: FAILED ({fmt}-{ts_type})")
        
        
# ================= GET LATEST FILE =================

def get_latest_file(download_dir: Path):
    files = list(download_dir.glob("*.pdf"))
    if not files:
        raise FileNotFoundError(f"No PDF found in {download_dir}")

    return max(files, key=lambda f: f.stat().st_mtime)


# ================= GET LATEST FILE =================

def rename_latest_file(download_dir: Path, mode: str):
    latest_file = get_latest_file(download_dir)

    original_name = latest_file.stem

    if mode == "ds_on":
        new_name = f"{original_name}.pdf"
    else:
        new_name = f"{original_name}_ds_off.pdf"

    new_path = download_dir / new_name

    counter = 1
    while new_path.exists():
        new_name = new_name.replace(".pdf", f"_{counter}.pdf")
        new_path = download_dir / new_name
        counter += 1

    latest_file.rename(new_path)

    logger.info(f"Renamed file to: {new_name}")

    return new_path

    
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

            logger.info(f"========== START FORMAT: {fmt.upper()} ==========")

        # ================= SET FORMAT + DS ON =================
        while True:
            try:
                hr_context = browser.new_context()
                hr_page = hr_context.new_page()
                hr.login_page(hr_page, env_config)

                hr.work_information(hr_page, employee_name)
                hr.set_format(hr_page, format_id)

                hr.toggle_approval_using_space(hr_page, True)  # DS ON
                logger.info("DS ON")

                hr.submit_update(hr_page)
                hr_context.close()
                break

            except PlaywrightTimeoutError:
                log_step(hr_page, f"timeout_hr_setup_{fmt}")
                wait_if_timeout("HR Setup DS ON")
                hr_context.close()

        # ================= LOOP TIMESHEET (DS ON) =================
        for ts_type in timesheet_types:
            logger.info(f"[DS ON] {fmt.upper()} | {ts_type.upper()}")

            # ===== EMPLOYEE CREATE =====
            while True:
                try:
                    emp_context = browser.new_context()
                    emp_page = emp_context.new_page()
                    employee.login_page(emp_page, env_config, username, password)

                    employee.create_timesheet(emp_page, ts_type, fmt)
                    emp_context.close()
                    break

                except PlaywrightTimeoutError:
                    log_step(emp_page, f"timeout_create_{fmt}_{ts_type}")
                    wait_if_timeout("Create Timesheet")
                    emp_context.close()

            # ===== EMPLOYEE DOWNLOAD =====
            while True:
                try:
                    emp_context = browser.new_context()
                    emp_page = emp_context.new_page()
                    employee.login_page(emp_page, env_config, username, password)

                    employee.download_timesheet(emp_page, env_config, fmt, ts_type)
                    emp_context.close()
                    break

                except PlaywrightTimeoutError:
                    log_step(emp_page, f"timeout_download_{fmt}_{ts_type}")
                    wait_if_timeout("Download Timesheet")
                    emp_context.close()

            # ===== HR TIMESHEET APPROVAL & DOWNLOAD =====
            while True:
                try:
                    hr_context = browser.new_context()
                    hr_page = hr_context.new_page()
                    hr.login_page(hr_page, env_config)

                    input("Complete DS approval, then press ENTER...")

                    hr.approve_timesheet(hr_page)
                    hr.download_timesheet(hr_page, env_config, fmt, ts_type, True)

                    download_dir = BASE_DIR / "Downloaded_timesheet" / "hr" / fmt.upper()
                    rename_latest_file(download_dir, "ds_on")

                    hr_context.close()
                    break

                except PlaywrightTimeoutError:
                    log_step(hr_page, f"timeout_hr_{fmt}_{ts_type}")
                    wait_if_timeout("HR Approve & Download")
                    hr_context.close()
                    
            # ===== HR TIMESHEET REJECT =====
            while True:
                try:
                    hr_context = browser.new_context()
                    hr_page = hr_context.new_page()
                    hr.login_page(hr_page, env_config)
            
                    hr.reject_timesheet(hr_page)
                    hr_context.close()
                    break
                except PlaywrightTimeoutError:
                    log_step(hr_page, f"timeout_hr_{fmt}_{ts_type}")
                    wait_if_timeout("HR Reject")
                    

        # ================= SET DS OFF =================
        while True:
            try:
                hr_context = browser.new_context()
                hr_page = hr_context.new_page()
                hr.login_page(hr_page, env_config)

                hr.work_information(hr_page, employee_name)

                hr.toggle_approval_using_space(hr_page, False)  # DS OFF
                logger.info("DS OFF")

                hr.submit_update(hr_page)
                hr_context.close()
                break

            except PlaywrightTimeoutError:
                log_step(hr_page, f"timeout_ds_off_{fmt}")
                wait_if_timeout("DS OFF Setup")
                hr_context.close()

        # ================= LOOP TIMESHEET (DS OFF + CHECKSUM) =================
        for ts_type in timesheet_types:
            logger.info(f"[DS OFF] {fmt.upper()} | {ts_type.upper()}")

            # bersihin folder sebelum download
            download_dir = BASE_DIR / "Downloaded_timesheet" / "hr" / fmt.upper()

            # ===== EMPLOYEE CREATE =====
            while True:
                try:
                    emp_context = browser.new_context()
                    emp_page = emp_context.new_page()
                    employee.login_page(emp_page, env_config, username, password)

                    employee.create_timesheet(emp_page, ts_type, fmt)
                    emp_context.close()
                    break

                except PlaywrightTimeoutError:
                    log_step(emp_page, f"timeout_create_off_{fmt}_{ts_type}")
                    wait_if_timeout("Create Timesheet")
                    emp_context.close()

            # ===== EMPLOYEE SEND WITHOUT DS =====
            while True:
                try:
                    emp_context = browser.new_context()
                    emp_page = emp_context.new_page()
                    employee.login_page(emp_page, env_config, username, password)

                    employee.without_ds(emp_page, stat["file"]["pdf_1"])
                    emp_context.close()
                    break

                except PlaywrightTimeoutError:
                    log_step(emp_page, f"timeout_without_ds_{fmt}_{ts_type}")
                    wait_if_timeout("Without DS")
                    emp_context.close()

            # ===== HR APPROVE + DOWNLOAD =====
            while True:
                try:
                    hr_context = browser.new_context()
                    hr_page = hr_context.new_page()
                    hr.login_page(hr_page, env_config)

                    hr.approve_timesheet(hr_page)
                    hr.download_timesheet(hr_page, env_config, fmt, ts_type, False)

                    download_dir = BASE_DIR / "Downloaded_timesheet" / "hr" / fmt.upper()
                    rename_latest_file(download_dir, "ds_off")

                    # CHECKSUM
                    run_checksum(fmt, ts_type)

                    hr.reject_timesheet(hr_page)

                    hr_context.close()
                    break

                except PlaywrightTimeoutError:
                    log_step(hr_page, f"timeout_hr_off_{fmt}_{ts_type}")
                    wait_if_timeout("HR Process DS OFF")
                    hr_context.close()

        logger.info(f"========== END FORMAT: {fmt.upper()} ==========\n")

    browser.close()