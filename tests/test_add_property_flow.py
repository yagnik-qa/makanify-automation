import os
import random
import re
from config.settings import DEFAULT_TIMEOUT_MS, PROPERTIES_URL
from pages.login_page import LoginPage
from playwright.sync_api import expect


def select_dropdown_option(page, trigger, option_text):
    print(f"select_dropdown_option: Selecting '{option_text}'")
    trigger.wait_for(state="visible", timeout=5000)
    trigger.click()
    page.wait_for_timeout(500)
    
    # Locate the option matching option_text (case-insensitive, trimmed)
    option = page.locator("//*[@role='option']").filter(
        has_text=re.compile(rf"^\s*{re.escape(option_text)}\s*$", re.IGNORECASE)
    ).first
    option.wait_for(state="visible", timeout=5000)
    option.click()
    page.wait_for_timeout(500)


def select_random_dropdown_option(page, trigger):
    trigger.wait_for(state="visible", timeout=5000)
    trigger.click()
    page.wait_for_timeout(500)
    
    options_locator = page.locator("//*[@role='option']")
    options_locator.first.wait_for(state="visible", timeout=5000)
    options = options_locator.all()
    if not options:
        raise Exception("No options found in dropdown")
        
    random_index = random.randint(0, len(options) - 1)
    target_option = options[random_index]
    option_text = target_option.inner_text().strip().replace('\n', ' ')
    target_option.click()
    page.wait_for_timeout(500)
    return option_text


