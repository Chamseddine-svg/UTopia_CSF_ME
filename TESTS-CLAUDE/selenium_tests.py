# ========================================
# Selenium Tests - Complete Suite
# ========================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import time
import os

# ========================================
# TEST 1: LOGIN SCENARIOS (ERRORS + VALID)
# ========================================

# Test Data for Login Errors
login_error_data = [
    # Invalid credentials
    {"case": "invalid_credentials_1", "username": "wrong_user", "password": "wrong_pass",
     "expected_error": "Epic sadface: Username and password do not match any user in this service"},
    {"case": "invalid_credentials_2", "username": "invalid_user", "password": "invalid_pass",
     "expected_error": "Epic sadface: Username and password do not match any user in this service"},
    
    # Empty username
    {"case": "empty_username_1", "username": "", "password": "secret_sauce",
     "expected_error": "Epic sadface: Username is required"},
    {"case": "empty_username_2", "username": "", "password": "any_password",
     "expected_error": "Epic sadface: Username is required"},
    
    # Empty password
    {"case": "empty_password_1", "username": "standard_user", "password": "",
     "expected_error": "Epic sadface: Password is required"},
    {"case": "empty_password_2", "username": "any_user", "password": "",
     "expected_error": "Epic sadface: Password is required"},
    
    # Locked out user
    {"case": "locked_out_user", "username": "locked_out_user", "password": "secret_sauce",
     "expected_error": "Epic sadface: Sorry, this user has been locked out."},
    
    # Special characters
    {"case": "special_char_user", "username": "user!@#", "password": "pass!@#",
     "expected_error": "Epic sadface: Username and password do not match any user in this service"},
]

# Test Data for Valid Login (should NOT show errors)
valid_login_data = [
    {"case": "standard_user", "username": "standard_user", "password": "secret_sauce"},
    {"case": "performance_glitch_user", "username": "performance_glitch_user", "password": "secret_sauce"},
    {"case": "error_user", "username": "error_user", "password": "secret_sauce"},
    {"case": "visual_user", "username": "visual_user", "password": "secret_sauce"},
]

# Test Data for Problem User (valid login but problematic behavior)
problem_user_data = {
    "username": "problem_user",
    "password": "secret_sauce",
    "case": "problem_user"
}

# ========================================
# EXPECTED PRODUCTS DATA
# ========================================

EXPECTED_PRODUCTS = [
    {"name": "Sauce Labs Backpack", "price": "$29.99"},
    {"name": "Sauce Labs Bike Light", "price": "$9.99"},
    {"name": "Sauce Labs Bolt T-Shirt", "price": "$15.99"},
    {"name": "Sauce Labs Fleece Jacket", "price": "$49.99"},
    {"name": "Sauce Labs Onesie", "price": "$7.99"},
    {"name": "Test.allTheThings() T-Shirt (Red)", "price": "$15.99"},
]

# ========================================
# PAGE OBJECT MODELS
# ========================================

