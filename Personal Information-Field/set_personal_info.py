# ================= LIBRARY =================

import json
from pathlib import Path
from playwright.sync_api import Playwright, TimeoutError as PlaywrightTimeoutError
import logging


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


# ================= LOGS =================

def log_step(page, step_name):
    screenshot_dir = BASE_DIR / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)

    page.screenshot(path=screenshot_dir / f"{step_name}.png")

    logging.info(f"{step_name} completed successfully.")


# ================= TIMEOUT HANDLER =================

def wait_if_timeout(step_name):
    logging.warning(f"Timeout after 30s at step: {step_name}")
    input("Server is full. Make sure server is normal, then press ENTER to continue...")


# ================= LOGIN HR =================

def login_hr(page, env):
    username = cred[env]["hr"]["username"]
    password = cred[env]["hr"]["password"]
    link = cred[env]["link"]

    page.goto(link)

    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)
    page.get_by_role("button", name="Submit").click()

    try:
        page.get_by_text("OK").click(timeout=5000)
    except PlaywrightTimeoutError:
        pass

    page.locator("a:has(p:has-text('Human Resource'))").click()


# ================= LOGIN EMPLOYEE =================

def login_employee(page, env, username, password):
    link = cred[env]["link"]

    page.goto(link)

    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)

    page.get_by_role("button", name="Submit").click()

    try:
        page.get_by_text("OK", exact=True).click(timeout=5000)
    except PlaywrightTimeoutError:
        pass

    try:
        page.locator("text=Company Regulation Approval").wait_for(timeout=2000)
        company_regulation(page)
    except PlaywrightTimeoutError:
        pass

    page.locator(".wrap-role").click()
    page.get_by_text("Edit Profile").click()


# ================= COMMON =================

def confirm(page):
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="OK").click()


# ================= SET SUPPORT INFORMATION =================

def set_support_info(browser, env, name):
    hr_context = browser.new_context()
    hr_page = hr_context.new_page()

    login_hr(hr_page, env)

    hr_page.locator("input.search").fill(name)
    
    # set 1 second wait
    hr_page.wait_for_timeout(1000)
    
    if hr_page.get_by_text("There is no data to display yet.", exact=True).is_visible():
        hr_page.get_by_text("Inactive", exact=True).click()
        hr_page.locator("input.search").fill(name)
        
        hr_page.wait_for_timeout(1000)
        
        pass
    
    hr_page.locator(".icon-crud-family").nth(0).click()
    hr_page.get_by_role("link", name="Supporting Information").click()

    # set 1 second wait
    hr_page.wait_for_timeout(1000)
    set_bank_account(hr_page, name)

    # set 1 second wait
    hr_page.wait_for_timeout(1000)
    set_npwp(hr_page)
    
    hr_context.close()
    

# ================= SET BANK ACCOUNT =================

def set_bank_account(hr_page, name):
    hr_page.get_by_role("button", name="Add").click()
    hr_page.locator("input[name=\"bank_name\"]").fill(stat["string"]["text"])
    hr_page.locator("input[name=\"bank_account_number\"]").fill(stat["string"]["number"]["long"])
    hr_page.locator("input[name=\"bank_account_name\"]").fill(name)
    hr_page.get_by_role("button", name="Add +").click()

    confirm(hr_page)
    log_step(hr_page, "Set Bank Account by HR")
    
    
# ================= SET NPWP =================

def set_npwp(hr_page):  
    hr_page.get_by_text("NPWP").click()
    hr_page.get_by_role("button", name="Add").click()
    hr_page.get_by_role("textbox").fill(stat["string"]["number"]["long"])
    hr_page.get_by_role("button", name="Add +").click()
    
    confirm(hr_page)
    log_step(hr_page, "Set NPWP by HR")
    
    
# ================= GET NAME =================

def get_employee_name(browser, env, username, password):
    context = browser.new_context()
    page = context.new_page()

    login_employee(page, env, username, password)
    
    company_regulation(page)
    
    name = page.locator('input[name="full_name"]').input_value()

    log_step(page, "Get Employee Name")
    context.close()

    return name
    
    
# ================= COMPANY REGULATION =================

def company_regulation(page):
    checkboxes = page.get_by_role("checkbox")
    count = checkboxes.count()

    if count == 0 or count > 3:
        print(f"Skip company regulation - checkbox count: {count}")
        return
    
    checkboxes.click()
    page.locator("canvas").click(position={"x":357,"y":59})
    page.get_by_role("button", name="Submit Signature").click()
    page.get_by_role("button", name="Submit Approval").click()
    confirm(page)
    
    log_step(page, "E-sign—company regulation")
    
        
# ================= GENERAL PERSONAL =================

