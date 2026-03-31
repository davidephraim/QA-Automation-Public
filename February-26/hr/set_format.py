import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"

with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as fc:
    cred = json.load(fc)

FORMAT_PATH = BASE_DIR  / "format.json"

with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as fc:
    cred = json.load(fc)

with open (FORMAT_PATH, 'r', encoding='utf-8') as fp:
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
    page.locator("input.search").fill("Raim'林")
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

def toggle_approval_using_space(page, enable: bool):

    switch = page.locator('input[name="approval_using_space"]')
    switch.wait_for(state="visible")

    if enable:
        switch.check()
    else:
        switch.uncheck()

    print(f"approval_using_space = {switch.is_checked()}")


# ================= TEST =================

def set_employee_format(
    playwright,
    env_config,
    company_format,
    use_without_ds=False
):

    browser = playwright.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    login_page(page, env_config)

    set_format(
        page,
        company_format
    )

    # DS ON jika NOT without_ds
    toggle_approval_using_space(
        page,
        enable=not use_without_ds
    )

    submit_stage(page)

    context.close()

    browser.close()