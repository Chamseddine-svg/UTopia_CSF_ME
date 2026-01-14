import sys
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# FIX PYTHON PATH
PROJECT_ROOT = Path(__file__).resolve().parents[2] / "selenium" / "verify_product_test"
sys.path.insert(0, str(PROJECT_ROOT))

from config.config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def inventory_page(driver):
    return InventoryPage(driver)


@pytest.fixture
def product_detail_page(driver):
    return ProductDetailPage(driver)


@pytest.fixture
def authenticated_user(driver, login_page):
    login_page.navigate()
    login_page.login("standard_user")
    assert login_page.is_login_successful()
    return driver


@pytest.fixture
def authenticated_user_factory(driver, login_page):
    def _login(username):
        login_page.navigate()
        login_page.login(username)
        assert login_page.is_login_successful()
        return driver
    return _login

