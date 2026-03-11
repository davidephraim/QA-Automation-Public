import json
from pathlib import Path
from hr.set_format import search_employee

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"
FORMAT_PATH = BASE_DIR / "hr" / "format.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)

with open (FORMAT_PATH) as fp:
    format_path = json.load(fp)

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


def test_toggle_approval_using_space(page, env_config, enable=True):
    login_page(page, env_config)

    link = cred[env_config]["link"]
    
    page.goto(link+"human-resource/employee")
    search_employee(page)

    switch = page.locator('input[name="approval_using_space"]')

    if enable:
        if not switch.is_checked():
            switch.check()
    else:
        if switch.is_checked():
            switch.uncheck()

    page.wait_for_timeout(5000)