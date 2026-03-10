import json
from pathlib import Path
from hr.set_format import set_employee_format
from employee.employee_timesheet_download import download_timesheet
from playwright.sync_api import Playwright

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)


# ================= LOGIN =================

def login_page(page, env):

    username = cred[env]["employee"]["username"]
    password = cred[env]["employee"]["password"]
    link = cred[env]["link"]

    page.goto(link)

    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)

    page.get_by_role("button", name="Submit").click()
    page.locator("a:has(p:has-text('Employee'))").click()


# ================= TIMESHEET =================

def create_timesheet(page, timesheet_type, fmt):

    page.get_by_role("link", name="Timesheet").click()
    page.get_by_role("button", name="Add +").click()

    page.get_by_role("textbox", name="Select Date").first.click()
    page.get_by_role("button", name="Choose February").click()

    timesheet_map = {
        "full": ("Sunday, February 1st,", "Saturday, February 28th,"),
        "halfh": ("Sunday, February 1st,", "Saturday, February 14th,"),
        "halft": ("Sunday, February 15th,", "Saturday, February 28th,"),
        "last": ("Sunday, February 25th,", "Saturday, February 28th,"),
    }

    start_date, end_date = timesheet_map[timesheet_type]

    # START DATE
    page.get_by_role("textbox", name="Select Date").nth(1).click()
    page.get_by_role("button", name=f"Choose {start_date}").click()

    # END DATE
    page.locator("input[name='end_date']").click()
    page.get_by_role("button", name=f"Choose {end_date}").click()

    # SUBMIT
    if fmt == "bri" or fmt == "cimb":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper()} timesheet has been Created by Automation -D.")
    elif fmt == "mandiri":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper(), 1} timesheet has been Created by Automation -D.")
        page.locator("input[name=\"custom_fields[1].value\"]").fill(f"{fmt.upper(), 2} timesheet has been Created by Automation -D.")
    elif fmt == "hypernet":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper(), 1} timesheet has been Created by Automation -D.")
        page.locator("input[name=\"custom_fields[1].value\"]").fill(f"{fmt.upper(), 2} timesheet has been Created by Automation -D.")
        page.locator("input[name=\"custom_fields[2].value\"]").fill(f"{fmt.upper(), 3} timesheet has been Created by Automation -D.")
        page.locator("input[name=\"custom_fields[3].value\"]").fill(f"{fmt.upper(), 4} timesheet has been Created by Automation -D.")

    page.get_by_role("button", name="Create").click()
    page.get_by_role("link", name="Close").click()


# ================= TEST =================

def test_create_timesheet(playwright: Playwright, page, timesheet_config, env_config, company_format):
    # Set employee timesheet format
    set_employee_format(playwright, env_config, company_format)

    # Create timesheet
    login_page(page, env_config)
    create_timesheet(page, timesheet_config, company_format)

    # Download timesheet
    download_timesheet(playwright, env_config)

    