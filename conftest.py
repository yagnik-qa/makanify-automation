import os

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    return {
        **browser_type_launch_args,
        "headless": headless,
        "args": [
            "--disable-notifications",
            "--disable-popup-blocking",
            "--start-maximized",
            "--window-size=1920,1080",
        ],
    }
