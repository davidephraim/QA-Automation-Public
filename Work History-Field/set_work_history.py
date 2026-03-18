# ================= LIBRARY =================

import json
from pathlib import Path
import logging


# ================= STATIC DIRECTORIES =================

BASE_DIR = Path(__file__).resolve().parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"
DATA_PATH = BASE_DIR / "stat_employee.json"
FORMAT_PATH = BASE_DIR / "timesheet_format.json"

with open(CREDENTIAL_PATH, 'r', encoding="utf-8") as f:
    cred = json.load(f)

with open(DATA_PATH) as f:
    stat = json.load(f)

with open(FORMAT_PATH) as f:
    formats = json.load(f)


# ================= LOGGING =================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_step(step):
    logging.info(f"{step} completed successfully.")


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

    log_step("Login HR")


# ================= SEARCH EMPLOYEE =================

def search_employee(page, name):
    page.locator("input.search").fill(name)
    page.locator(".icon-crud-family").nth(0).click()
    page.get_by_role("link", name="Work Information").click()
    
    page.wait_for_timeout(1000)
    
    icons = page.locator(".icon-crud-family")

    if icons.count() > 0:
        icons.first.click()
        page.get_by_role("link", name="Detail").click()
    else:
        page.get_by_role("button", name="Add").click()

    log_step("Search employee")


# ================= HELPER: NATIVE SELECT =================

def select_native(page, selector, value):
    page.evaluate(
        """({selector, value}) => {
            const select = document.querySelector(selector);
            if (select) {
                select.value = value;
                select.dispatchEvent(new Event('input', { bubbles: true }));
                select.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""",
        {"selector": selector, "value": value}
    )
    page.wait_for_timeout(300)


# ================= HELPER: REACT SELECT =================

def select_react(page, index, value):
    dropdown = page.locator("div.select__control").nth(index)

    dropdown.click()

    input_box = dropdown.locator("input")
    input_box.fill(value)

    menu = page.locator("div.select__menu")

    option = menu.locator("div.select__option", has_text=value)
    option.wait_for()
    option.first.click()

    page.wait_for_timeout(500)


# ================= SET TIMESHEET FORMAT =================

def set_timesheet_format(page, fmt):
    format_id = None

    for item in formats:
        if fmt in item:
            format_id = item["id"]
            break

    if format_id is None:
        raise ValueError(f"Format '{fmt}' not found")

    select_native(page, 'select[name="timesheet_client_format_id"]', format_id)

    log_step("Set timesheet format")


# ================= TOGGLE =================

def toggle_approval_using_space(page, enable=True):
    toggle = page.locator('input[name="approval_using_space"]')

    if enable and not toggle.is_checked():
        toggle.check()
    elif not enable and toggle.is_checked():
        toggle.uncheck()

    log_step("Toggle approval using space")


# ================= SET DEPARTMENT =================

def set_department(page, dept_key):
    dept_value = stat["dept"][dept_key]

    select_native(page, 'select[name="department"]', dept_value)

    log_step("Set department")


# ================= SET JOB POSITION =================

def set_job_position(page, dept_key):
    job_value = stat["dept"][f"{dept_key}_title"]

    # asumsi dropdown kedua
    select_react(page, 0, job_value)

    log_step("Set job position")


# ================= SET BIZDEV MANAGER =================

def set_bizdev_manager(page):
    select_native(
        page,
        'select[name="bizdev_manager_employee_id"]',
        "3d6f7bf6752811eca2070242ac130002"
    )

    log_step("Set bizdev manager")


# ================= STAGE 1 =================

def stage_field_1(page, fmt, name, ds, dept):
    
    page.locator('input[name="start_effective_date"]').fill(stat["effective"]["start"])
    page.locator('input[name="end_effective_date"]').fill(stat["effective"]["end"])
    page.locator('input[name="name"]').fill(name)
    
    # timesheet format
    set_timesheet_format(page, fmt)
    
    # with/without ds approval (sigmatech system)
    toggle_approval_using_space(page, ds)

    # gender (native)
    select_native(page, 'select[name="gender"]', "Male")

    # department (react)
    set_department(page, dept)

    # job position (react)
    set_job_position(page, dept)

    # bizdev manager
    set_bizdev_manager(page)

    log_step("Stage 1 completed")


# ================= STAGE 2 =================

def stage_field_2(page, env):
    page.locator('input[name="direct_supervisor.name"]').fill(cred[env]["ds"]["name"])
    page.locator('input[name="direct_supervisor.email"]').fill(cred[env]["ds"]["email"])
    page.locator('input[name="direct_supervisor.position"]').fill(cred[env]["ds"]["position"])

    log_step("Stage 2 completed")


# ================= UPDATE =================

def update(page):
    page.get_by_role("button", name="Update").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="OK").click()

    log_step("Update data")


# ================= SAVE =================

def save(page):
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Confirm").click()
    
    return "Try to slowdown the process execution on code or use `--slowmo=1000`."
    
# ================= MAIN FUNCTION =================

def test_employee_format(page, env, fmt, name, ds, dept):
    login_hr(page, env)
    search_employee(page, name)

    stage_field_1(page, fmt, name, ds, dept)
    stage_field_2(page, env)

    update_btn = page.get_by_role("button", name="Update")

    if update_btn.is_visible():
        update(page)
    else:
        print(save(page))