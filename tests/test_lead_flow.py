from pages.dashboard_page import DashboardPage
from pages.leads_page import LeadsPage
from pages.login_page import LoginPage


def test_lead_flow_login_search_add_lead_and_save(page):
    LoginPage(page).open().login()

    DashboardPage(page).open_leads_via_search()

    leads_page = LeadsPage(page)
    leads_page.expect_on_leads_page()
    leads_page.create_lead_full_flow()
