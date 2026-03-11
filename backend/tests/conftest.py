import os

import pytest

from app.core.paths import load_env


def pytest_configure(config):
    load_env()
    os.environ["RUNNING_TESTS"] = "True"
    config.addinivalue_line("markers", "llm: mark test as requiring the --llm option to run")


def pytest_addoption(parser):
    # Adding a custom command-line option
    parser.addoption("--llm", action="store_true", default=False, help="Run tests marked with 'llm'")


def pytest_collection_modifyitems(config, items):
    # Skip tests marked with 'llm' if --llm option is not provided
    if not config.getoption("--llm"):
        skip_llm = pytest.mark.skip(reason="need --llm option to run")
        for item in items:
            if "llm" in item.keywords:
                item.add_marker(skip_llm)
