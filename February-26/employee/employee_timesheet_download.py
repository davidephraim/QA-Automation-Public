import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"

with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as fc:
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


# ================= DOWNLOAD LATEST TIMESHEET =================

def download_timesheet(playwright, env_config, company_format, timesheet_config):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # LOGIN
    login_page(page, env_config)

    # DOWNLOAD TIMESHEET
    page.get_by_role("link", name="Timesheet").click()
    page.locator("tbody tr").nth(0).locator("td").nth(0).click()
    page.locator(".icon-crud-family").nth(0).click()

    if company_format == "sigmatech":
        with page.expect_download() as download_info:
            page.get_by_text("Download Sigmatech's Format").click()
    else:
        with page.expect_download() as download_info:
            page.get_by_text("Download Client's Format").click()

    download = download_info.value

    path = f"{BASE_DIR}/employee/Downloaded_timesheet/{company_format.upper()}/" + f"{env_config.upper()} - Employee - {company_format} - {timesheet_config} - {download.suggested_filename}"
    download.save_as(path)
    
    context.close()
    browser.close()