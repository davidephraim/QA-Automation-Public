# ================= LIBRARY =================

import hashlib
from pathlib import Path


# ================= HASH FUNCTION =================

def generate_hash(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# ================= COMPARE FUNCTION =================

def compare_files(static_file: Path, downloaded_file: Path):
    static_hash = generate_hash(static_file)
    downloaded_hash = generate_hash(downloaded_file)

    if static_hash == downloaded_hash:
        return True
    else:
        return False