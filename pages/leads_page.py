from playwright.sync_api import Locator, Page, expect

from config.settings import DEFAULT_TIMEOUT_MS, LEADS_URL
from pages.base_page import BasePage


class LeadsPage(BasePage):
    FORM_COMBOBOX_STEPS: tuple[tuple[str, str | None], ...] = (
        (
            "//form//button[@role='combobox' and normalize-space()='Select Source']",
            "(//form//button[@role='combobox'])[2]",
        ),
        ("(//form//button[@role='combobox'])[4]", None),
        ("(//form//button[@role='combobox'])[5]", "(//button[@role='combobox'])[7]"),
        ("(//form//button[@role='combobox'])[6]", "(//button[@role='combobox'])[8]"),
    )

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.add_lead_button = page.get_by_role("button", name="Add Lead")
        self.contact_dropdown = page.locator(
            "xpath=//form//button[@role='combobox'][normalize-space()='Select contact']"
        )
        self.contact_combobox = page.locator("xpath=(//form//button[@role='combobox'])[1]")
        self.save_lead_button = page.get_by_role("button", name="Save Lead")
        self.field_11_dropdown = page.locator("//form/div[11]//button[1]")

    def expect_on_leads_page(self) -> None:
        expect(self.page).to_have_url(LEADS_URL)

    def open_add_lead_form(self) -> None:
        self.add_lead_button.click()
        self.contact_dropdown.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)

    def select_contact_first_option(self) -> None:
        self.click_and_select_first_option(self.contact_dropdown)
        expect(self.contact_combobox).not_to_contain_text("Select contact")

    def fill_remaining_dropdowns(self) -> None:
        for primary_xpath, fallback_xpath in self.FORM_COMBOBOX_STEPS:
            combobox = self._resolve_combobox(primary_xpath, fallback_xpath)
            self.click_and_select_first_option(combobox)

        field_11 = self.click_with_fallback(
            self.page.locator("/html/body/div[11]/motion.div[2]/form/div[11]/div[1]/button[1]"),
            self.field_11_dropdown,
        )
        self.click_and_select_first_option(field_11)

    def save_lead(self) -> None:
        self.save_lead_button.scroll_into_view_if_needed()
        self.save_lead_button.click()

    def create_lead_full_flow(self) -> None:
        self.open_add_lead_form()
        self.select_contact_first_option()
        self.fill_remaining_dropdowns()
        self.save_lead()
        self.expect_on_leads_page()

    def _resolve_combobox(self, primary_xpath: str, fallback_xpath: str | None) -> Locator:
        primary = self.page.locator(f"xpath={primary_xpath}")
        if fallback_xpath:
            fallback = self.page.locator(f"xpath={fallback_xpath}")
            return self.click_with_fallback(primary, fallback)
        primary.wait_for(state="visible")
        return primary
