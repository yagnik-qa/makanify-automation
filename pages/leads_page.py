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
        self.project_dropdown = page.locator("//form//button[contains(., 'Select Project') or contains(., 'Select project')]")
        self.field_11_dropdown = page.locator("//form/div[11]//button[1]")

    def expect_on_leads_page(self) -> None:
        expect(self.page).to_have_url(LEADS_URL)

    def open_add_lead_form(self) -> None:
        self.add_lead_button.click()
        self.contact_dropdown.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)

    def select_contact_random(self) -> str:
        selected_contact = self.click_and_select_random_option(self.contact_dropdown)
        expect(self.contact_combobox).not_to_contain_text("Select contact")
        return selected_contact

    def fill_remaining_dropdowns(self) -> str:
        for primary_xpath, fallback_xpath in self.FORM_COMBOBOX_STEPS:
            combobox = self._resolve_combobox(primary_xpath, fallback_xpath)
            self.click_and_select_first_option(combobox)

        field_11 = self.click_with_fallback(
            self.project_dropdown,
            self.field_11_dropdown,
        )
        
        from config.settings import get_stored_project_name
        stored_project = get_stored_project_name()
        if stored_project:
            print(f"Selecting stored project name: '{stored_project}'")
            self.click_and_select_specific_option(field_11, stored_project)
            project_name = stored_project
        else:
            print("No stored project name found. Selecting dynamic random project name...")
            project_name = self.click_and_select_random_option(field_11)

        # Select Purpose combobox
        purpose_combobox = self.page.locator("form button", has_text="Purpose")
        self.click_and_select_first_option(purpose_combobox)
        return project_name

    def save_lead(self) -> None:
        self.save_lead_button.scroll_into_view_if_needed()
        self.save_lead_button.click()

    def verify_success_toast(self) -> None:
        expect(self.page.get_by_text("Lead Created", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Successfully created the lead.", exact=True)).to_be_visible()

    def create_lead_full_flow(self) -> tuple[str, str]:
        self.open_add_lead_form()
        contact_name = self.select_contact_random()
        project_name = self.fill_remaining_dropdowns()
        self.save_lead()
        self.verify_success_toast()
        self.expect_on_leads_page()
        print(f"\nSUCCESS: Selected contact name: {contact_name}")
        print(f"SUCCESS: Selected project name: {project_name}")
        return contact_name, project_name

    def click_contact_in_listing(self, contact_name: str) -> None:
        parts = [p.strip() for p in contact_name.split("  ") if p.strip()]
        clean_name = None
        for part in parts:
            # Skip initials (usually <= 2 chars and uppercase)
            if len(part) <= 2 and part.isupper() and len(parts) > 1:
                continue
            # Skip phone numbers
            if part.startswith("+") or part.replace(" ", "").isdigit():
                continue
            clean_name = part
            break
        if not clean_name:
            clean_name = parts[0]
        
        print(f"Extracted clean name for listing search: '{clean_name}' (from '{contact_name}')")
        
        # Reload the page to ensure the list fetches the latest lead from the database
        self.page.reload()
        self.page.wait_for_timeout(3000)

        # Print the first contact text for diagnostics
        first_contact = self.page.locator("div.font-medium.capitalize").first
        first_contact.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        print(f"First contact name in table: '{first_contact.inner_text().strip()}'")

        contact_element = self.page.locator("div.font-medium.capitalize", has_text=clean_name).first
        contact_element.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        contact_element.scroll_into_view_if_needed()
        contact_element.click()
        
        # Wait for the details page URL and load state
        import re
        self.page.wait_for_url(re.compile(r"/leads/.+\?id=.+"), timeout=15000)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(3000)

    def click_schedule_tab(self) -> None:
        import re
        self.page.get_by_role("tab", name="Schedule", exact=True).click()
        time_trigger = self.page.locator("button").filter(
            has_text=re.compile(r"Select time|\d{1,2}:\d{2}\s*(?:AM|PM)")
        ).first
        time_trigger.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)

    def select_random_time_slot(self) -> None:
        import re
        import random
        time_trigger = self.page.locator("button").filter(
            has_text=re.compile(r"Select time|\d{1,2}:\d{2}\s*(?:AM|PM)")
        ).first
        time_trigger.click()
        self.page.wait_for_timeout(1000)
        
        enabled_slots = self.page.locator("button:not([disabled])").filter(
            has_text=re.compile(r"^\d{1,2}:\d{2}\s*(?:AM|PM)$")
        ).all()
        
        if not enabled_slots:
            raise Exception("No available (enabled) time slots found!")
            
        selected_slot = random.choice(enabled_slots)
        slot_text = selected_slot.inner_text().strip()
        print(f"Selected random time slot: {slot_text}")
        selected_slot.scroll_into_view_if_needed()
        selected_slot.click()
        expect(time_trigger).to_have_text(slot_text)

    def submit_schedule(self) -> None:
        self.page.get_by_role("button", name="Schedule", exact=True).click()
        # Wait for Next.js navigation / page reload to complete
        import re
        self.page.wait_for_url(re.compile(r"/leads/.+"), timeout=15000)
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000)

    def verify_activity_scheduled(self, expected_title: str = "call back") -> None:
        import re
        # Wait for the timeline heading to be visible
        timeline_heading = self.page.locator("xpath=//h3[contains(., 'Activity Timeline')]")
        timeline_heading.wait_for(state="visible", timeout=10000)
        
        # Verify the expected activity title is visible inside the timeline area
        timeline_area = self.page.locator("xpath=//h3[contains(., 'Activity Timeline')]/parent::div/following-sibling::div")
        
        # Wait for timeline to load stably (by waiting for 'Lead Created' to be visible)
        lead_created = timeline_area.get_by_text("Lead Created").first
        lead_created.wait_for(state="visible", timeout=15000)
        
        item = timeline_area.get_by_text(re.compile(re.escape(expected_title), re.IGNORECASE)).first
        expect(item).to_be_visible(timeout=10000)

    def schedule_meeting_flow(self) -> None:
        self.click_schedule_tab()
        
        # 1. Click on "Meeting" tab
        meeting_tab = self.page.get_by_role("tab", name="Meeting", exact=True)
        meeting_tab.click()
        
        # 2. Select any random available to click time slot
        self.select_random_time_slot()
        
        # 3. Enter random address in "Meeting Address"
        import random
        address = f"Random Meeting Road {random.randint(100, 999)}, Floor {random.randint(1, 5)}"
        address_input = self.page.get_by_placeholder("Enter meeting address")
        address_input.fill(address)
        print(f"Filled Meeting Address: {address}")
        
        # 4. Add some random comment
        comment = f"This is a random comment {random.randint(100, 999)} for meeting."
        comment_input = self.page.get_by_placeholder("Enter activity details here...")
        comment_input.fill(comment)
        print(f"Filled Comments: {comment}")
        
        # 5. Click on "Schedule button"
        self.submit_schedule()
        
        # 6. Verify "success" message
        self.verify_activity_scheduled("meeting")

    def schedule_site_visit_flow(self) -> None:
        self.click_schedule_tab()
        
        # 1. Click on "Site Visit" tab (User prompt wrote "Meeting" tab with "Select Property", but "Select Property" is in "Site Visit" tab)
        site_visit_tab = self.page.get_by_role("tab", name="Site Visit", exact=True)
        site_visit_tab.click()
        self.page.wait_for_timeout(3000)
        
        # 2. Select any random available to click time slot
        self.select_random_time_slot()
        
        # 3. Select any random property from "Select Property"
        import random
        property_dropdown = self.page.locator("label", has_text="Select Property").locator("xpath=..").get_by_role("combobox")
        selected_prop = self.click_and_select_random_option(property_dropdown)
        print(f"Selected random property for Site Visit: {selected_prop}")
        
        # 4. Enter any random comment and click on "schedule" button
        comment = f"Random Site Visit comment {random.randint(100, 999)}."
        comment_input = self.page.get_by_placeholder("Enter activity details here...")
        comment_input.fill(comment)
        print(f"Filled Comments: {comment}")
        
        self.submit_schedule()
        self.verify_activity_scheduled("site visit")

    def schedule_other_flow(self) -> None:
        self.click_schedule_tab()
        
        # 1. Click on "Other" tab
        other_tab = self.page.get_by_role("tab", name="Other", exact=True)
        other_tab.click()
        
        # 2. Select any random available to click time slot
        self.select_random_time_slot()
        
        # 3. Enter any random activity name in "Activity Name" field
        import random
        activity_name = f"Random Activity {random.randint(100, 999)}"
        activity_input = self.page.locator("#activityName")
        activity_input.fill(activity_name)
        activity_input.press("Tab")
        print(f"Filled Activity Name: {activity_name}")
        
        # 4. Enter any random comment and click on "schedule" button
        comment = f"Random Other activity comment {random.randint(100, 999)}."
        comment_input = self.page.get_by_placeholder("Enter activity details here...")
        comment_input.fill(comment)
        print(f"Filled Comments: {comment}")
        
        self.submit_schedule()
        self.verify_activity_scheduled(activity_name)

    def _resolve_combobox(self, primary_xpath: str, fallback_xpath: str | None) -> Locator:
        primary = self.page.locator(f"xpath={primary_xpath}")
        if fallback_xpath:
            fallback = self.page.locator(f"xpath={fallback_xpath}")
            return self.click_with_fallback(primary, fallback)
        primary.wait_for(state="visible")
        return primary
