import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"

with open(CREDENTIAL_PATH) as f:
    cred = json.load(f)


# ================= LOGIN =================

def login_page(page, env):

    username = cred[env]["admin"]["username"]
    password = cred[env]["admin"]["password"]
    link = cred[env]["link"]

    page.goto(link)
    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)

    page.get_by_role("button", name="Submit").click()
    page.locator("a:has(p:has-text('Human Resource'))").click()


# ================= APPROVE TIMESHEET =================

def approve_timesheet(page):
    page.get_by_role("link", name="Timesheet").click()
    page.locator("tr:first-child td:nth-child(4) a").click()
    
    page.get_by_role("button", name="Approval").click()

    checkbox = page.get_by_placeholder("1").first
    checkbox.scroll_into_view_if_needed()
    checkbox.check()

    page.get_by_role("button", name="Send").click()
    submit_stage(page)


# ================= REJECT TIMESHEET =================

def reject_timesheet(page):
    page.get_by_role("link", name="Timesheet").click()
    page.locator("tr:first-child td:nth-child(4) a").click()

    page.get_by_role("button", name="Approval").click()

    reject_checkbox = page.get_by_placeholder("1").nth(1)
    reject_checkbox.scroll_into_view_if_needed()
    reject_checkbox.check()

    comment_box = page.locator("textarea[name=\"comment\"]")
    comment_box.scroll_into_view_if_needed()
    comment_box.fill("Rejected by Automation -D.")

    page.get_by_role("button", name="Send").click()
    submit_stage(page)


# ================= SUBMISSION =================

def submit_stage(page):
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="OK").click()


# ================= TEST =================

def test_timesheet_action(page, env_config, action_config):

    login_page(page, env_config)

    action_config(page)