import re, json
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)


# ================= LOGIN =================

def login_page(page, env):

    username = cred[env]["admin"]["username"]
    password = cred[env]["admin"]["password"]
    link = cred[env]["link"]

    page.goto(link)

    page.locator("input[name=\"email\"]").fill(username)
    page.locator("input[name=\"password\"]").fill(password)

    page.get_by_role("button", name="Submit").click()
    page.locator("a:has(p:has-text('Human Resource'))").click()


# ================= SET HOLIDAY =================

def search_set_holiday(page, holiday_config):
    target_name = holiday_config["target_name"]
    selected_date = holiday_config["selected_date"]

    page.locator("div").filter(has_text=re.compile(r"^Master$")).first.click()
    page.get_by_role("link", name="Holiday and Event").click()
    row = page.locator("table tbody tr", has_text=target_name)
    row.locator("td").nth(6).locator(".icon-crud-family").click()
    page.get_by_role("link", name="Edit").click()

    start_input = page.locator('input[name="start_date"]')
    end_input = page.locator('input[name="end_date"]')

    # Remove browser constraint
    start_input.evaluate("el => el.removeAttribute('max')")
    end_input.evaluate("el => el.removeAttribute('min')")

    # Set one-day holiday
    start_input.fill(selected_date)
    start_input.dispatch_event("change")

    end_input.fill(selected_date)
    end_input.dispatch_event("change")
    

# ================= SUBMISSION =================

def submit_stage(page):
    # Submission
    page.get_by_role("button", name="Edit").click()
    page.get_by_role("link", name="Close").click()


# ================= TEST =================

def test_edit_holiday(playwright: Playwright, holiday_config, env_config):
    
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    login_page(page, env_config)
    search_set_holiday(page, holiday_config)
    submit_stage(page)
