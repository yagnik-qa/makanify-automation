from playwright.sync_api import Page, expect

from config.settings import LEADS_URL
from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.search_field = page.get_by_placeholder("Search")
        self.command_search = page.get_by_placeholder("Type a command or search...")
        self.leads_option = page.get_by_role("option", name="Leads", exact=True)

    def open_leads_via_search(self) -> None:
        self.search_field.wait_for(state="visible")
        self.page.wait_for_timeout(2000)
        self.search_field.click()
        self.command_search.wait_for(state="visible")
        self.command_search.fill("Leads")
        self.leads_option.wait_for(state="visible")
        self.leads_option.click()
        expect(self.page).to_have_url(LEADS_URL)
