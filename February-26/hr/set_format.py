import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)

FORMAT_PATH = BASE_DIR  / "format.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)

with open (FORMAT_PATH) as fp:
    format_path = json.load(fp)

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


# ================= SEARCH EMPLOYEE =================

def search_employee(page):
    page.locator("input.search").fill("alaba")
    page.wait_for_timeout(500)

    page.locator(".icon-crud-family").click()

    page.get_by_role("link", name="Work Information").click()
    page.locator(".icon-crud-family").first.click()
    page.get_by_role("link", name="Detail").click()

    page.wait_for_timeout(2000)


# ================= SET FORMAT =================

def set_format(page, fmt):
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

    print(f"Format set to: {format_name} | ID: {format_id}")


# ================= SUBMISSION =================

def submit_stage(page):
    page.get_by_role("button", name="Update").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="OK").click()


# ================= DS TOGGLE =================

def toggle_approval_using_space(page, env, enable=True):
    link = cred[env]["link"]
    
    page.goto(link+"/human-resource/employee")
    search_employee(page)

    switch = page.locator('input[name="approval_using_space"]')

    if enable:
        if not switch.is_checked():
            switch.click()
    else:
        if switch.is_checked():
            switch.click()


# ================= TEST =================

def set_employee_format(playwright, env_config, company_format):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login_page(page, env_config)
    set_format(page, company_format)
    submit_stage(page)

    context.close()
    browser.close()