def set_general_personal(page, name):
    page.locator("input[name=\"nick_name\"]").fill(name)

    page.locator("textarea[name=\"address\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"city\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"postal_code\"]").fill(stat["string"]["number"]["short"])
    page.locator("textarea[name=\"permanentAddress\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"cityKTP\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"postalCodeKTP\"]").fill(stat["string"]["number"]["short"])
    page.locator("input[name=\"birth_place\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"birthday\"]").fill(stat["date"])
    
    page.locator("select[name=\"religion\"]").select_option("Protestan")
    page.locator("select[name=\"blood_type\"]").select_option("B")
    
    page.locator("input[name=\"nationality\"]").fill(stat["string"]["text"])

    page.locator("input[name='residence_address_status']").first.click()

    page.locator("input[name=\"ktp\"]").fill(stat["string"]["number"]["long"])
    page.locator("input[name=\"kk\"]").fill(stat["string"]["number"]["long"])
    page.locator("input[name=\"handphone\"]").fill(stat["string"]["number"]["long"])
    
    page.locator("input[name=\"email\"]").fill(stat["string"]["email"])
    
    page.get_by_role("button", name="Choose File").set_input_files(stat["file"]["img"])

    page.get_by_role("button", name="Save").click()
    confirm(page)
    
    log_step(page, "General—Personal")


# ================= GENERAL FAMILY =================

def set_general_family(page):
    page.get_by_text("Family").click()
    page.get_by_role("button", name="Add +").click()

    page.locator("input[name=\"fullname\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"id_number\"]").fill(stat["string"]["number"]["long"])
    page.locator("select[name=\"gender\"]").select_option("Male")
    page.locator("input[name=\"place_of_birth\"]").fill(stat["string"]["text"])

    page.locator("input[name=\"date_of_birth\"]").fill("2026-03-13")
    page.locator("select[name=\"religion\"]").select_option("d04b9a58b03411ee89aa5124d28652dc")
    page.locator("select[name=\"education\"]").select_option("Tidak / Belum Sekolah")
    page.locator("#combo-box-demo").click()
    page.get_by_role("option", name="Gubernur", exact=True).click()
    page.locator("select[name=\"blood_type\"]").select_option("A+")
    page.locator("select[name=\"marital_status\"]").select_option("Belum Kawin")
    page.locator("select[name=\"relationship_status\"]").select_option("d04b9ab4b03411ee89aa5124d28652dc")
    page.locator("select[name=\"nationnality\"]").select_option("WNI")
    
    page.locator("input[name=\"setEmergency\"]").click()
    page.locator("input[name=\"emergency_contact_telephone\"]").fill(stat["string"]["number"]["long"])
    page.locator("input[name=\"emergency_contact_address\"]").fill(stat["string"]["text"])

    page.get_by_role("button", name="Create").click()
    confirm(page)

    log_step(page, "General—Family")


# ================= EDUCATION FORMAL & INFORMAL =================

def set_education_formal_informal(page):
    page.get_by_text("Education").nth(0).click()
    page.get_by_role("button", name="Add +").click()

    page.locator("select[name=\"level\"]").select_option("SD")
    page.locator("input[name=\"institution\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"location\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"subject\"]").fill(stat["string"]["text"])
    
    page.locator('input[name="year"]').nth(0).fill("2026")
    page.locator('input[name="year"]').nth(1).fill("2026")
    
    page.locator('input[id="1"]').click()

    page.get_by_role("button", name="Create").click()
    confirm(page)
    
    log_step(page, "Education—Formal & Informal")


# ================= EDUCATION COURSE TRAINING =================

def set_education_course_training(page):
    page.get_by_text("Course Training").click()
    page.get_by_role("button", name="Add +").click()
    
    page.locator("input[name=\"subject\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"institution\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"location\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"duration\"]").fill(stat["string"]["number"]["short"])
    
    page.get_by_role("button", name="Create").click()
    confirm(page)
    
    log_step(page, "Education—Course")


# ================= FOREIGN LANGUAGE =================

def set_foreign_language(page):
    page.get_by_text("Foreign Language").click()
    page.get_by_role("button", name="Add +").click()
    
    page.locator("input[name=\"language_skill\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"active_speaker\"]").click()
    
    page.get_by_role("button", name="Add +").click()
    confirm(page)
    
    log_step(page, "Foreign Language")


# ================= ACTIVITY =================

def set_activity(page):
    page.get_by_text("Activity", exact=True).click()
    page.get_by_role("button", name="Edit").click()
    
    page.locator("textarea[name=\"hobbies_and_leisure_time\"]").fill(stat["string"]["text"])
    page.locator("textarea[name=\"reading_subject\"]").fill(stat["string"]["text"])
    
    page.get_by_role("button", name="Save Changes").click()
    confirm(page)
    
    log_step(page, "Activity")


# ================= WORKING EXPERIENCE =================

