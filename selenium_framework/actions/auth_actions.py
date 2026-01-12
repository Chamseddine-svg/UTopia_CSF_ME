from typing import Dict, Optional, Tuple
from actions.base_action import BaseAction
from pages.login_page import LoginPage

class AuthActions(BaseAction):
    """Actions modulaires pour l'authentification"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.login_page = LoginPage(driver)
    
    def execute(self, action_type: str, **kwargs) -> Dict:
        """Exécute une action d'authentification"""
        actions_map = {
            'login': self.perform_login,
            'logout': self.perform_logout,
            'validate_error': self.validate_login_error,
            'reset_password': self.reset_password
        }
        
        if action_type not in actions_map:
            raise ValueError(f"Action '{action_type}' non supportée")
        
        return actions_map[action_type](**kwargs)
    
    def perform_login(self, username: str, password: str, 
                     expect_success: bool = True, 
                     timeout: int = 10) -> Dict:
        """Effectue une connexion"""
        self.log_action("perform_login", {"username": username})
        
        try:
            self.login_page.open()
            self.login_page.enter_username(username)
            self.login_page.enter_password(password)
            self.login_page.click_login()
            
            if expect_success:
                self.waiter.wait_for_url_contains("inventory", timeout)
                result = {
                    "success": True,
                    "message": "Connexion réussie",
                    "url": self.driver.current_url
                }
            else:
                # Pour les tests d'erreur
                error_msg = self.login_page.get_error_message()
                result = {
                    "success": True if error_msg else False,
                    "error_message": error_msg,
                    "message": "Échec de connexion attendu"
                }
            
            self.take_screenshot(f"login_{username}")
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Échec de la connexion"
            }
    
    def validate_login_error(self, expected_error: str, 
                           error_type: str = None) -> Dict:
        """Valide un message d'erreur de connexion"""
        actual_error = self.login_page.get_error_message()
        
        validation_result = {
            "expected": expected_error,
            "actual": actual_error,
            "match": actual_error == expected_error,
            "error_type": error_type
        }
        
        if validation_result["match"]:
            validation_result["message"] = f"Message d'erreur '{error_type}' validé"
        else:
            validation_result["message"] = f"Message d'erreur incorrect. Attendu: '{expected_error}', Obtenu: '{actual_error}'"
        
        return validation_result
    
    def perform_logout(self) -> Dict:
        """Effectue une déconnexion"""
        # Implémentation de la déconnexion
        pass
