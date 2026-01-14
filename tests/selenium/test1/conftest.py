import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture(scope="session")
def chrome_options():
    """Common Chrome options for all tests"""
    options = Options()
    options.add_argument("--headless") 
    
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Point to Chromium or Chrome binary
    # Default to Chromium, override with env variable if needed (good for CI)
    options.binary_location = os.environ.get("CHROME_BINARY", "/usr/bin/chromium-browser")
    
    return options

@pytest.fixture(scope="function")
def driver(chrome_options):
    """Selenium WebDriver fixture"""
    # Optionally, you can specify a custom ChromeDriver path
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

