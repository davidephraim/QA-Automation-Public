# ================= LIBRARY =================

import pytest


# ================= CLI OPTIONS =================

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run test: dev or stg"
    )

    parser.addoption(
        "--username",
        action="store",
        default=None,
        help="Employee username (email)"
    )

    parser.addoption(
        "--password",
        action="store",
        default=None,
        help="Employee password"
    )


# ================= FIXTURES =================

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def username(request):
    return request.config.getoption("--username")


@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("--password")
