import json
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LEAVE_PATH = BASE_DIR / "leave_date.json"


def pytest_addoption(parser):

    # ================= LEAVE =================
    parser.addoption(
        "--leave",
        action="store",
        default="unpaid",
        help="Leave type: unpaid, child_wed, sick, baptism"
    )

    parser.addoption(
        "--date-type",
        action="store",
        default="begin",
        help="begin or end"
    )

    # ================= TIMESHEET =================
    parser.addoption(
        "--timesheet",
        action="store",
        default="full",
        help="Timesheet type: full, halfh, halft, last"
    )

    # ================= URL =================
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment: dev or stg"
    )

    # ================= FORMAT =================
    parser.addoption(
        "--format",
        action="store",
        default="sigmatech",
        help="Format: sigmatech, bri, cimb, mandiri, hypernet"
    )

# ================= LEAVE FIXTURE =================

@pytest.fixture
def leave_config(request):

    leave_type = request.config.getoption("--leave")
    date_type = request.config.getoption("--date-type")

    with open(LEAVE_PATH) as fh:
        leave_data = json.load(fh)

    if leave_type not in leave_data:
        raise ValueError(f"Leave type '{leave_type}' not found in JSON")

    if date_type not in ["begin", "end"]:
        raise ValueError("--date-type must be begin or end")

    selected_date = leave_data[leave_type][date_type]

    return {
        "leave_type": leave_type,
        "selected_date": selected_date
    }


# ================= TIMESHEET FIXTURE =================

@pytest.fixture
def timesheet_config(request):

    timesheet_type = request.config.getoption("--timesheet")

    allowed = ["full", "halfh", "halft", "last"]

    if timesheet_type not in allowed:
        raise ValueError(f"--timesheet must be one of {allowed}")

    return timesheet_type

# ================= URL FIXTURE =================

@pytest.fixture
def env_config(request):

    env = request.config.getoption("--env")

    allowed = ["dev", "stg"]

    if env not in allowed:
        raise ValueError(f"--env must be one of {allowed}")

    return env

# ================= FORMAT FIXTURE =================

@pytest.fixture
def company_format(request):

    fmt = request.config.getoption("--format")

    allowed = ["sigmatech", "bri", "cimb", "mandiri", "hypernet"]

    if fmt not in allowed:
        raise ValueError(f"--format must be one of {allowed}")

    return fmt