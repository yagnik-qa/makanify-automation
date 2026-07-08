import os

BASE_URL = os.getenv("MAKANIFY_BASE_URL") or "https://uat-makanify.workzy.co"
LOGIN_URL = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
LEADS_URL = f"{BASE_URL}/leads"
PROPERTIES_URL = f"{BASE_URL}/individual-properties"

DEFAULT_EMAIL = os.getenv("MAKANIFY_EMAIL") or "sales@moweb.com"
DEFAULT_PASSWORD = os.getenv("MAKANIFY_PASSWORD") or "Test@321"

DEFAULT_TIMEOUT_MS = 20_000
DROPDOWN_TIMEOUT_MS = 5_000

STORED_PROJECT_FILE = os.path.join(os.path.dirname(__file__), "stored_project.txt")


def store_project_name(name: str) -> None:
    with open(STORED_PROJECT_FILE, "w", encoding="utf-8") as f:
        f.write(name)


def get_stored_project_name() -> str | None:
    if os.path.exists(STORED_PROJECT_FILE):
        with open(STORED_PROJECT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None