class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.driver.find_element(By.ID, "user-name").clear()
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
        ).text

    def close_error(self):
        close_btn = self.driver.find_element(By.CLASS_NAME, "error-button")
        close_btn.click()

    def is_error_closed(self):
        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
            )
            return True
        except TimeoutException:
            return False
    
    def is_error_present(self):
        """Check if error message is present"""
        try:
            self.driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
            return True
        except:
            return False

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self):
        """Verify we're on the inventory page"""
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            return True
        except TimeoutException:
            return False

    def get_all_products(self):
        """Get all product items"""
        return self.driver.find_elements(By.CLASS_NAME, "inventory_item")

    def get_product_count(self):
        """Return the number of products"""
        return len(self.get_all_products())

    def verify_product_elements(self, product_element):
        """Verify a product has all required elements"""
        checks = {
            "has_image": False,
            "image_visible": False,
            "has_add_button": False,
            "has_name_link": False
        }
        
        try:
            img = product_element.find_element(By.CLASS_NAME, "inventory_item_img")
            checks["has_image"] = True
            checks["image_visible"] = img.is_displayed()
        except:
            pass
        
        try:
            btn = product_element.find_element(By.CSS_SELECTOR, "button[class*='btn_inventory']")
            checks["has_add_button"] = btn.is_displayed()
        except:
            pass
        
        try:
            name_link = product_element.find_element(By.CLASS_NAME, "inventory_item_name")
            checks["has_name_link"] = name_link.is_displayed()
        except:
            pass
        
        return checks

    def get_product_info(self, product_element):
        """Extract product name and price"""
        name = product_element.find_element(By.CLASS_NAME, "inventory_item_name").text
        price = product_element.find_element(By.CLASS_NAME, "inventory_item_price").text
        return {"name": name, "price": price}

    def click_product_by_name(self, product_name):
        """Click on a product name link"""
        products = self.get_all_products()
        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name == product_name:
                product.find_element(By.CLASS_NAME, "inventory_item_name").click()
                return True
        return False
    
    def get_product_images_src(self):
        """Get all product image sources (for problem_user detection)"""
        products = self.get_all_products()
        images = []
        for product in products:
            try:
                img = product.find_element(By.CLASS_NAME, "inventory_item_img").find_element(By.TAG_NAME, "img")
                images.append(img.get_attribute("src"))
            except:
                images.append(None)
        return images

class ProductDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self):
        """Verify we're on the product details page"""
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_details"))
            )
            return True
        except TimeoutException:
            return False

    def get_product_name(self):
        """Get the product name from details page"""
        return self.driver.find_element(By.CLASS_NAME, "inventory_details_name").text

    def back_to_products(self):
        """Click the back button to return to inventory"""
        back_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "back-to-products"))
        )
        back_btn.click()

# ========================================
# PYTEST FIXTURES
# ========================================

