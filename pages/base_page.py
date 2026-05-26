from playwright.sync_api import Locator, Page, expect

from config.settings import DEFAULT_TIMEOUT_MS, DROPDOWN_TIMEOUT_MS


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(DEFAULT_TIMEOUT_MS)

    def goto(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def click_and_select_first_option(self, trigger: Locator) -> None:
        try:
            trigger.scroll_into_view_if_needed(timeout=3_000)
            trigger.click(timeout=3_000)
        except Exception:
            trigger.evaluate("el => el.click()")
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
        try:
            option.scroll_into_view_if_needed(timeout=2_000)
            option.click(timeout=2_000)
        except Exception:
            option.evaluate("el => el.click()")

    def click_and_select_random_option(self, trigger: Locator) -> str:
        try:
            trigger.scroll_into_view_if_needed(timeout=3_000)
            trigger.click(timeout=3_000)
        except Exception:
            trigger.evaluate("el => el.click()")
        options_locator = self.page.locator(
            "xpath=(//*[@role='listbox'])[last()]//*[@role='option'][normalize-space()!='']"
        )
        try:
            options_locator.first.wait_for(state="visible", timeout=DROPDOWN_TIMEOUT_MS)
        except Exception:
            options_locator = self.page.locator(
                "xpath=//*[@role='option'][normalize-space()!='']"
            )
            options_locator.first.wait_for(state="visible", timeout=DROPDOWN_TIMEOUT_MS)
        count = options_locator.count()
        if count == 0:
            raise Exception("No options found in dropdown listbox")
        import random
        random_index = random.randint(0, count - 1)
        target_option = options_locator.nth(random_index)
        option_text = target_option.inner_text().strip().replace('\n', ' ')
        try:
            target_option.scroll_into_view_if_needed(timeout=2_000)
            target_option.click(timeout=2_000)
        except Exception:
            target_option.evaluate("el => el.click()")
        return option_text

    def click_with_fallback(self, primary: Locator, fallback: Locator) -> Locator:
        try:
            primary.wait_for(state="visible", timeout=2_000)
            return primary
        except Exception:
            fallback.wait_for(state="visible")
            return fallback
