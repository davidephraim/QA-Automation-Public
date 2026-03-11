import json
from pathlib import Path
from hr.set_format import set_employee_format
from employee.employee_timesheet_download import download_timesheet
from hr.hr_timesheet_merged import timesheet_employee
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
        "last": ("Wednesday, February 25th,", "Saturday, February 28th,"),
    }

    start_date, end_date = timesheet_map[timesheet_type]

    # START DATE
    page.get_by_role("textbox", name="Select Date").nth(1).click()
    page.get_by_role("button", name=f"Choose {start_date}").click()

    # END DATE
    page.locator("input[name='end_date']").click()
    page.get_by_role("button", name=f"Choose {end_date}").click()

    # Comment
    comment = "timesheet has been Created by Automation -D."

    # SUBMIT
    if fmt == "bri" or fmt == "cimb":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper()} {comment}")
    elif fmt == "mandiri":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper(), 1} {comment}")
        page.locator("input[name=\"custom_fields[1].value\"]").fill(f"{fmt.upper(), 2} {comment}")
    elif fmt == "hypernet":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper(), 1} {comment}")
        page.locator("input[name=\"custom_fields[1].value\"]").fill(f"{fmt.upper(), 2} {comment}")
        page.locator("input[name=\"custom_fields[2].value\"]").fill(f"{fmt.upper(), 3} {comment}")
        page.locator("input[name=\"custom_fields[3].value\"]").fill(f"{fmt.upper(), 4} {comment}")

    page.get_by_role("button", name="Create").click()
    page.get_by_role("link", name="Close").click()


# ================= TEST =================

# def test_create_timesheet(playwright: Playwright, page, timesheet_config, env_config, company_format):
#     # Set employee timesheet format from HR module
#     set_employee_format(playwright, env_config, company_format)

#     # Create timesheet employee
#     login_page(page, env_config)
#     create_timesheet(page, timesheet_config, company_format)

#     # Download timesheet employee
#     download_timesheet(playwright, env_config, company_format, timesheet_config)

#     # Approve-Reject timesheet from HR module
#     timesheet_employee(playwright, env_config, company_format, timesheet_config)


# ================= AUTO =================

def create_employee_timesheet(playwright: Playwright, env_config, company_format, timesheet_config):

    browser = playwright.chromium.launch(headless=False)

    # context baru → reset session
    context = browser.new_context()
    page = context.new_page()

    # login
    login_page(page, env_config)

    # create timesheet
    create_timesheet(page, timesheet_config, company_format)

    # download
    download_timesheet(playwright, env_config, company_format, timesheet_config)

    # HR action
    timesheet_employee(playwright, env_config, company_format, timesheet_config)

    context.close()
    browser.close()


TIMESHEET_TYPES = ["full", "halfh", "halft", "last"]

FORMATS = [
    "sigmatech",
    "bri",
    "cimb",
    "mandiri"
]


def test_timesheet_merged(playwright, env_config):

    for company_format in FORMATS:

        set_employee_format(playwright, env_config, company_format)

        for timesheet_type in TIMESHEET_TYPES:

            create_employee_timesheet(
                playwright,
                env_config,
                company_format,
                timesheet_type
            )