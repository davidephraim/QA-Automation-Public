import os
import json
from pathlib import Path
from hr.set_format import set_employee_format
from employee.employee_timesheet_download import download_timesheet
from hr.hr_timesheet_merged import timesheet_employee
from playwright.sync_api import Playwright

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)

file_sampel_pdf = BASE_DIR / "employee" / "File_test" / "file_sample_150kB.pdf"


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


# ================= TIMESHEET =================

def create_timesheet(page, timesheet_type, fmt):

    page.get_by_role("link", name="Timesheet").click()
    page.get_by_role("button", name="Add +").click()

    page.get_by_role("textbox", name="Select Date").first.click()
    page.get_by_role("button", name="Choose February").click()

    timesheet_map = {
        "full": ("Sunday, February 1st,", "Saturday, February 28th,"),
        "halfh": ("Sunday, February 1st,", "Saturday, February 14th,"),
        "halft": ("Sunday, February 15th,", "Saturday, February 28th,"),
        "last": ("Wednesday, February 25th,", "Saturday, February 28th,"),
    }

    start_date, end_date = timesheet_map[timesheet_type]

    # START DATE
    page.get_by_role("textbox", name="Select Date").nth(1).click()
    page.get_by_role("button", name=f"Choose {start_date}").click()

    # END DATE
    page.locator("input[name='end_date']").click()
    page.get_by_role("button", name=f"Choose {end_date}").click()

    # Comment
    comment = "timesheet has been Created by Automation -D."

    # SUBMIT
    if fmt == "bri" or fmt == "cimb":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper()} {comment}")
    elif fmt == "mandiri":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper()}-1 {comment}")
        page.locator("input[name=\"custom_fields[1].value\"]").fill(f"{fmt.upper()}-2 {comment}")
    elif fmt == "hypernet":
        page.locator("input[name=\"custom_fields[0].value\"]").fill(f"{fmt.upper()}-1 {comment}")
        page.locator("input[name=\"custom_fields[1].value\"]").fill(f"{fmt.upper()}-2 {comment}")
        page.locator("input[name=\"custom_fields[2].value\"]").fill(f"{fmt.upper()}-3 {comment}")
        page.locator("input[name=\"custom_fields[3].value\"]").fill(f"{fmt.upper()}-4 {comment}")

    page.get_by_role("button", name="Create").click()
    page.get_by_role("link", name="Close").click()


# ================= TEST =================

def open_admin_wait(playwright, env_config):

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    username = cred[env_config]["admin"]["username"]
    password = cred[env_config]["admin"]["password"]
    link = cred[env_config]["link"]

    page.goto(link)

    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)

    page.get_by_role("button", name="Submit").click()

    page.wait_for_timeout(15000)

    context.close()
    browser.close()


def without_ds(page):
    page.wait_for_timeout(2000)
    page.reload(wait_until="load")

    page.locator("tbody tr").nth(0).locator("td").nth(0).click()
    page.locator(".icon-crud-family").nth(0).click()

    page.get_by_text("Send Approval").click()
    page.get_by_role("button", name="Choose File").click()
    page.locator("input[type='file']").set_input_files(file_sampel_pdf)

    page.get_by_role("button", name="Send").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="Close").click()


# ================= AUTO =================

def create_employee_timesheet(playwright: Playwright, env_config, company_format, timesheet_config, use_without_ds=False):

    browser = playwright.chromium.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()

    page.set_default_timeout(0)
    page.set_default_navigation_timeout(0)
    
    login_page(page, env_config)

    create_timesheet(page, timesheet_config, company_format)

    if use_without_ds:
        without_ds(page)

        download_timesheet(playwright, env_config, "", timesheet_config)

    else:
        download_timesheet(playwright, env_config, company_format, timesheet_config)

    timesheet_employee(playwright, env_config, company_format, timesheet_config)
    process_checksum(company_format)

    context.close()
    browser.close()


# ================= CHECKSUM =================

def sha256_checksum(file_path, chunk_size=8192):
    import hashlib

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()


# ================= REPORT CHECKSUM =================

def write_checksum_report(file_path, checksum, status):

    report_path = BASE_DIR / "checksum_report.txt"

    with open(report_path, "a", encoding="utf-8") as f:
        f.write(f"{file_path.name} | {checksum} | {status}\n")


# ================= GET FILE =================

def get_latest_file(folder_path):

    files = list(folder_path.glob("*"))

    if not files:
        return None

    latest_file = max(files, key=os.path.getctime)

    return latest_file


# ================= CHECKSUM PROCESS =================

def process_checksum(company_format):

    download_folder = BASE_DIR / "hr" / "Downloaded_timesheet" / company_format.upper()

    latest_file = get_latest_file(download_folder)

    if not latest_file:
        return

    downloaded_checksum = sha256_checksum(latest_file)

    # checksum dari static file
    static_checksum = sha256_checksum(file_sampel_pdf)

    if downloaded_checksum == static_checksum:
        status = "MATCH"
    else:
        status = "DIFFERENT"

    write_checksum_report(latest_file, downloaded_checksum, status)

    print(f"{latest_file.name} | {downloaded_checksum} | {status}")
    

TIMESHEET_TYPES = ["full", "halfh", "halft", "last"]

FORMATS = [
    "sigmatech",
    "bri",
    "cimb",
    "mandiri",
    "hypernet"
]


# ================= EXECUTION =================

def test_timesheet_merged(playwright, env_config):

    # ======================
    # CYCLE 1 (NORMAL)
    # ======================

    for company_format in FORMATS:

        set_employee_format(playwright, env_config, company_format)

        for timesheet_type in TIMESHEET_TYPES:

            create_employee_timesheet(
                playwright,
                env_config,
                company_format,
                timesheet_type,
                use_without_ds=False
            )

    # # admin wait
    # open_admin_wait(playwright, env_config)


    # ======================
    # CYCLE 2 (WITHOUT DS)
    # ======================

    # for company_format in FORMATS:

    #     set_employee_format(playwright, env_config, company_format)

    #     for timesheet_type in TIMESHEET_TYPES:

    #         create_employee_timesheet(
    #             playwright,
    #             env_config,
    #             company_format,
    #             timesheet_type,
    #             use_without_ds=True
    #         )