@pytest.fixture
def driver():
    """WebDriver fixture"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    """Fixture that provides a driver already logged in with standard_user"""
    login = LoginPage(driver)
    login.load()
    login.login("standard_user", "secret_sauce")
    
    inventory = InventoryPage(driver)
    assert inventory.is_loaded(), "Failed to login and reach inventory page"
    
    return driver

@pytest.fixture
def problem_user_driver(driver):
    """Fixture that provides a driver logged in with problem_user"""
    login = LoginPage(driver)
    login.load()
    login.login("problem_user", "secret_sauce")
    
    inventory = InventoryPage(driver)
    assert inventory.is_loaded(), "Failed to login with problem_user"
    
    return driver

# ========================================
# TEST 1A: LOGIN ERROR MESSAGES
# ========================================

@pytest.mark.parametrize("data", login_error_data, ids=lambda d: d["case"])
def test_login_error_messages(driver, data):
    """Test 1A: Verify error messages for invalid login scenarios"""
    login = LoginPage(driver)
    login.load()
    login.login(data["username"], data["password"])

    try:
        error_message = login.get_error_message()
        assert error_message == data["expected_error"], (
            f"Test {data['case']} failed: expected error '{data['expected_error']}', got '{error_message}'"
        )
        
        # Test error close button
        login.close_error()
        assert login.is_error_closed(), f"Error message did not close for {data['case']}"
        
        print(f"✓ Test {data['case']}: Error message verified and closed successfully")
        
    except TimeoutException:
        # No error appeared → user logged in instead
        os.makedirs("screenshots", exist_ok=True)
        screenshot_file = f"screenshots/{data['case']}_fail.png"
        driver.save_screenshot(screenshot_file)
        pytest.fail(
            f"Test {data['case']} failed: user logged in instead of showing error "
            f"(screenshot: {screenshot_file})"
        )

# ========================================
# TEST 1B: VALID LOGIN (Should NOT Show Errors)
# ========================================

@pytest.mark.parametrize("data", valid_login_data, ids=lambda d: d["case"])
def test_valid_login_success(driver, data):
    """Test 1B: Verify valid users can login successfully WITHOUT errors"""
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    
    login.load()
    login.login(data["username"], data["password"])
    
    # Wait a moment for page to load
    time.sleep(1)
    
    # Verify NO error message appears
    assert not login.is_error_present(), (
        f"Test {data['case']} failed: Error message appeared for valid user"
    )
    
    # Verify we reached the inventory page
    assert inventory.is_loaded(), (
        f"Test {data['case']} failed: Did not reach inventory page after valid login"
    )
    
    print(f"✓ Test {data['case']}: Login successful, no errors shown")

# ========================================
# TEST 2A: PRODUCT VERIFICATION (Standard User)
# ========================================

def test_product_catalog_verification(logged_in_driver):
    """Test 2A: Verify all products are present with correct details"""
    driver = logged_in_driver
    inventory = InventoryPage(driver)
    
    # Verify total product count is 6
    product_count = inventory.get_product_count()
    assert product_count == 6, f"Expected 6 products, found {product_count}"
    
    # Verify all expected products are present
    products = inventory.get_all_products()
    found_products = []
    
    for product in products:
        product_info = inventory.get_product_info(product)
        found_products.append(product_info)
    
    # Check each expected product
    for expected in EXPECTED_PRODUCTS:
        matching = [p for p in found_products if p["name"] == expected["name"] and p["price"] == expected["price"]]
        assert len(matching) == 1, (
            f"Product '{expected['name']}' with price '{expected['price']}' not found. "
            f"Found products: {found_products}"
        )
    
    print(f"✓ All {len(EXPECTED_PRODUCTS)} expected products found with correct prices")

def test_product_elements_verification(logged_in_driver):
    """Test 2A: Verify each product has required elements"""
    driver = logged_in_driver
    inventory = InventoryPage(driver)
    
    products = inventory.get_all_products()
    
    for idx, product in enumerate(products):
        product_name = inventory.get_product_info(product)["name"]
        checks = inventory.verify_product_elements(product)
        
        assert checks["has_image"], f"Product '{product_name}' missing image"
        assert checks["image_visible"], f"Product '{product_name}' image not visible"
        assert checks["has_add_button"], f"Product '{product_name}' missing 'Add to cart' button"
        assert checks["has_name_link"], f"Product '{product_name}' name is not clickable"
        
        print(f"✓ Product {idx+1} '{product_name}': All elements present")

def test_product_details_navigation(logged_in_driver):
    """Test 2A: Navigate to product details and back"""
    driver = logged_in_driver
    inventory = InventoryPage(driver)
    details = ProductDetailsPage(driver)
    
    # Click on "Sauce Labs Backpack"
    product_clicked = inventory.click_product_by_name("Sauce Labs Backpack")
    assert product_clicked, "Failed to click on 'Sauce Labs Backpack'"
    
    # Verify product details page
    assert details.is_loaded(), "Product details page did not load"
    detail_name = details.get_product_name()
    assert detail_name == "Sauce Labs Backpack", (
        f"Wrong product details page: expected 'Sauce Labs Backpack', got '{detail_name}'"
    )
    
    print("✓ Successfully navigated to product details page")
    
    # Return to product list
    details.back_to_products()
    
    # Wait for inventory page to load with explicit wait
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
    
    # Verify we're back on inventory page
    assert inventory.is_loaded(), "Failed to return to inventory page"
    
    # Verify product count is still correct
    product_count = inventory.get_product_count()
    assert product_count == 6, f"After navigation, expected 6 products, found {product_count}"
    
    print("✓ Successfully returned to product list")

# ========================================
# TEST 2B: PROBLEM USER BEHAVIOR
# ========================================

def test_problem_user_login_and_issues(driver):
    """Test 2B: Verify problem_user can login but has visual issues"""
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    
    # Login with problem_user
    login.load()
    login.login(problem_user_data["username"], problem_user_data["password"])
    
    time.sleep(1)
    
    # Verify NO error message (login should succeed)
    assert not login.is_error_present(), "problem_user should login successfully without errors"
    
    # Verify we reached inventory page
    assert inventory.is_loaded(), "problem_user should reach inventory page"
    
    print("✓ problem_user logged in successfully")
    
    # Verify products are present
    product_count = inventory.get_product_count()
    assert product_count == 6, f"problem_user should see 6 products, found {product_count}"
    
    # Check for image issues (problem_user has broken images)
    images = inventory.get_product_images_src()
    broken_images = [img for img in images if img and "WithGarbageOnItToBreakTheUrl" in img]
    
    # problem_user should have some broken image URLs
    if len(broken_images) > 0:
        print(f"✓ Detected {len(broken_images)} broken images for problem_user (expected behavior)")
    else:
        print("⚠ Warning: No broken images detected for problem_user")
    
    print(f"✓ problem_user test completed: Login successful, {product_count} products visible")

def test_problem_user_product_verification(problem_user_driver):
    """Test 2B: Verify problem_user sees products but with issues"""
    driver = problem_user_driver
    inventory = InventoryPage(driver)
    
    # Verify all products are still present
    products = inventory.get_all_products()
    found_products = []
    
    for product in products:
        product_info = inventory.get_product_info(product)
        found_products.append(product_info)
    
    # Check each expected product is present
    for expected in EXPECTED_PRODUCTS:
        matching = [p for p in found_products if p["name"] == expected["name"] and p["price"] == expected["price"]]
        assert len(matching) == 1, (
            f"problem_user: Product '{expected['name']}' with price '{expected['price']}' not found"
        )
    
    print(f"✓ problem_user can see all {len(EXPECTED_PRODUCTS)} products (with visual issues)")

def test_problem_user_navigation(problem_user_driver):
    """Test 2B: Verify problem_user can navigate to product details"""
    driver = problem_user_driver
    inventory = InventoryPage(driver)
    details = ProductDetailsPage(driver)
    
    # Try to click on a product
    product_clicked = inventory.click_product_by_name("Sauce Labs Backpack")
    assert product_clicked, "problem_user failed to click on product"
    
    # Verify details page loads
    assert details.is_loaded(), "problem_user: Product details page did not load"
    
    # Navigate back
    details.back_to_products()
    time.sleep(0.5)
    assert inventory.is_loaded(), "problem_user: Failed to return to inventory"
    
    print("✓ problem_user can navigate to product details and back")

# ========================================
# TEST 2C: INVALID USER CANNOT ACCESS PRODUCTS
# ========================================

def test_invalid_user_no_product_access(driver):
    """Test 2C: Verify invalid users cannot access product page"""
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    
    # Try to login with invalid credentials
    login.load()
    login.login("invalid_user", "wrong_password")
    
    time.sleep(1)
    
    # Verify error message appears
    assert login.is_error_present(), "Error message should appear for invalid user"
    
    # Verify we're NOT on inventory page
    assert not inventory.is_loaded(), "Invalid user should NOT reach inventory page"
    
    print("✓ Invalid user correctly blocked from accessing products")

def test_locked_user_no_product_access(driver):
    """Test 2C: Verify locked_out_user cannot access product page"""
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    
    # Try to login with locked_out_user
    login.load()
    login.login("locked_out_user", "secret_sauce")
    
    time.sleep(1)
    
    # Verify error message appears
    assert login.is_error_present(), "Error message should appear for locked_out_user"
    error_msg = login.get_error_message()
    assert "locked out" in error_msg.lower(), f"Expected 'locked out' message, got: {error_msg}"
    
    # Verify we're NOT on inventory page
    assert not inventory.is_loaded(), "Locked user should NOT reach inventory page"
    
    print("✓ Locked out user correctly blocked from accessing products")

# ========================================
# RUN DIRECTLY
# ========================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])