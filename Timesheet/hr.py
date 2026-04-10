# ================= LIBRARY =================

import json
from pathlib import Path


# ================= STATIC DIRECTORIES =================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"
STATIC_PATH = PROJECT_ROOT / "static_data.json"

with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as fc:
    cred = json.load(fc)

with open(STATIC_PATH, 'r', encoding='utf-8') as fp:
    stat = json.load(fp)

# convert relative file path -> absolute
stat["file"]["img"] = str(
    PROJECT_ROOT / stat["file"]["img_1"]
)

stat["file"]["pdf"] = str(
    PROJECT_ROOT / stat["file"]["pdf_1"]
)


# ================= LOGIN =================

def login_page(page, env):
    username = cred[env]["hr"]["username"]
    password = cred[env]["hr"]["password"]
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

def download_timesheet(page, env, fmt, timesheet_config):
    page.locator(".icon-crud-family").nth(2).click()

    if fmt == "sigmatech":
        with page.expect_download() as download_info:
            page.get_by_text("Download Sigmatech's Format").click()
    else:
        with page.expect_download() as download_info:
            page.get_by_text("Download Client's Format").click()

    download = download_info.value

    path = f"{BASE_DIR}/Downloaded_timesheet/hr/{fmt.upper()}/" + f"{env.upper()} - HR - {fmt} - {timesheet_config} - {download.suggested_filename}"
    download.save_as(path)


# ================= EMPLOYEE WORK INFORMATION =================

def work_information(page, name):
    page.locator("input.search").fill(name)
    page.wait_for_timeout(500)

    page.locator(".icon-crud-family").click()

    page.get_by_role("link", name="Work Information").click()
    page.locator(".icon-crud-family").first.click()
    page.get_by_role("link", name="Detail").click()

    page.wait_for_timeout(2000)


# ================= SET FORMAT =================

def set_format(page, format_id):
    page.evaluate("""
        (id) => {
        const select = document.querySelector('select[name="timesheet_client_format_id"]');
        select.value = id;
        select.dispatchEvent(new Event('input', { bubbles: true }));
        select.dispatchEvent(new Event('change', { bubbles: true }));
        }
        """, format_id)

    page.wait_for_timeout(500)


# ================= SUBMISSION =================

def submit_update(page):
    page.get_by_role("button", name="Update").click()
    submit_stage(page)


# ================= DS TOGGLE =================

def toggle_approval_using_space(page, enable: bool):

    switch = page.locator('input[name="approval_using_space"]')
    switch.wait_for(state="visible")

    if enable:
        switch.check()
    else:
        switch.uncheck()