def test_add_property_flow(page):
    # Log page errors and console errors to diagnose client-side exceptions
    page.on("pageerror", lambda err: print(f"\n[PAGE ERROR] {err}\n"))
    page.on("console", lambda msg: print(f"\n[CONSOLE ERROR] {msg.text}\n") if msg.type == "error" else None)
    
    try:
        # 1. Login
        print("Logging in...")
        LoginPage(page).open().login()
        
        # 2. Click on search and enter "properties" and click on "properties" option from dropdown
        print("Searching for properties...")
        search_field = page.get_by_placeholder("Search")
        search_field.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        page.wait_for_timeout(2000)
        search_field.click()
        
        command_search = page.get_by_placeholder("Type a command or search...")
        command_search.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        command_search.fill("properties")
        
        properties_option = page.get_by_role("option", name=re.compile("properties", re.IGNORECASE))
        properties_option.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        properties_option.click()
        
        # Verify redirect to properties url
        print(f"Expecting redirection to: {PROPERTIES_URL}")
        expect(page).to_have_url(PROPERTIES_URL, timeout=DEFAULT_TIMEOUT_MS)
        
        # 3. Click on "Add Property button"
        print("Clicking Add Property button...")
        add_property_button = page.get_by_role("button", name=re.compile("Add Property", re.IGNORECASE))
        add_property_button.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        add_property_button.click()
        
        print("Waiting for Add Property form...")
        page.wait_for_timeout(3000)
        
        # 1. Select "Sell" option from "Listing Type" dropdown
        print("Selecting 'Sell' for Listing Type...")
        listing_type_trigger = page.locator("//label[@for='listingType']/following-sibling::div//button").first
        select_dropdown_option(page, listing_type_trigger, "Sell")
        
        # 2. Select "Residential" option from "Property Category" dropdown
        print("Selecting 'Residential' for Property Category...")
        property_cat_trigger = page.locator("//label[@for='propertyType']/following-sibling::div//button").first
        select_dropdown_option(page, property_cat_trigger, "Residential")
        page.wait_for_timeout(1000)
        
        # 3. Select any random option from "Sub Category" dropdown
        print("Selecting dynamic 'Sub Category'...")
        subcategory_trigger = page.locator("//label[@for='subcategory']/following-sibling::div//button").first
        sub_cat = select_random_dropdown_option(page, subcategory_trigger)
        print(f"  Selected subcategory: {sub_cat}")
        
        # 4. Select any random project from "Project Name" dropdown
        print("Selecting dynamic 'Project Name'...")
        project_trigger = page.locator("//label[contains(normalize-space(), 'Project Name')]/following-sibling::button").first
        project_name = select_random_dropdown_option(page, project_trigger)
        print(f"  Selected project: {project_name}")
        
        # 5. Select any random State from "State" dropdown
        print("Selecting dynamic 'State'...")
        state_trigger = page.locator("//label[@for='state']/following-sibling::div//button").first
        state_name = select_random_dropdown_option(page, state_trigger)
        print(f"  Selected state: {state_name}")
        
        # 6. Select any random City from "City" dropdown
        print("Selecting dynamic 'City'...")
        city_trigger = page.locator("//label[@for='city']/following-sibling::div//button").first
        city_name = select_random_dropdown_option(page, city_trigger)
        print(f"  Selected city: {city_name}")
        
        # 7. Select any random Locality/Area from "Locality/Area" dropdown
        print("Selecting dynamic 'Locality/Area'...")
        locality_trigger = page.locator("//label[@for='locality']/following-sibling::div//button").first
        print("  Waiting for Locality/Area trigger to be enabled...")
        for _ in range(10):
            if not locality_trigger.is_disabled():
                break
            page.wait_for_timeout(500)
        locality_name = select_random_dropdown_option(page, locality_trigger)
        print(f"  Selected locality: {locality_name}")
        
        # 8. Select any random option from "Configuration" dropdown
        print("Selecting dynamic 'Configuration'...")
        configuration_trigger = page.locator("//label[@for='configuration']/following-sibling::div//button").first
        config_val = select_random_dropdown_option(page, configuration_trigger)
        print(f"  Selected configuration: {config_val}")
        
        # 9. Select any random option from "Furnishing Type" dropdown
        print("Selecting dynamic 'Furnishing Type'...")
        furnishing_trigger = page.locator("//label[@for='furnishingType']/following-sibling::div//button").first
        furnishing_val = select_random_dropdown_option(page, furnishing_trigger)
        print(f"  Selected furnishing: {furnishing_val}")
        
        # 10. Enter random 4 digit amount in "Carpet Area" field
        carpet_area = str(random.randint(1000, 9999))
        print(f"Entering carpet area: {carpet_area}")
        page.locator("#carpetArea").fill(carpet_area)
        
        # 11. Enter random person name in "Owner Name" field
        owner_name = f"Owner {random.randint(1000, 9999)}"
        print(f"Entering owner name: {owner_name}")
        page.locator("#ownerName").fill(owner_name)
        
        # 12. Enter random 10 digit mobile number in "Mobile Number" field
        mobile_number = f"9{random.randint(100000000, 999999999)}"
        print(f"Entering mobile number: {mobile_number}")
        page.locator("#ownerContact").fill(mobile_number)
        
        # 13. Enter random amount in "Total Price" field
        total_price = str(random.randint(5000000, 15000000))
        print(f"Entering total price: {total_price}")
        page.locator("#price").fill(total_price)
        
        # 14. Select "No" option from "Brokerage Available" dropdown
        print("Selecting 'No' for Brokerage Available...")
        brokerage_trigger = page.locator("//label[@for='brokerageAvailable']/following-sibling::div//button").first
        select_dropdown_option(page, brokerage_trigger, "No")
        
        # 15. Select random option from "Availability" dropdown
        print("Selecting dynamic 'Availability'...")
        availability_trigger = page.locator("//label[@for='availability']/following-sibling::div//button").first
        avail_val = select_random_dropdown_option(page, availability_trigger)
        print(f"  Selected availability: {avail_val}")
        
        # 16. Enter random property title in "Property Title" field
        property_title = f"Automation Prop {random.randint(10000, 99999)}"
        print(f"Entering property title: {property_title}")
        page.locator("#title").fill(property_title)
        
        # 17. Click on "submit" button and verify same property is visible in listing
        print("Clicking Submit button...")
        submit_button = page.locator("button[type='submit'][form='property-form']").first
        submit_button.click()
        
        # Wait for redirection/navigation back to individual-properties
        print("Waiting for properties list page to load...")
        page.wait_for_url(re.compile(r"/individual-properties"), timeout=DEFAULT_TIMEOUT_MS)
        page.wait_for_timeout(3000)
        
        # Search the created property by its title
        print(f"Searching for the newly created property title: '{property_title}'")
        search_input = page.locator("input[name='searchQuery']")
        search_input.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
        search_input.fill(property_title)
        page.wait_for_timeout(2000)
        
        # Verify the property is visible in listing
        print("Verifying property is visible in listing...")
        expect(page.get_by_text(property_title)).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
        
        # Take success screenshot
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = "screenshots/add_property_success.png"
        page.screenshot(path=screenshot_path)
        print(f"TEST SUCCESS. Verification screenshot saved to {screenshot_path}")
        
    except Exception as e:
        os.makedirs("screenshots", exist_ok=True)
        failure_path = "screenshots/add_property_failure.png"
        page.screenshot(path=failure_path)
        print(f"TEST FAILED: {e}. Screenshot saved to {failure_path}")
        raise e
