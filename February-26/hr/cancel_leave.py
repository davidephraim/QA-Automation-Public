import re, json
from pathlib import Path
from playwright.sync_api import Playwright

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
    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)

    page.get_by_role("button", name="Submit").click()
    page.locator("a:has(p:has-text('Human Resource'))").click()


# ================= REJECT =================

def reject_leave(page, leave_config):

    target_leave = leave_config["target_leave"]

    page.locator("div").filter(has_text=re.compile(r"^Leave$")).first.click()
    page.get_by_role("link", name="Leave Approval").click()

    # search employee
    page.locator("input.search").fill("alaba")

    page.wait_for_timeout(2000)

    rows = page.locator("table tbody tr")
    count = rows.count()

    for i in range(count):
        row = rows.nth(i)

        leave_cell = row.locator("td").nth(3)
        leave_text = leave_cell.inner_text().strip()

        if target_leave.lower() in leave_text.lower():

            cancel_btn = row.get_by_text("Cancel")

            if cancel_btn.count() > 0:

                cancel_btn.click()

                page.get_by_role("textbox").fill(f"{target_leave.upper} has been Canceled by Automation -D.")
                page.get_by_role("button", name="Save").click()

                break


# ================= SUBMISSION =================

def submit_stage(page):
    page.locator("button:has-text('Confirm')").click()
    page.get_by_role("link", name="OK").click()


# ================= TEST =================

def test_cancel_leave(page, leave_config, env_config):
    login_page(page, env_config)
    reject_leave(page, leave_config)
    submit_stage(page)