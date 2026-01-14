# =====================================================
# FILE: pages/login_page.py
# =====================================================
# LOGIN_PAGE_PY = '''"""
# Page Object pour la page de connexion
# """

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from config.config import Config


class LoginPage(BasePage):
    """Page de connexion SauceDemo"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CLASS_NAME, "error-button")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = Config.BASE_URL
    
    def navigate(self):
        """Navigate vers la page de login"""
        self.navigate_to(self.url)
    
    def enter_username(self, username):
        """Saisir le nom d'utilisateur"""
        self.send_keys(*self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Saisir le mot de passe"""
        self.send_keys(*self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Cliquer sur le bouton de connexion"""
        self.click_element(*self.LOGIN_BUTTON)
    
    def login(self, username, password=None):
        """Effectuer une connexion complète"""
        password = password or Config.PASSWORD
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_error_message(self):
        """Récupère le message d'erreur"""
        try:
            return self.get_text(*self.ERROR_MESSAGE)
        except:
            return None
    
    def is_error_displayed(self):
        """Vérifie si un message d'erreur est affiché"""
        return self.is_element_visible(*self.ERROR_MESSAGE, timeout=5)  # Augmenté de 3 à 5
    
    def is_login_successful(self, timeout=5):
        """Vérifie si la connexion a réussi"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("/inventory.html")
            )
            return True
        except TimeoutException:
            return False
    
    def close_error_message(self):
        """Ferme le message d'erreur"""
        if self.is_error_displayed():
            self.click_element(*self.ERROR_CLOSE_BUTTON)

