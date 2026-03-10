import json
from pathlib import Path

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


# ================= DOWNLOAD LATEST TIMESHEET =================

def download_timesheet(playwright, env_config):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # LOGIN
    login_page(page, env_config)

    # DOWNLOAD TIMESHEET
    page.get_by_role("link", name="Timesheet").click()
    page.locator("tbody tr").first.locator("td").first.click()
    page.locator(".icon-crud-family").first.click()

    with page.expect_download() as download_info:
        page.get_by_text("Download Client's Format").click()

    download = download_info.value

    path = "Downloaded_timesheet/" + download.suggested_filename
    download.save_as(path)

    print("Downloaded file:", download.suggested_filename)
    print("Saved to:", path)
    
    context.close()
    browser.close()