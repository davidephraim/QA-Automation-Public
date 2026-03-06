import json
from pathlib import Path
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
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper} timesheet has been Created by Automation -D.")
    page.get_by_role("button", name="Create").click()
    page.get_by_role("link", name="Close").click()


# ================= TEST =================

def test_create_timesheet(playwright: Playwright, timesheet_config, env_config, company_format):

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    login_page(page, env_config)
    create_timesheet(page, timesheet_config, company_format)

    context.close()
    browser.close()