import random
import re
from playwright.sync_api import Locator, Page, expect

from config.settings import DEFAULT_TIMEOUT_MS, PROPERTIES_URL
from pages.base_page import BasePage


class PropertyPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Search & Navigation Locators
        self.search_field = page.get_by_placeholder("Search")
        self.command_search = page.get_by_placeholder("Type a command or search...")
        self.properties_option = page.get_by_role("option", name=re.compile("properties", re.IGNORECASE))
        
        # Action Locators
        self.add_property_button = page.get_by_role("button", name=re.compile("Add Property", re.IGNORECASE))
        
        # Form Locators
        self.listing_type_trigger = page.locator("//label[@for='listingType']/following-sibling::div//button").first
        self.property_cat_trigger = page.locator("//label[@for='propertyType']/following-sibling::div//button").first
        self.subcategory_trigger = page.locator("//label[@for='subcategory']/following-sibling::div//button").first
        self.project_trigger = page.locator("//label[contains(normalize-space(), 'Project Name')]/following-sibling::button").first
        self.state_trigger = page.locator("//label[@for='state']/following-sibling::div//button").first
        self.city_trigger = page.locator("//label[@for='city']/following-sibling::div//button").first
        self.locality_trigger = page.locator("//label[@for='locality']/following-sibling::div//button").first
        self.configuration_trigger = page.locator("//label[@for='configuration']/following-sibling::div//button").first
        self.furnishing_trigger = page.locator("//label[@for='furnishingType']/following-sibling::div//button").first
        
        self.carpet_area_input = page.locator("#carpetArea")
        self.owner_name_input = page.locator("#ownerName")
        self.mobile_number_input = page.locator("#ownerContact")
        self.price_input = page.locator("#price")
        
        self.brokerage_trigger = page.locator("//label[@for='brokerageAvailable']/following-sibling::div//button").first
        self.availability_trigger = page.locator("//label[@for='availability']/following-sibling::div//button").first
        self.property_title_input = page.locator("#title")
        self.submit_button = page.locator("button[type='submit'][form='property-form']").first
        
        # Search & List Locators
        self.search_input = page.locator("input[name='searchQuery']")

    def select_dropdown_option(self, trigger: Locator, option_text: str) -> None:
        print(f"select_dropdown_option: Selecting '{option_text}'")
        trigger.wait_for(state="visible", timeout=5000)
        trigger.click()
        self.page.wait_for_timeout(500)
        
        # Locate the option matching option_text (case-insensitive, trimmed)
        option = self.page.locator("//*[@role='option']").filter(
            has_text=re.compile(rf"^\s*{re.escape(option_text)}\s*$", re.IGNORECASE)
        ).first
        option.wait_for(state="visible", timeout=5000)
        option.click()
        self.page.wait_for_timeout(500)

    def select_random_dropdown_option(self, trigger: Locator) -> str:
        trigger.wait_for(state="visible", timeout=5000)
        trigger.click()
        self.page.wait_for_timeout(500)
        
        options_locator = self.page.locator("//*[@role='option']")
        options_locator.first.wait_for(state="visible", timeout=5000)
        options = options_locator.all()
        if not options:
            raise Exception("No options found in dropdown")
            
        random_index = random.randint(0, len(options) - 1)
        target_option = options[random_index]
        option_text = target_option.inner_text().strip().replace('\n', ' ')
        target_option.click()
        self.page.wait_for_timeout(500)
        return option_text

    def search_and_navigate_to_properties(self) -> None:
        print("Searching for properties...")
        self.search_field.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        self.page.wait_for_timeout(2000)
        self.search_field.click()
        
        self.command_search.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        self.command_search.fill("properties")
        
        self.properties_option.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        self.properties_option.click()
        
        # Verify redirect to properties url
        print(f"Expecting redirection to: {PROPERTIES_URL}")
        expect(self.page).to_have_url(PROPERTIES_URL, timeout=DEFAULT_TIMEOUT_MS)

    def click_add_property(self) -> None:
        print("Clicking Add Property button...")
        self.add_property_button.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        self.add_property_button.click()
        
        print("Waiting for Add Property form...")
        self.page.wait_for_timeout(3000)

    def fill_add_property_form(
        self,
        listing_type: str = "Sell",
        property_category: str = "Residential",
        carpet_area: str = "",
        owner_name: str = "",
        mobile_number: str = "",
        total_price: str = "",
        brokerage_available: str = "No",
        property_title: str = "",
    ) -> dict:
        """
        Fills the property form. Dropdowns for subcategory, project, state, city,
        locality, configuration, furnishing type, and availability are selected randomly.
        Returns a dict containing the selected random values and explicitly passed values.
        """
        # 1. Select "Sell" option from "Listing Type" dropdown
        print(f"Selecting '{listing_type}' for Listing Type...")
        self.select_dropdown_option(self.listing_type_trigger, listing_type)
        
        # 2. Select "Residential" option from "Property Category" dropdown
        print(f"Selecting '{property_category}' for Property Category...")
        self.select_dropdown_option(self.property_cat_trigger, property_category)
        self.page.wait_for_timeout(1000)
        
        # 3. Select any random option from "Sub Category" dropdown
        print("Selecting dynamic 'Sub Category'...")
        sub_cat = self.select_random_dropdown_option(self.subcategory_trigger)
        print(f"  Selected subcategory: {sub_cat}")
        
        # 4. Select any random project from "Project Name" dropdown
        print("Selecting dynamic 'Project Name'...")
        project_name = self.select_random_dropdown_option(self.project_trigger)
        print(f"  Selected project: {project_name}")
        
        # 5. Select any random State from "State" dropdown
        print("Selecting dynamic 'State'...")
        state_name = self.select_random_dropdown_option(self.state_trigger)
        print(f"  Selected state: {state_name}")
        
        # 6. Select any random City from "City" dropdown
        print("Selecting dynamic 'City'...")
        city_name = self.select_random_dropdown_option(self.city_trigger)
        print(f"  Selected city: {city_name}")
        
        # 7. Select any random Locality/Area from "Locality/Area" dropdown
        print("Selecting dynamic 'Locality/Area'...")
        print("  Waiting for Locality/Area trigger to be enabled...")
        for _ in range(10):
            if not self.locality_trigger.is_disabled():
                break
            self.page.wait_for_timeout(500)
        locality_name = self.select_random_dropdown_option(self.locality_trigger)
        print(f"  Selected locality: {locality_name}")
        
        # 8. Select any random option from "Configuration" dropdown
        print("Selecting dynamic 'Configuration'...")
        config_val = self.select_random_dropdown_option(self.configuration_trigger)
        print(f"  Selected configuration: {config_val}")
        
        # 9. Select any random option from "Furnishing Type" dropdown
        print("Selecting dynamic 'Furnishing Type'...")
        furnishing_val = self.select_random_dropdown_option(self.furnishing_trigger)
        print(f"  Selected furnishing: {furnishing_val}")
        
        # 10. Enter Carpet Area
        print(f"Entering carpet area: {carpet_area}")
        self.carpet_area_input.fill(carpet_area)
        
        # 11. Enter Owner Name
        print(f"Entering owner name: {owner_name}")
        self.owner_name_input.fill(owner_name)
        
        # 12. Enter Mobile Number
        print(f"Entering mobile number: {mobile_number}")
        self.mobile_number_input.fill(mobile_number)
        
        # 13. Enter Total Price
        print(f"Entering total price: {total_price}")
        self.price_input.fill(total_price)
        
        # 14. Select "Brokerage Available"
        print(f"Selecting '{brokerage_available}' for Brokerage Available...")
        self.select_dropdown_option(self.brokerage_trigger, brokerage_available)
        
        # 15. Select random option from "Availability" dropdown
        print("Selecting dynamic 'Availability'...")
        avail_val = self.select_random_dropdown_option(self.availability_trigger)
        print(f"  Selected availability: {avail_val}")
        
        # 16. Enter Property Title
        print(f"Entering property title: {property_title}")
        self.property_title_input.fill(property_title)
        
        return {
            "listing_type": listing_type,
            "property_category": property_category,
            "subcategory": sub_cat,
            "project_name": project_name,
            "state": state_name,
            "city": city_name,
            "locality": locality_name,
            "configuration": config_val,
            "furnishing_type": furnishing_val,
            "carpet_area": carpet_area,
            "owner_name": owner_name,
            "mobile_number": mobile_number,
            "total_price": total_price,
            "brokerage_available": brokerage_available,
            "availability": avail_val,
            "property_title": property_title,
        }

    def submit_property_form(self) -> None:
        print("Clicking Submit button...")
        self.submit_button.click()
        
        # Wait for redirection/navigation back to individual-properties
        print("Waiting for properties list page to load...")
        self.page.wait_for_url(re.compile(r"/individual-properties"), timeout=DEFAULT_TIMEOUT_MS)
        self.page.wait_for_timeout(3000)

    def search_and_verify_property(self, property_title: str) -> None:
        # Search the created property by its title
        print(f"Searching for the newly created property title: '{property_title}'")
        self.search_input.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        self.search_input.fill(property_title)
        self.page.wait_for_timeout(2000)
        
        # Verify the property is visible in listing
        print("Verifying property is visible in listing...")
        expect(self.page.get_by_text(property_title)).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
