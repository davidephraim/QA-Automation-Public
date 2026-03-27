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

    parser.addoption(
        "--name",
        action="store",
        default=None,
        help="Employee name to search"
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


@pytest.fixture(scope="session")
def name(request):
    return request.config.getoption("--name")