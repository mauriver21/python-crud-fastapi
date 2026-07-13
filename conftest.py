import os

import pytest
from tests.utils import initialize_test_user

os.environ["NODE_ENV"] = "test"


@pytest.fixture(scope="session", autouse=True)
def setup_tests():
    initialize_test_user(
        "controller-test@example.com",
        "test-password",
    )
