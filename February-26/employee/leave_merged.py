import re, json
from pathlib import Path
from playwright.sync_api import Playwright

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"

with open(CREDENTIAL_PATH) as f:
    cred = json.load(f)


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


# ================= SET MONTH =================

def find_month(page):
    target_month = "February 2026"
    prev_button = page.locator("button.react-datepicker__navigation--previous")
    cur_month = page.locator("div.react-datepicker__current-month")

    while True:
        if cur_month.inner_text() == target_month:
            break
        prev_button.click()


# ================= SET DATE =================

def select_single_day(page, selected_date):
    # BEGIN DATE
    page.get_by_role("textbox", name="dd-mm-yyyy").first.click()
    find_month(page)
    page.get_by_role("button", name=f"Choose {selected_date}").click()

    # END DATE
    page.get_by_role("textbox", name="dd-mm-yyyy").nth(1).click()
    find_month(page)
    page.get_by_role("button", name=f"Choose {selected_date}").click()


# ================= CREATE LEAVE =================

def create_leave(page, leave_type, selected_date):
    page.locator("div").filter(has_text=re.compile(r"^Leave$")).nth(2).click()
    page.get_by_role("link", name="Leave Approval").click()
    page.get_by_role("button", name="Add +").click()

    # SELECT DATE (1 DAY)
    select_single_day(page, selected_date)

    # Mapping leave_type ke option value
    leave_option_map = {
        "unpaid": "e753b646bf4511eeadf50242ac110003",
        "child_wed": "b222ae46bf2211eeadf50242ac110003",
        "sick": "c7474afe156a11ef8faa0242ac110002",
        "baptism": "7c3eb798bf2211ee9ea90242ac110003"
    }

    page.get_by_role("combobox").select_option(leave_option_map[leave_type])

    if leave_type == "baptism" or leave_type=="sick" or leave_type=="child_wed":
        page.get_by_role("button", name="Choose File").click()
        file_path = BASE_DIR / "employee" / "File_test" / "img_dummy.png"
        page.locator("input[type='file']").set_input_files(file_path)

    page.locator('textarea[name="reason"]').fill(f"{leave_type.upper} has been Created by Automation -D.")
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(1000)
    page.get_by_role("link", name="Close").click()


# ================= TEST =================

def test_create_leave(page, leave_config, env_config):
    login_page(page, env_config)
    create_leave(
        page,
        leave_config["leave_type"],
        leave_config["selected_date"]
    )