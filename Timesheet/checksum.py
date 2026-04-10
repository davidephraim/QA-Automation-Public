# ================= LIBRARY =================

import os
import json
from pathlib import Path
import logging
import hashlib


# ================= STATIC DIRECTORIES =================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

CREDENTIAL_PATH = PROJECT_ROOT / "credentials.json"
STATIC_PATH = PROJECT_ROOT / "static_data.json"

with open(CREDENTIAL_PATH) as fc:
    cred = json.load(fc)

with open(STATIC_PATH) as fp:
    stat = json.load(fp)
    

# ================= LOGGING =================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

def log_step(step):
    logger.info(f"STEP: {step}")
    
        
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


def write_checksum_report(file_path, checksum_value, status):

    report_file = BASE_DIR / "checksum_report.txt"

    with open(report_file, "a") as f:

        f.write(f"{file_path.name} | {checksum_value} | {status}\n")


def process_checksum(company_format):

    # log_step(f"checksum_process | {company_format}")

    download_folder = (BASE_DIR / "Downloaded_timesheet" / company_format.upper())

    download_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    latest_file = get_latest_file(download_folder)

    if not latest_file:

        # logger.warning("no downloaded file found")

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