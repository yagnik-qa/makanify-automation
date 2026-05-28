import os
import random

from pages.login_page import LoginPage
from pages.property_page import PropertyPage


def test_add_property_flow(page):
    # Log page errors and console errors to diagnose client-side exceptions
    page.on("pageerror", lambda err: print(f"\n[PAGE ERROR] {err}\n"))
    page.on("console", lambda msg: print(f"\n[CONSOLE ERROR] {msg.text}\n") if msg.type == "error" else None)
    
    try:
        # 1. Login
        print("Logging in...")
        LoginPage(page).open().login()
        
        # Initialize Property Page
        property_page = PropertyPage(page)
        
        # 2. Search and navigate to properties page
        property_page.search_and_navigate_to_properties()
        
        # 3. Click on "Add Property" button
        property_page.click_add_property()
        
        # 4. Generate random form values
        carpet_area = str(random.randint(1000, 9999))
        owner_name = f"Owner {random.randint(1000, 9999)}"
        mobile_number = f"9{random.randint(100000000, 999999999)}"
        total_price = str(random.randint(5000000, 15000000))
        property_title = f"Automation Prop {random.randint(10000, 99999)}"
        
        # 5. Fill property details form
        property_page.fill_add_property_form(
            listing_type="Sell",
            property_category="Residential",
            carpet_area=carpet_area,
            owner_name=owner_name,
            mobile_number=mobile_number,
            total_price=total_price,
            brokerage_available="No",
            property_title=property_title,
        )
        
        # 6. Click submit and wait for listing redirect
        property_page.submit_property_form()
        
        # 7. Search and verify the newly created property is visible in listing
        property_page.search_and_verify_property(property_title)
        
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
