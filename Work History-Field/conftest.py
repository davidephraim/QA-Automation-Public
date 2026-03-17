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
        "--name",
        action="store",
        default=None,
        help="Employee name to search"
    )

    parser.addoption(
        "--format",
        action="store",
        default="sigmatech",
        help="Format: sigmatech, bri, cimb, mandiri, hypernet"
    )

    parser.addoption(
        "--ds",
        action="store",
        default="yes",
        help="DS approval: yes or no"
    )

    parser.addoption(
        "--dept",
        action="store",
        default="bd",
        help="Department: bd or rec"
    )


# ================= FIXTURES =================

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def name(request):
    return request.config.getoption("--name")


@pytest.fixture(scope="session")
def username(request):
    return request.config.getoption("--format")


@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("--ds")


@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("--dept")
