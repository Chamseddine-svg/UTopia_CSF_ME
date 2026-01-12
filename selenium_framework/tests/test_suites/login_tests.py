import pytest
from typing import Dict, List
from actions.action_factory import ActionFactory
from data.test_data_loader import TestDataLoader
from tests.base_test import BaseTest

class TestLoginErrors(BaseTest):
    """Test Selenium 1: Gestion des erreurs de connexion - Version modulaire"""
    
    @pytest.fixture
    def auth_actions(self, driver):
        """Fixture pour les actions d'authentification"""
        return ActionFactory.create_action('auth', driver)
    
    @pytest.fixture(params=TestDataLoader.load_test_scenarios('login_errors'))
    def error_scenario(self, request):
        """Paramétrisation data-driven des scénarios d'erreur"""
        return request.param
    
    def test_login_error_scenarios(self, auth_actions, error_scenario: Dict):
        """
        Test data-driven pour les erreurs de connexion
        Format du scénario:
        {
            "test_id": "TC_LOGIN_001",
            "description": "Mauvais identifiants",
            "username": "invalid",
            "password": "wrong",
            "expected_error": "Epic sadface: Username and password...",
            "error_type": "invalid_credentials"
        }
        """
        # Étape 1: Tentative de connexion
        login_result = auth_actions.execute(
            action_type='login',
            username=error_scenario['username'],
            password=error_scenario['password'],
            expect_success=False
        )
        
        assert login_result['success'], "La tentative de connexion a échoué de manière inattendue"
        
        # Étape 2: Validation du message d'erreur
        validation_result = auth_actions.execute(
            action_type='validate_error',
            expected_error=error_scenario['expected_error'],
            error_type=error_scenario.get('error_type')
        )
        
        assert validation_result['match'], validation_result['message']
        
        # Étape 3: Fermeture du message d'erreur (si configuré)
        if error_scenario.get('test_close_button', True):
            auth_actions.login_page.close_error_message()
            
            # Vérification que le message a disparu
            remaining_error = auth_actions.login_page.get_error_message()
            assert remaining_error is None, "Le message d'erreur devrait être fermé"
    
    @pytest.mark.parametrize("empty_field", ["username", "password", "both"])
    def test_empty_fields_validation(self, auth_actions, empty_field: str):
        """Test paramétré pour les champs vides"""
        test_data = {
            "username": {"username": "", "password": "secret_sauce", "error": "Username is required"},
            "password": {"username": "standard_user", "password": "", "error": "Password is required"},
            "both": {"username": "", "password": "", "error": "Username is required"}
        }
        
        data = test_data[empty_field]
        
        # Exécution via l'action
        auth_actions.execute(
            action_type='login',
            username=data['username'],
            password=data['password'],
            expect_success=False
        )
        
        validation_result = auth_actions.execute(
            action_type='validate_error',
            expected_error=data['error']
        )
        
        assert validation_result['match'], f"Validation échouée pour champ vide: {empty_field}"
