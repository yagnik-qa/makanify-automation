from pages.dashboard_page import DashboardPage
from pages.leads_page import LeadsPage
from pages.login_page import LoginPage


def test_lead_flow_login_search_add_lead_and_save(page):
    # Log page errors and console errors to diagnose client-side exceptions
    page.on("pageerror", lambda err: print(f"\n[PAGE ERROR] {err}\n"))
    page.on("console", lambda msg: print(f"\n[CONSOLE ERROR] {msg.text}\n") if msg.type == "error" else None)
    try:
        LoginPage(page).open().login()

        DashboardPage(page).open_leads_via_search()

        leads_page = LeadsPage(page)
        leads_page.expect_on_leads_page()
        
        # 1. Create a lead and get contact name and project name
        contact_name, project_name = leads_page.create_lead_full_flow()

        # 2. Click on the contact from listing
        print(f"Clicking contact '{contact_name}' in the listing...")
        leads_page.click_contact_in_listing(contact_name)

        # 3. Click on "Schedule" tab
        print("Navigating to Schedule tab...")
        leads_page.click_schedule_tab()

        # 4. Select a random available time slot
        leads_page.select_random_time_slot()

        # 5. Click on "Schedule" button (submit)
        print("Submitting the schedule activity...")
        leads_page.submit_schedule()

        # 6. Verify "Success" message
        print("Verifying success message toast...")
        leads_page.verify_activity_scheduled()

        # 8. Schedule a Meeting
        print("Scheduling meeting...")
        leads_page.schedule_meeting_flow()

        # 9. Schedule a Site Visit
        print("Scheduling site visit...")
        leads_page.schedule_site_visit_flow()

        # 10. Schedule Other Activity
        print("Scheduling other activity...")
        leads_page.schedule_other_flow()

        # 11. Take verification screenshot
        page.wait_for_timeout(2000)
        import os
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = "screenshots/meeting_scheduled.png"
        page.screenshot(path=screenshot_path)
        print(f"Test complete. Verification screenshot saved to {screenshot_path}")
        print(f"TEST RESULT: Randomly selected project: {project_name}")
    except Exception as e:
        import os
        os.makedirs("screenshots", exist_ok=True)
        failure_path = "screenshots/failure.png"
        page.screenshot(path=failure_path)
        print(f"TEST FAILED: {e}. Screenshot saved to {failure_path}")
        raise e
