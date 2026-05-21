from playwright.sync_api import Locator, Page, expect

from config.settings import DEFAULT_TIMEOUT_MS, DROPDOWN_TIMEOUT_MS


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(DEFAULT_TIMEOUT_MS)

    def goto(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def click_and_select_first_option(self, trigger: Locator) -> None:
        trigger.scroll_into_view_if_needed()
        trigger.click()
        option = self.page.locator(
            "xpath=((//*[@role='listbox'])[last()]//*[@role='option'][normalize-space()!=''])[1]"
        )
        try:
            option.wait_for(state="visible", timeout=DROPDOWN_TIMEOUT_MS)
        except Exception:
            option = self.page.locator(
                "xpath=(//*[@role='option'][normalize-space()!=''])[1]"
            )
            option.wait_for(state="visible", timeout=DROPDOWN_TIMEOUT_MS)
        option.click()

    def click_with_fallback(self, primary: Locator, fallback: Locator) -> Locator:
        try:
            primary.wait_for(state="visible", timeout=2_000)
            return primary
        except Exception:
            fallback.wait_for(state="visible")
            return fallback
