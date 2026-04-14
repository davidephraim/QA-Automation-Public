# ================= LIBRARY =================
import hashlib
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


# ================= HASH FUNCTION =================
def generate_hash(file_path: Path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# ================= COMPARE FUNCTION =================
def compare_files(static_file: Path, downloaded_file: Path):
    static_hash = generate_hash(static_file)
    downloaded_hash = generate_hash(downloaded_file)

    logger.info(f"Static Hash     : {static_hash}")
    logger.info(f"Downloaded Hash : {downloaded_hash}")

    if static_hash == downloaded_hash:
        logger.info("CHECKSUM PASSED")
        return True
    else:
        logger.error("CHECKSUM FAILED")
        return False