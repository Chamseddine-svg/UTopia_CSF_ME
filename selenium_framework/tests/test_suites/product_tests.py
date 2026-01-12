import pytest
from actions.action_factory import ActionFactory
from data.test_data_loader import TestDataLoader
from tests.base_test import BaseTest

class TestProductsNavigation(BaseTest):
    """Test Selenium 2: Navigation et vérification des produits - Version modulaire"""
    
    @pytest.fixture
    def product_actions(self, driver):
        return ActionFactory.create_action('product', driver)
    
    @pytest.fixture
    def navigation_actions(self, driver):
        return ActionFactory.create_action('navigation', driver)
    
    @pytest.fixture
    def test_products(self):
        """Charge la liste des produits à tester"""
        return TestDataLoader.load_test_scenarios('products')
    
    def test_all_products_present(self, product_actions, test_products: List[Dict]):
        """Vérifie que tous les produits spécifiques sont présents"""
        validation_result = product_actions.execute(
            action_type='validate_products',
            expected_products=test_products
        )
        
        # Assertions détaillées
        assert validation_result['all_valid'], \
            f"Produits manquants ou invalides: {validation_result['missing_products']}"
        
        # Log des résultats
        for result in validation_result['validation_results']:
            if not result['all_passed']:
                failed = [k for k, v in result['validations'].items() if not v]
                print(f"Produit '{result['product']}' a échoué: {failed}")
    
    def test_product_navigation_flow(self, product_actions, navigation_actions):
        """Test complet de navigation produit"""
        # 1. Cliquer sur le produit
        click_result = product_actions.execute(
            action_type='navigate_to_details',
            product_name="Sauce Labs Backpack"
        )
        
        assert click_result['success'], "Échec de la navigation vers les détails"
        
        # 2. Valider les détails
        details_result = product_actions.execute(
            action_type='validate_product_details',
            expected_name="Sauce Labs Backpack",
            expected_price="$29.99"
        )
        
        assert details_result['valid'], "Détails du produit invalides"
        
        # 3. Retourner aux produits
        back_result = navigation_actions.execute(
            action_type='go_back'
        )
        
        assert back_result['success'], "Échec du retour à la liste"
        
        # 4. Vérifier le nombre de produits
        count_result = product_actions.execute(
            action_type='count_products'
        )
        
        assert count_result['count'] == 6, \
            f"Nombre de produits incorrect: {count_result['count']}"
    
    @pytest.mark.parametrize("product_index", range(6))
    def test_each_product_has_required_elements(self, product_actions, product_index: int):
        """Test que chaque produit a tous les éléments requis"""
        result = product_actions.execute(
            action_type='validate_product_elements',
            product_index=product_index,
            required_elements=['image', 'name', 'price', 'add_to_cart_button']
        )
        
        assert result['all_present'], \
            f"Produit {product_index} manque: {result['missing_elements']}"
