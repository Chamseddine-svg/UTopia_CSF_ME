import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.selenium
def test_products_navigation_and_verification():
    # ---------- Browser setup (Chromium, headless) ----------
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
   
    options.add_argument("--start-maximized") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # ---------- 1. Login ----------
        driver.get("https://www.saucedemo.com/")

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))

        # ---------- 2. Products to verify ----------
        expected_products = {
            "Sauce Labs Backpack": "$29.99",
            "Sauce Labs Bike Light": "$9.99",
            "Sauce Labs Bolt T-Shirt": "$15.99",
            "Sauce Labs Fleece Jacket": "$49.99",
            "Sauce Labs Onesie": "$7.99",
            "Test.allTheThings() T-Shirt (Red)": "$15.99",
        }

        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(products) == 6, f"Expected 6 products, found {len(products)}"

        # ---------- 3. Verify each product ----------
        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
            image = product.find_element(By.CLASS_NAME, "inventory_item_img")
            add_button = product.find_element(By.TAG_NAME, "button")

            assert name in expected_products, f"Unexpected product: {name}"
            assert price == expected_products[name], f"Wrong price for {name}"
            assert image.is_displayed(), f"Image not visible for {name}"
            assert add_button.is_displayed(), f"Add to cart missing for {name}"

        # ---------- 4. Click Sauce Labs Backpack ----------
        driver.find_element(By.LINK_TEXT, "Sauce Labs Backpack").click()

        # ---------- 5. Verify product details page ----------
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_details_name")))

        detail_name = driver.find_element(By.CLASS_NAME, "inventory_details_name").text
        detail_price = driver.find_element(By.CLASS_NAME, "inventory_details_price").text
        detail_image = driver.find_element(By.CLASS_NAME, "inventory_details_img")

        assert detail_name == "Sauce Labs Backpack"
        assert detail_price == "$29.99"
        assert detail_image.is_displayed()

        # ---------- 6. Back to products ----------
        driver.find_element(By.ID, "back-to-products").click()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))

        # ---------- 7. Verify total products again ----------
        products_after = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(products_after) == 6

    finally:
        driver.quit()
