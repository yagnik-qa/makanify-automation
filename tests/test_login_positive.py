from config.settings import DASHBOARD_URL
from pages.login_page import LoginPage


def test_login_with_valid_credentials_redirects_to_dashboard(page):
    login_page = LoginPage(page)
    login_page.open().login()
    assert page.url.rstrip("/") == DASHBOARD_URL.rstrip("/")
