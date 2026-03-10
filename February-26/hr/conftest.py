import json
import pytest
from pathlib import Path
from hr.hr_timesheet_merged import approve_timesheet, reject_timesheet

BASE_DIR = Path(__file__).resolve().parent
HOLIDAY_PATH = BASE_DIR / "holiday_date.json"
LEAVE_PATH = BASE_DIR / "leave_date.json"

def pytest_addoption(parser):

    # ================= HOLIDAY =================
    parser.addoption(
        "--holiday",
        action="store",
        default="public",
        help="Holiday type"
    )

    parser.addoption(
        "--date-type",
        action="store",
        default="begin",
        help="begin or end"
    )

    # ================= TIMESHEET =================
    parser.addoption(
        "--action",
        action="store",
        default="approve",
        help="Timesheet action: approve or reject"
    )

    # ================= LEAVE =================
    parser.addoption(
        "--leave",
        action="store",
        default="sick",
        help="Leave type to reject"
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

    with open(LEAVE_PATH) as fh:
        holiday_data = json.load(fh)

    target_leave = holiday_data[leave_type]["name"]

    return {
        "leave_type": leave_type,
        "target_leave": target_leave
    }


# ================= HOLIDAY FIXTURE =================

@pytest.fixture
def holiday_config(request):
    holiday_type = request.config.getoption("--holiday")
    date_type = request.config.getoption("--date-type")

    with open(HOLIDAY_PATH) as fh:
        holiday_data = json.load(fh)

    target_name = holiday_data[holiday_type]["name"]
    selected_date = holiday_data[holiday_type][date_type]

    return {
        "holiday_type": holiday_type,
        "target_name": target_name,
        "selected_date": selected_date
    }


# ================= URL FIXTURE =================

@pytest.fixture
def env_config(request):

    env = request.config.getoption("--env")

    allowed = ["dev", "stg"]

    if env not in allowed:
        raise ValueError(f"--env must be one of {allowed}")

    return env


# ================= TIMESHEET ACTION FIXTURE =================

@pytest.fixture
def action_config(request):

    action = request.config.getoption("--action")

    actions = {
        "approve": approve_timesheet,
        "reject": reject_timesheet,
    }

    if action not in actions:
        raise ValueError("--action must be approve or reject")

    return actions[action]


# ================= FORMAT FIXTURE =================

@pytest.fixture
def company_format(request):

    fmt = request.config.getoption("--format")

    allowed = ["sigmatech", "bri", "cimb", "mandiri", "hypernet"]

    if fmt not in allowed:
        raise ValueError(f"--format must be one of {allowed}")

    return fmt