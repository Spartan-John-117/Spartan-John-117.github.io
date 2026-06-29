from pathlib import Path
from typing import Any

import pytest

TEST_DIR = Path(__file__).parent


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--turingtoy-force-regen",
        action="store_true",
        default=False,
        help="Force regen regression data files",
    )


@pytest.fixture()
def global_datadir() -> Path:
    return TEST_DIR / "data"