def set_working_experience(page):
    page.get_by_text("Working Experience").click()
    page.get_by_role("button", name="Add +").click()

    page.locator("input[name=\"company_name\"]").fill(stat["string"]["text"])
    page.locator("textarea[name=\"address\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"company_phone\"]").fill(stat["string"]["number"]["long"])
    page.locator("input[name=\"starting_job_position\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"last_job_position\"]").fill(stat["string"]["text"])
    
    page.locator("input[name=\"start_date\"]").fill("2026-03-13")
    page.locator("input[name=\"end_date\"]").fill("2026-03-13")
    
    page.locator("textarea[name=\"leaving_reason\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"direct_manager_name\"]").fill(stat["string"]["text"])
    page.locator("label:has-text('Last Salary') + input").fill(stat["string"]["number"]["short"])
    
    page.get_by_role("button", name="Add +").click()
    confirm(page)
    
    log_step(page, "Working Experience")


# ================= ADDITIONAL QUESTIONNAIR =================

def set_additional_questionnair(page):
    page.get_by_text("Additional").click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Edit").click()
    
    page.wait_for_timeout(500)
    page.get_by_role("textbox").nth(0).fill("1")
    page.wait_for_timeout(500)
    page.get_by_role("textbox").nth(1).fill("2")
    
    page.get_by_role("button", name="Save Changes").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="Close").click()
    
    log_step(page, "Additional—Questionnair")


# ================= ADDITIONAL ATTACHMENT =================

def set_attachment(page):
    page.get_by_text("Attachment").click()
    
    page.get_by_role("button", name="Choose File").first.set_input_files(stat["file"]["pdf"])
    page.get_by_role("button", name="Choose File").nth(1).set_input_files(stat["file"]["pdf"])
    page.get_by_role("button", name="Choose File").nth(2).set_input_files(stat["file"]["pdf"])
    page.get_by_role("button", name="Choose File").nth(3).set_input_files(stat["file"]["pdf"])
    page.get_by_role("button", name="Choose File").nth(4).set_input_files(stat["file"]["pdf"])
    page.get_by_role("button", name="Choose File").nth(5).set_input_files(stat["file"]["pdf"])
    
    page.locator("div:nth-child(7) > .container-upload-employee > input").set_input_files(stat["file"]["pdf"])
    
    page.get_by_role("button", name="Save").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="Close").click()
    
    log_step(page, "Additional—Attachment")


# ================= ADDITIONAL PTKP STATUS =================

def set_ptkp_status(page):
    page.get_by_text("PTKP Status").click()
    page.get_by_role("button", name="Add").click()
    
    page.get_by_role("combobox").nth(1).select_option("Daughter")
    page.locator("input[name=\"name\"]").fill(stat["string"]["text"])
    page.locator("select[name=\"gender\"]").select_option("Male")
    page.locator("input[name=\"date_of_birth\"]").fill(stat["date"])
    
    page.get_by_role("button", name="Create").click()
    page.get_by_role("button", name="Confirm").click()
    
    try:
        page.get_by_role("link", name="OK").click(timeout=3000)
    except PlaywrightTimeoutError:
        pass

    try:
        page.get_by_text("Confirm").click(timeout=3000)
    except PlaywrightTimeoutError:
        pass
    
    log_step(page, "Additional—PTKP")
    
    
# ================= MERGE =================

def employee_merge(browser, env, username, password):

    # ================= STEP 1: GET NAME FROM EMPLOYEE =================
    while True:
        try:
            name = get_employee_name(browser, env, username, password)

            logging.info(f"Employee name detected: {name}")
            break
        except PlaywrightTimeoutError:
            wait_if_timeout("get_employee_name")
    
    
    # ================= STEP 2: HR SET SUPPORT INFO =================
    while True:
        try:
            set_support_info(browser, env, name)
            break
        except PlaywrightTimeoutError:
            wait_if_timeout("set_support_info")

    while True:
        try:
            # ================= STEP 3: EMPLOYEE COMPLETE PROFILE =================
            employee_context = browser.new_context()
            employee_page = employee_context.new_page()

            login_employee(employee_page, env, username, password)

            set_general_personal(employee_page, name)
            set_general_family(employee_page)
            set_education_formal_informal(employee_page)
            set_education_course_training(employee_page)
            set_foreign_language(employee_page)
            set_activity(employee_page)
            set_working_experience(employee_page)
            set_additional_questionnair(employee_page)
            set_attachment(employee_page)
            set_ptkp_status(employee_page)
        
            employee_context.close()
            break
        except PlaywrightTimeoutError:
            wait_if_timeout("Employee data completion process")


# ================= TEST =================

def test_set_profile(playwright: Playwright, env, username, password):
    browser = playwright.chromium.launch(
        headless=True,

        args=[
            "--disable-dev-shm-usage",
            "--no-sandbox"
        ]
    )

    employee_merge(browser, env, username, password)

    browser.close()