# ================= LIBRARY =================

import json
from pathlib import Path
import logging


# ================= STATIC DIRECTORIES =================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"
STATIC_PATH = PROJECT_ROOT / "static_data.json"

with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as fc:
    cred = json.load(fc)

with open(STATIC_PATH, 'r', encoding='utf-8') as fp:
    stat = json.load(fp)


# ================= LOGS =================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_step(page, step_name):
    screenshot_dir = BASE_DIR / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)

    page.screenshot(path=screenshot_dir / f"{step_name}.png")

    logging.info(f"{step_name} completed successfully.")    
    
    
# ================= HELP =================

def helper_dashboard(page):
    page.get_by_role("link", name="Dashboard").click()
    
    
# ================= CONFIRM =================

def confirm(page):
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="OK").click()
    
    
# ================= LOGIN =================

def login_page(page, env, username, password):
    link = cred[env]["link"]

    page.goto(link)

    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)

    page.get_by_role("button", name="Submit").click()
    
    page.locator("a:has(p:has-text('Employee'))").click()
    

# ================= CREATE TIMESHEET =================

def create_timesheet(page, timesheet_type, fmt):

    while True:
        helper_dashboard(page)
        page.get_by_role("link", name="Timesheet").click()
        page.get_by_role("button", name="Add +").click()

        page.get_by_role("textbox", name="Select Date").first.click()
        page.get_by_role("button", name="Choose February").click()

        timesheet_map = {
            "full": ("Sunday, February 1st,", "Saturday, February 28th,"),
            "halfh": ("Sunday, February 1st,", "Saturday, February 14th,"),
            "halft": ("Sunday, February 15th,", "Saturday, February 28th,"),
            "last": ("Wednesday, February 25th,", "Saturday, February 28th,"),
        }

        start_date, end_date = timesheet_map[timesheet_type]

        # START DATE
        page.get_by_role("textbox", name="Select Date").nth(1).click()
        page.get_by_role("button", name=f"Choose {start_date}").click()

        # END DATE
        page.locator("input[name='end_date']").click()
        page.get_by_role("button", name=f"Choose {end_date}").click()

        # INPUT FIELD
        if fmt in ["bri", "cimb"]:
            page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper()} {stat['string']['text']}")
        elif fmt == "mandiri":
            page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper()} 1 {stat['string']['text']}")
            page.locator("input[name=\"custom_fields[1].value\"]").fill(f"{fmt.upper()} 2 {stat['string']['text']}")
        elif fmt == "hypernet":
            for i in range(4):
                page.locator(f"input[name=\"custom_fields[{i}].value\"]").fill(f"{fmt.upper()} {i+1} {stat['string']['text']}")
        elif fmt == "mufg":
            page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper()} {stat['string']['text']}")

        # CLICK CREATE
        page.get_by_role("button", name="Create").click()

        # CHECKING
        invalid_popup = page.get_by_text("Invalid!")

        try:
            invalid_popup.wait_for(timeout=3000)
            log_step(page, "Timesheet Existed. Reject timesheet using HR to retry")

            input("Press ENTER to continue...")

            page.get_by_role("link", name="Close").click()
            continue
        except:
            page.get_by_role("link", name="Close").click()
            break
        

# ================= DOWNLOAD LATEST TIMESHEET =================

def download_timesheet(page, env, fmt, timesheet_config):

    # DOWNLOAD TIMESHEET
    helper_dashboard(page)
    page.get_by_role("link", name="Timesheet").click()
    page.locator("tbody tr").nth(0).locator("td").nth(0).click()
    page.locator(".icon-crud-family").nth(0).click()

    if fmt == "sigmatech":
        with page.expect_download() as download_info:
            page.get_by_text("Download Sigmatech's Format").click()
    else:
        with page.expect_download() as download_info:
            page.get_by_text("Download Client's Format").click()

    download = download_info.value

    path = f"{BASE_DIR}/Downloaded_timesheet/employee/{fmt.upper()}/" + f"{env.upper()} - Employee - {fmt.upper()} - {timesheet_config} - {download.suggested_filename}"
    download.save_as(path)
    
    
# ================= GET NAME =================

def get_employee_name(browser, env, username, password):
    link = cred[env]["link"]
    context = browser.new_context()
    page = context.new_page()

    login_page(page, env, username, password)
    
    # name = page.locator(".wrap-role-main").inner_text()
    page.goto(link+"employee/profile")
    name = page.locator('input[name="full_name"]').input_value()

    log_step(page, "Get Employee Name")
    context.close()

    return name


# ================= WITHOUT DS =================

def without_ds(page, file_path):
    page.locator("tbody tr").nth(0).locator("td").nth(0).click()
    page.locator(".icon-crud-family").nth(0).click()

    page.get_by_text("Send Approval").click()
    page.get_by_role("button", name="Choose File").click()
    page.locator("input[type='file']").set_input_files(file_path)

    page.get_by_role("button", name="Send").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="Close").click()