import os
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List

class BrowserType(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"

class Environment(Enum):
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"

@dataclass
class TestSettings:
    """Configuration des tests"""
    browser: BrowserType = BrowserType.CHROME
    headless: bool = False
    implicit_wait: int = 10
    explicit_wait: int = 30
    page_load_timeout: int = 60
    screenshot_on_failure: bool = True
    screenshot_on_success: bool = False
    video_recording: bool = False
    highlight_elements: bool = True
    
@dataclass
class EnvironmentSettings:
    """Configuration par environnement"""
    name: Environment
    base_url: str
    api_url: str
    db_connection: Optional[Dict] = None
    test_users: List[Dict] = None
    
@dataclass
class ReportingSettings:
    """Configuration des rapports"""
    generate_html_report: bool = True
    generate_allure_report: bool = False
    report_dir: Path = Path("reports")
    allure_results_dir: Path = Path("allure-results")
    attach_screenshots: bool = True
    attach_logs: bool = True

class ConfigManager:
    """Gestionnaire centralisé de configuration"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Charge la configuration depuis différents sources"""
        # Priorité: variables d'environnement > fichier .env > valeurs par défaut
        env = os.getenv('TEST_ENV', 'test').upper()
        
        self.test_settings = TestSettings(
            browser=BrowserType(os.getenv('BROWSER', 'chrome')),
            headless=os.getenv('HEADLESS', 'false').lower() == 'true'
        )
        
        self.environment = self._get_environment_settings(env)
        self.reporting = ReportingSettings()
        
        # Chargement dynamique de configurations additionnelles
        self._load_custom_configs()
    
    def _get_environment_settings(self, env: str) -> EnvironmentSettings:
        """Retourne les paramètres pour l'environnement spécifié"""
        environments = {
            'DEV': EnvironmentSettings(
                name=Environment.DEV,
                base_url="https://dev.saucedemo.com",
                api_url="https://dev.api.saucedemo.com"
            ),
            'TEST': EnvironmentSettings(
                name=Environment.TEST,
                base_url="https://www.saucedemo.com",
                api_url="https://api.saucedemo.com"
            ),
            'STAGING': EnvironmentSettings(
                name=Environment.STAGING,
                base_url="https://staging.saucedemo.com",
                api_url="https://staging.api.saucedemo.com"
            ),
            'PROD': EnvironmentSettings(
                name=Environment.PROD,
                base_url="https://prod.saucedemo.com",
                api_url="https://prod.api.saucedemo.com"
            )
        }
        
        return environments.get(env, environments['TEST'])
    
    def get_settings_dict(self) -> Dict:
        """Retourne tous les paramètres sous forme de dictionnaire"""
        return {
            'test': asdict(self.test_settings),
            'environment': asdict(self.environment),
            'reporting': asdict(self.reporting)
        }
