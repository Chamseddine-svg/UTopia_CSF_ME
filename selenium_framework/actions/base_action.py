from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from core.element_finder import ElementFinder
from core.wait_strategies import WaitStrategies

class BaseAction(ABC):
    """Classe de base pour toutes les actions"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.finder = ElementFinder(driver)
        self.waiter = WaitStrategies(driver)
        
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Méthode abstraite à implémenter par chaque action"""
        pass
    
    def log_action(self, action_name: str, details: Dict = None):
        """Loggue l'exécution d'une action"""
        from utils.logger import get_logger
        logger = get_logger()
        log_msg = f"Action '{action_name}' exécutée"
        if details:
            log_msg += f" avec détails: {details}"
        logger.info(log_msg)
    
    def take_screenshot(self, prefix: str = "action"):
        """Prend une capture d'écran"""
        from utils.screenshot_manager import ScreenshotManager
        ScreenshotManager.take_screenshot(self.driver, prefix)
