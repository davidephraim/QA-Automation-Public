# ================= LIBRARY =================

import os
import json
import logging
import hashlib
from pathlib import Path
from playwright.sync_api import Playwright

# import module internal
from hr.set_format import set_employee_format
from employee.employee_timesheet_download import download_timesheet
from hr.hr_timesheet_merged import timesheet_employee


# ================= PATH SETUP =================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"
STATIC_PATH = PROJECT_ROOT / "static_data.json"

with open(CREDENTIAL_PATH, 'r', encoding='utf-8') as fc:
    cred = json.load(fc)

with open(STATIC_PATH, 'r', encoding='utf-8') as fp:
    stat = json.load(fp)


# convert relative file path -> absolute

stat["file"]["pdf_1"] = str(
    PROJECT_ROOT / stat["file"]["pdf_1"]
)

# ================= LOGGING =================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def log_step(step):
    logger.info(f"STEP: {step}")


# ================= LOGIN =================

def login_page(page, env):

    log_step("login_employee")

    username = cred[env]["employee"]["username"]
    password = cred[env]["employee"]["password"]

    page.goto(cred[env]["link"])

    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)

    page.get_by_role("button", name="Submit").click()
    page.locator("a:has(p:has-text('Employee'))").click()


# ================= TIMESHEET CREATE =================

def create_timesheet(page, timesheet_type, fmt):

    log_step(f"create_timesheet | {fmt} | {timesheet_type}")

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

    page.get_by_role("textbox", name="Select Date").nth(1).click()
    page.get_by_role("button", name=f"Choose {start_date}").click()

    page.locator("input[name='end_date']").click()
    page.get_by_role("button", name=f"Choose {end_date}").click()

    comment = "Timesheet created by automation."

    if fmt in ["bri", "cimb"]:
        page.locator("input[name='custom_fields[0].value']").fill(
            f"{fmt.upper()} {comment}"
        )

    elif fmt == "mandiri":
        page.locator("input[name='custom_fields[0].value']").fill(
            f"{fmt.upper()}-1 {comment}"
        )
        page.locator("input[name='custom_fields[1].value']").fill(
            f"{fmt.upper()}-2 {comment}"
        )

    elif fmt == "hypernet":

        for i in range(4):
            page.locator(
                f"input[name='custom_fields[{i}].value']"
            ).fill(
                f"{fmt.upper()}-{i+1} {comment}"
            )

    page.get_by_role("button", name="Create").click()
    page.get_by_role("link", name="Close").click()


# ================= WITHOUT DS =================

def without_ds(page):

    log_step("without_digital_signature")

    page.reload()

    page.locator("tbody tr").first.click()

    page.locator(".icon-crud-family").nth(0).click()

    page.get_by_text("Send Approval").click()

    page.locator("input[type='file']").set_input_files(
        stat["file"]["pdf_1"]
    )

    page.get_by_role("button", name="Send").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="Close").click()


# ================= CHECKSUM =================

def sha256_checksum(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:

        while chunk := f.read(8192):

            sha256.update(chunk)

    return sha256.hexdigest()


def get_latest_file(folder):

    files = list(folder.glob("*"))

    if not files:
        return None

    return max(files, key=os.path.getctime)


def write_checksum_report(file_path, checksum, status):

    report_file = BASE_DIR / "checksum_report.txt"

    with open(report_file, "a") as f:

        f.write(
            f"{file_path.name} | {checksum} | {status}\n"
        )


def process_checksum(company_format):

    log_step(f"checksum_process | {company_format}")

    download_folder = (BASE_DIR / "Downloaded_timesheet" / company_format.upper())

    download_folder.mkdir(parents=True, exist_ok=True)

    latest_file = get_latest_file(download_folder)

    if not latest_file:
        logger.warning("no downloaded file found")

        return

    downloaded_checksum = sha256_checksum(latest_file)

    static_checksum = sha256_checksum(stat["file"]["pdf_1"])

    status = (
        "MATCH"
        if downloaded_checksum == static_checksum
        else "DIFFERENT"
    )

    write_checksum_report(latest_file, downloaded_checksum, status)

    logger.info(f"{latest_file.name} | {status}")


# ================= FLOW =================

def create_employee_timesheet(
    playwright,
    env_config,
    company_format,
    timesheet_config,
    use_without_ds=False
):

    log_step(
        f"FLOW | {company_format} | {timesheet_config} | DS={not use_without_ds}"
    )

    browser = playwright.chromium.launch(
        headless=False,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    context = browser.new_context()
    page = context.new_page()

    login_page(page, env_config)

    create_timesheet(
        page,
        timesheet_config,
        company_format
    )

    # ================= WITHOUT DS =================

    if use_without_ds:

        without_ds(page)

    page.reload()

    # download tetap pakai company_format
    download_timesheet(
        playwright,
        env_config,
        company_format,
        timesheet_config
    )

    timesheet_employee(
        playwright,
        env_config,
        company_format,
        timesheet_config
    )

    process_checksum(company_format)

    context.close()
    browser.close()

# ================= CONFIG =================

TIMESHEET_TYPES = [
    "full",
    "halfh",
    "halft",
    "last"
]

FORMATS = [
    "sigmatech",
    "bri",
    "cimb",
    "mandiri",
    "hypernet"
]


# ================= TEST =================

def test_timesheet_merged(playwright, env_config):

    log_step("START TEST")

    # ================= NORMAL FLOW (DS ON) =================

    # for company_format in FORMATS:
        # set_employee_format(playwright, env_config, company_format, use_without_ds=False)

    #     for timesheet_type in TIMESHEET_TYPES:
    #         create_employee_timesheet(playwright, env_config, company_format, timesheet_type, use_without_ds=False)

    # ================= WITHOUT DS =================

    for company_format in FORMATS:
        set_employee_format(playwright, env_config, company_format, use_without_ds=True)

        for timesheet_type in TIMESHEET_TYPES:
            create_employee_timesheet(playwright, env_config, company_format, timesheet_type, use_without_ds=True)

    log_step("END TEST")