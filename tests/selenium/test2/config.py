"""
Configuration globale pour les tests SauceDemo
"""

class Config:
    """Configuration centralisée"""
    
    # URL de base
    BASE_URL = "https://www.saucedemo.com/"
    
    # Timeouts - Augmentés pour plus de stabilité
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    
    # Credentials
    PASSWORD = "secret_sauce"
    
    # Utilisateurs disponibles
    USERS = [
        "standard_user",
        "locked_out_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user"
    ]
    
    # Utilisateurs fonctionnels (qui peuvent se connecter)
    # Note: problem_user, error_user et visual_user ont des bugs intentionnels
    FUNCTIONAL_USERS = [
        "standard_user",           # ✅ User stable et fiable
        # "problem_user",          # ⚠️  Images cassées intentionnellement
        # "performance_glitch_user", # ⏱️ Très lent (délais de 5+ secondes)
        # "error_user",            # ⚠️  Comportements erratiques
        # "visual_user"            # ❌ Bugs visuels CSS
    ]
    
    # Utilisateurs pour tests spécifiques de bugs
    BUGGY_USERS = [
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user"
    ]
    
    # Produits attendus
    EXPECTED_PRODUCTS = [
        {"name": "Sauce Labs Bike Light", "price": "$9.99"},
        {"name": "Sauce Labs Backpack", "price": "$29.99"},
        {"name": "Sauce Labs Bolt T-Shirt", "price": "$15.99"},
        {"name": "Sauce Labs Fleece Jacket", "price": "$49.99"},
        {"name": "Sauce Labs Onesie", "price": "$7.99"},
        {"name": "Test.allTheThings() T-Shirt (Red)", "price": "$15.99"}
    ]
    
    # Configuration du navigateur
    BROWSER = "chrome"  # chrome, firefox, edge
    HEADLESS = False
    MAXIMIZE_WINDOW = True