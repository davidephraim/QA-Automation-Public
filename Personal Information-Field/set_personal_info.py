# ================= LIBRARY =================

import json
from pathlib import Path
from playwright.sync_api import Playwright, TimeoutError


# ================= STATIC DIRECTORIES =================

BASE_DIR = Path(__file__).resolve().parent
CREDENTIAL_PATH = BASE_DIR / "credentials.json"
STATIC_PATH = BASE_DIR / "static_data.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)

with open (STATIC_PATH) as fp:
    stat = json.load(fp)


# ================= LOGIN HR =================

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


# ================= LOGIN EMPLOYEE =================

def login_employee(page, env, username, password, name):
    link = cred[env]["link"]
    page.goto(link)

    page.locator('input[name="email"]').fill(username)
    page.locator('input[name="password"]').fill(password)
    page.get_by_role("button", name="Submit").click()
    
    if page.get_by_text("OK").is_visible(timeout=3000):
        page.get_by_text("OK").click()
    
    page.locator(".wrap-role").click()
    page.get_by_text("Edit Profile").click()


# ================= CONFIRM =================

def confirm(page):
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="OK").click()


# ================= SET NPWP =================

def set_npwp (playwright: Playwright, env, name):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login_hr(page, env)
    
    page.locator("input.search").fill(name)
    page.locator(".icon-crud-family").nth(0).click()
    page.get_by_role("link", name="Supporting Information").click()
    page.get_by_text("NPWP").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_role("textbox").fill(stat["string"]["number"]["long"])
    page.get_by_role("button", name="Add +").click()

    confirm(page)

    context.close()
    browser.close()


# ================= GENERAL PERSONAL =================

def set_general_personal(page, name):
    page.locator("input[name=\"full_name\"]").fill(name)
    page.locator("input[name=\"nick_name\"]").fill(name)

    page.locator("textarea[name=\"address\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"city\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"postal_code\"]").fill(stat["string"]["number"]["short"])
    page.locator("textarea[name=\"permanentAddress\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"cityKTP\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"postalCodeKTP\"]").fill(stat["string"]["number"]["short"])
    page.locator("input[name=\"birth_place\"]").fill(stat["string"]["text"])
    
    page.locator("select[name=\"religion\"]").select_option("Protestan")
    page.locator("select[name=\"blood_type\"]").select_option("B")
    
    page.locator("input[name=\"nationality\"]").fill(stat["string"]["text"])

    page.locator("input[name=\"ktp\"]").fill(stat["string"]["number"]["long"])
    page.locator("input[name=\"kk\"]").fill(stat["string"]["number"]["long"])
    page.locator("input[name=\"handphone\"]").fill(stat["string"]["number"]["long"])
    
    page.locator("input[name=\"email\"]").fill(stat["string"]["email"])
    
    page.locator("input[type='file']").nth(0).set_input_files(stat["file"]["img"])

    page.get_by_role("button", name="Save").click()
    confirm(page)


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


# ================= FOREIGN LANGUAGE =================

def set_foreign_language(page):
    page.get_by_text("Foreign Language").click()
    page.get_by_role("button", name="Add +").click()
    
    page.locator("input[name=\"language_skill\"]").fill(stat["string"]["text"])
    page.locator("input[name=\"active_speaker\"]").click()
    
    page.get_by_role("button", name="Add +").click()
    confirm(page)


# ================= ACTIVITY =================

def set_activity(page):
    page.get_by_text("Activity", exact=True).click()
    page.get_by_role("button", name="Edit").click()
    
    page.locator("textarea[name=\"hobbies_and_leisure_time\"]").fill(stat["string"]["text"])
    page.locator("textarea[name=\"reading_subject\"]").fill(stat["string"]["text"])
    
    page.get_by_role("button", name="Save Changes").click()
    confirm(page)


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


# ================= ADDITIONAL QUESTIONNAIR =================

def set_additional_questionnair(page):
    page.get_by_text("Additional").click()
    page.get_by_role("button", name="Edit").click()
    
    page.get_by_role("textbox").nth(0).fill(stat["string"]["text"])
    page.get_by_role("textbox").nth(1).fill(stat["string"]["text"])
    
    page.get_by_role("button", name="Save Changes").click()
    page.get_by_role("button", name="Confirm").click()
    page.get_by_role("link", name="Close").click()


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


# ================= ADDITIONAL PTKP STATUS =================

def set_ptkp_status(page):
    page.get_by_text("PTKP Status").click()
    page.get_by_role("button", name="Add").click()
    
    page.get_by_role("combobox").nth(1).select_option("Daughter")
    page.locator("input[name=\"name\"]").fill(stat["string"]["text"])
    page.locator("select[name=\"gender\"]").select_option("Male")
    page.locator("input[name=\"date_of_birth\"]").fill("2026-03-13")
    
    page.get_by_role("button", name="Create").click()
    page.get_by_role("button", name="Confirm").click()
    
    try:
        page.get_by_role("link", name="OK").click(timeout=3000)
    except TimeoutError:
        pass

    try:
        page.get_by_text("Confirm").click(timeout=3000)
    except TimeoutError:
        pass


# ================= MERGE =================

def employee_merge(page, env, username, password, name):
    login_employee(page, env, username, password, name)
    set_general_personal(page, name)
    set_general_family(page)
    set_education_formal_informal(page)
    set_education_course_training(page)
    set_foreign_language(page)
    set_activity(page)
    set_working_experience(page)
    set_additional_questionnair(page)
    set_attachment(page)
    set_ptkp_status(page)


# ================= TEST =================

def test_set_profile(playwright: Playwright, page, env, username, password, name):
    set_npwp(playwright, env, name)

    employee_merge(page, env, username, password, name)