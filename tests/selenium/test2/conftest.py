import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import Config
from login_page import LoginPage
from inventory_page import InventoryPage
from product_detail_page import ProductDetailPage


def get_chrome_options():
    """Create Chrome options based on the operating system"""
    options = Options()
    
    # Set binary location based on OS
    if sys.platform.startswith('linux'):
        # Ubuntu/Linux
        chrome_binary = os.environ.get("CHROME_BINARY", "/usr/bin/chromium-browser")
        options.binary_location = chrome_binary
    elif sys.platform.startswith('win32'):
        # Windows
        chrome_binary = os.environ.get("CHROME_BINARY", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        options.binary_location = chrome_binary
    elif sys.platform.startswith('win32'):
        # Windows
        chrome_binary = os.environ.get("CHROME_BINARY", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        options.binary_location = chrome_binary
    elif sys.platform.startswith('darwin'):
        # macOS
        chrome_binary = os.environ.get("CHROME_BINARY", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        options.binary_location = chrome_binary
    
    # Common options for all platforms
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    
    return options


@pytest.fixture(scope="function")
def driver():
    """Cross-platform WebDriver fixture"""
    options = get_chrome_options()
    
    try:
        # Try using webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception:
        # Fallback: try without explicit service
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