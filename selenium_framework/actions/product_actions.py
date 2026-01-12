from typing import List, Dict, Optional
from actions.base_action import BaseAction
from pages.products_page import ProductsPage

class ProductActions(BaseAction):
    """Actions modulaires pour la gestion des produits"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.products_page = ProductsPage(driver)
    
    def execute(self, action_type: str, **kwargs) -> Dict:
        actions_map = {
            'validate_products': self.validate_product_list,
            'add_to_cart': self.add_product_to_cart,
            'remove_from_cart': self.remove_product_from_cart,
            'sort_products': self.sort_products,
            'navigate_to_details': self.navigate_to_product_details,
            'validate_product_details': self.validate_product_details
        }
        
        if action_type not in actions_map:
            raise ValueError(f"Action produit '{action_type}' non supportée")
        
        return actions_map[action_type](**kwargs)
    
    def validate_product_list(self, expected_products: List[Dict]) -> Dict:
        """Valide la liste des produits"""
        actual_products = self.products_page.get_all_products()
        
        validation_results = []
        missing_products = []
        
        for expected in expected_products:
            found = False
            for actual in actual_products:
                if actual['name'] == expected['name']:
                    found = True
                    
                    # Validation détaillée
                    validations = {
                        'name': actual['name'] == expected['name'],
                        'price': actual['price'] == expected['price'],
                        'image_visible': actual.get('image_visible', False),
                        'button_text': actual.get('button_text') == 'Add to cart',
                        'name_clickable': actual.get('name_clickable', False)
                    }
                    
                    validation_results.append({
                        'product': expected['name'],
                        'validations': validations,
                        'all_passed': all(validations.values())
                    })
                    break
            
            if not found:
                missing_products.append(expected['name'])
        
        return {
            'total_expected': len(expected_products),
            'total_found': len(actual_products),
            'validation_results': validation_results,
            'missing_products': missing_products,
            'all_valid': len(missing_products) == 0 and all(r['all_passed'] for r in validation_results)
        }
    
    def add_product_to_cart(self, product_name: str, 
                          validate: bool = True) -> Dict:
        """Ajoute un produit au panier"""
        result = self.products_page.add_to_cart(product_name)
        
        if validate:
            cart_count = self.products_page.get_cart_item_count()
            
        return {
            'product': product_name,
            'action': 'add_to_cart',
            'success': result,
            'cart_count_after': cart_count if validate else None
        }
