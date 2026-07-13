import os
import sys
from pathlib import Path

os.environ["NODE_ENV"] = "test"
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import pytest

from tests.utils import initialize_test_user


@pytest.fixture(scope="session", autouse=True)
def setup_tests():
    initialize_test_user()
