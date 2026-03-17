# ================= LIBRARY =================

import json
from pathlib import Path


# ================= STATIC DIRECTORIES =================

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"
FORMAT_PATH = BASE_DIR / "hr" / "format.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)

with open (FORMAT_PATH) as fp:
    format_path = json.load(fp)


# ================= LOGIN =================

def login_hr(page, env):
    username = cred[env]["hr"]["username"]
    password = cred[env]["hr"]["password"]
    link = cred[env]["link"]
    page.goto(link)

    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)
    page.get_by_role("button", name="Submit").click()

    if page.get_by_text("OK").is_visible(timeout=3000):
        page.get_by_text("OK").click()

    page.locator("a:has(p:has-text('Human Resource'))").click()
    
    return "Login HR has been successfully created."


# ================= SEARCH EMPLOYEE =================

def search_employee(page, name):
    page.locator("input.search").fill(name)
    page.locator(".icon-crud-family").nth(0).click()
    page.get_by_role("link", name="Work Information").click()
    
    icons = page.locator(".icon-crud-family")

    if icons.count() > 0:
        icons.first.click()
        page.get_by_role("link", name="Detail").click()

    else:
        page.get_by_role("button", name="Add").click()
    
    return "Search and check employee has been succesfully executed."


# ================= SET TIMESHEET FORMAT =================

def set_timesheet_format(page, fmt):
    format_id = None
    format_name = None

    for item in format_path:
        if fmt in item:
            format_name = item[fmt]
            format_id = item["id"]
            break

    if format_id is None:
        raise ValueError(f"Format '{fmt}' not found in format.json")

    search_employee(page)

    page.evaluate("""
        (id) => {
        const select = document.querySelector('select[name="timesheet_client_format_id"]');
        select.value = id;
        select.dispatchEvent(new Event('input', { bubbles: true }));
        select.dispatchEvent(new Event('change', { bubbles: true }));
        }
        """, format_id)

    page.wait_for_timeout(500)

    return f"Timesheet format has been successfully set.\nFormat set to: {format_name} | ID: {format_id}"


# ================= DS TOGGLE =================

def toggle_approval_using_space(page, env, enable=True):
    link = cred[env]["link"]
    
    page.goto(link+"/human-resource/employee")
    search_employee(page)

    switch = page.locator('input[name="approval_using_space"]')

    if enable:
        if not switch.is_checked():
            switch.check()
    else:
        if switch.is_checked():
            switch.uncheck()
    
    return "Toggle approval has been successfully set."


# ================= SUBMISSION =================

def submit_stage(page):
    page.get_by_role("button", name="Update").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="OK").click()

    return "Done."


# ================= MERGE =================

def set_work_history_merge(page, name):
    a=a
# ================= TEST =================

def set_employee_format(page, env_config, company_format, name):
    login_hr(page, env_config)

    set_work_history_merge(page, name, company_format)
    
    submit_stage(page)
