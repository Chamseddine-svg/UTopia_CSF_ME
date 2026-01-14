# =====================================================
# FILE: tests/conftest.py
# =====================================================
# CONFTEST_PY = '''"""
# Fixtures pytest partagées pour tous les tests
# """

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage


@pytest.fixture(scope="function")
def driver():
    """Fixture pour initialiser et fermer le driver"""
    
    # Configuration du driver Chrome
    chrome_options = Options()
    if Config.HEADLESS:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialisation du driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Configuration
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    if Config.MAXIMIZE_WINDOW:
        driver.maximize_window()
    
    yield driver
    
    # Nettoyage
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """Fixture pour la page de login"""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def inventory_page(driver):
    """Fixture pour la page inventaire"""
    return InventoryPage(driver)


@pytest.fixture(scope="function")
def product_detail_page(driver):
    """Fixture pour la page détails produit"""
    return ProductDetailPage(driver)


@pytest.fixture(scope="function")
def authenticated_user(driver, login_page):
    """Fixture pour un utilisateur déjà connecté (standard_user)"""
    login_page.navigate()
    login_page.login("standard_user")
    assert login_page.is_login_successful(), "La connexion a échoué"
    return driver


@pytest.fixture(scope="function")
def authenticated_user_factory(driver, login_page):
    """Factory fixture pour connecter différents utilisateurs"""
    def _login(username):
        login_page.navigate()
        login_page.login(username)
        assert login_page.is_login_successful(), f"La connexion a échoué pour {username}"
        return driver
    return _login
