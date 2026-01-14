# =====================================================
# FILE: pages/base_page.py
# =====================================================
# BASE_PAGE_PY = '''"""
# Classe de base pour toutes les pages
# """
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import Config


class BasePage:
    """Classe de base avec méthodes communes à toutes les pages"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def find_element(self, by, value):
        """Trouve un élément avec attente explicite"""
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def find_elements(self, by, value):
        """Trouve plusieurs éléments"""
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))
    
    def click_element(self, by, value):
        """Clique sur un élément avec attente de cliquabilité"""
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        return element
    
    def is_element_visible(self, by, value, timeout=None):
        """Vérifie si un élément est visible"""
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, by, value):
        """Vérifie si un élément est présent dans le DOM"""
        try:
            self.driver.find_element(by, value)
            return True
        except:
            return False
    
    def get_text(self, by, value):
        """Récupère le texte d'un élément"""
        return self.find_element(by, value).text
    
    def send_keys(self, by, value, text):
        """Envoie du texte à un élément"""
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
    
    def get_current_url(self):
        """Récupère l'URL actuelle"""
        return self.driver.current_url
    
    def navigate_to(self, url):
        """Navigate vers une URL"""
        self.driver.get(url)
