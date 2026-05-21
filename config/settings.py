import os

BASE_URL = os.getenv("MAKANIFY_BASE_URL", "https://uat-makanify.workzy.co")
LOGIN_URL = f"{BASE_URL}/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
LEADS_URL = f"{BASE_URL}/leads"

DEFAULT_EMAIL = os.getenv("MAKANIFY_EMAIL", "sales@moweb.com")
DEFAULT_PASSWORD = os.getenv("MAKANIFY_PASSWORD", "Test@321")

DEFAULT_TIMEOUT_MS = 20_000
DROPDOWN_TIMEOUT_MS = 5_000
