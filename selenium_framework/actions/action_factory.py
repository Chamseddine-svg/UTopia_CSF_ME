from typing import Dict, Type
from actions.base_action import BaseAction
from actions.auth_actions import AuthActions
from actions.product_actions import ProductActions
from actions.cart_actions import CartActions
from actions.navigation_actions import NavigationActions

class ActionFactory:
    """Factory pour créer des instances d'actions"""
    
    _action_registry: Dict[str, Type[BaseAction]] = {}
    
    @classmethod
    def register_action(cls, action_type: str, action_class: Type[BaseAction]):
        """Enregistre une nouvelle action"""
        cls._action_registry[action_type] = action_class
    
    @classmethod
    def create_action(cls, action_type: str, driver) -> BaseAction:
        """Crée une instance d'action"""
        if action_type not in cls._action_registry:
            raise ValueError(f"Type d'action '{action_type}' non enregistré")
        
        return cls._action_registry[action_type](driver)
    
    @classmethod
    def get_available_actions(cls) -> List[str]:
        """Retourne la liste des actions disponibles"""
        return list(cls._action_registry.keys())

# Enregistrement des actions
ActionFactory.register_action('auth', AuthActions)
ActionFactory.register_action('product', ProductActions)
ActionFactory.register_action('cart', CartActions)
ActionFactory.register_action('navigation', NavigationActions)
