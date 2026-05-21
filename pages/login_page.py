from playwright.sync_api import Page, expect

from config.settings import (
    DASHBOARD_URL,
    DEFAULT_EMAIL,
    DEFAULT_PASSWORD,
    DEFAULT_TIMEOUT_MS,
    LOGIN_URL,
)
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.sign_in_button = page.get_by_role("button", name="Sign In")

    def open(self) -> "LoginPage":
        self.page.goto(LOGIN_URL, wait_until="networkidle")
        self.email_input.wait_for(state="visible")
        return self

    def login(self, email: str = DEFAULT_EMAIL, password: str = DEFAULT_PASSWORD) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        expect(self.sign_in_button).to_be_enabled(timeout=DEFAULT_TIMEOUT_MS)
        with self.page.expect_navigation(url=DASHBOARD_URL, timeout=DEFAULT_TIMEOUT_MS):
            self.sign_in_button.click()
