import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"

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


# ================= APPROVE TIMESHEET =================

def approve_timesheet(page):
    page.get_by_role("link", name="Timesheet").click()

    page.reload(wait_until="load")
    
    page.locator("tr:first-child td:nth-child(4) a").click()
    page.get_by_role("button", name="Approval").click()

    checkbox = page.get_by_placeholder("1").nth(0)
    checkbox.scroll_into_view_if_needed()
    checkbox.check()

    page.get_by_role("button", name="Send").click()
    submit_stage(page)


# ================= REJECT TIMESHEET =================

def reject_timesheet(page):
    # page.get_by_role("link", name="Timesheet").click()
    
    # page.locator("tr:first-child td:nth-child(4) a").click()
    page.get_by_role("button", name="Approval").click()

    reject_checkbox = page.get_by_placeholder("1").nth(1)
    reject_checkbox.scroll_into_view_if_needed()
    reject_checkbox.check()

    comment_box = page.locator("textarea[name='comment']")
    comment_box.fill("Timesheet has been Rejected by Automation -D.")

    page.get_by_role("button", name="Send").click()
    submit_stage(page)


# ================= SUBMISSION =================

def submit_stage(page):
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="OK").click()


# ================= DOWNLOAD TIMESHEET =================

def download_timesheet(page, company_format, timesheet_config, env):
    page.locator(".icon-crud-family").nth(2).click()

    if company_format == "sigmatech":
        with page.expect_download() as download_info:
            page.get_by_text("Download Sigmatech's Format").click()
    else:
        with page.expect_download() as download_info:
            page.get_by_text("Download Client's Format").click()

    download = download_info.value

    path = f"{BASE_DIR}/hr/Downloaded_timesheet/{company_format.upper()}/" + f"{env.upper()} - HR - {company_format} - {timesheet_config} - {download.suggested_filename}"
    download.save_as(path)


# ================= TEST =================

# def test_timesheet_action(page, env_config, action_config, company_format):
#     login_page(page, env_config)
#     action_config(page)
#     download_timesheet(page, company_format)


# ================= CONT. =================

def timesheet_employee(playwright, env_config, company_format, timesheet_config):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # LOGIN
    login_page(page, env_config)
    
    # DS approval waiting
    page.wait_for_timeout(10000)

    approve_timesheet(page)
    download_timesheet(page, company_format, timesheet_config, env_config)
    reject_timesheet(page)

    context.close()
    browser.close()