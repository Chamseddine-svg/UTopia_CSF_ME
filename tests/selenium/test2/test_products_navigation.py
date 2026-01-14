"""
Tests pour la vérification des produits SauceDemo
Test Selenium 2: Navigation et vérification des produits
"""

import pytest
import time
from selenium.webdriver.common.by import By
from config import Config  # Fixed import


class TestProductVerification:
    """Suite de tests pour la vérification des produits"""
    
    def test_login_all_users(self, driver, login_page):
        """
        Test de connexion pour tous les utilisateurs
        Vérifie que locked_out_user est bloqué et les autres peuvent se connecter
        """
        
        for username in Config.USERS:
            print(f"\n{'='*60}")
            print(f"Test de connexion pour: {username}")
            print(f"{'='*60}")
            
            login_page.navigate()
            time.sleep(0.5)  # Attendre le chargement de la page
            login_page.login(username)
            
            if username == "locked_out_user":
                # Cet utilisateur ne peut pas se connecter
                time.sleep(1)  # Attendre le message d'erreur
                assert login_page.is_error_displayed(), \
                    f"Message d'erreur attendu pour {username}"
                error = login_page.get_error_message()
                print(f"✓ {username}: Bloqué comme prévu")
                print(f"  Message: {error}")
            else:
                # Tous les autres devraient pouvoir se connecter
                # Note: Augmentation du timeout pour performance_glitch_user
                is_successful = login_page.is_login_successful(timeout=10)
                assert is_successful, \
                    f"Connexion échouée pour {username}"
                print(f"✓ {username}: Connexion réussie")
                driver.back()
                time.sleep(0.5)
    
    @pytest.mark.parametrize("username", Config.FUNCTIONAL_USERS)
    def test_complete_product_verification(self, driver, login_page, inventory_page, 
                                          product_detail_page, username):
        """
        Test Selenium 2 - Test complet de vérification des produits
        
        Steps:
        1. Se connecter avec l'utilisateur
        2. Vérifier que tous les produits sont présents
        3. Vérifier les éléments de chaque produit (tolérant aux bugs)
        4. Cliquer sur "Sauce Labs Backpack"
        5. Vérifier la page de détails
        6. Retourner à la liste des produits
        7. Vérifier le nombre total de produits (6)
        """
        
        print(f"\n{'='*70}")
        print(f"TEST COMPLET POUR L'UTILISATEUR: {username}")
        print(f"{'='*70}")
        
        # ===== STEP 1: Se connecter =====
        print(f"\n--- STEP 1: Connexion ---")
        login_page.navigate()
        time.sleep(0.5)
        login_page.login(username)
        
        # Timeout augmenté pour performance_glitch_user
        timeout = 15 if username == "performance_glitch_user" else 10
        assert login_page.is_login_successful(timeout=timeout), \
            f"Connexion échouée pour {username}"
        print(f"✓ Connexion réussie pour {username}")
        
        time.sleep(1)  # Attendre le chargement complet de la page
        
        # ===== STEP 2: Vérifier tous les produits =====
        print(f"\n--- STEP 2: Vérification de la présence de tous les produits ---")
        for expected_product in Config.EXPECTED_PRODUCTS:
            exists = inventory_page.verify_product_exists(
                expected_product['name'], 
                expected_product['price']
            )
            assert exists, \
                f"Produit manquant: {expected_product['name']} - {expected_product['price']}"
            print(f"✓ {expected_product['name']} - {expected_product['price']}")
        
        # ===== STEP 3: Vérifier les éléments de chaque produit =====
        print(f"\n--- STEP 3: Vérification des éléments de chaque produit ---")
        all_products = inventory_page.get_all_products()
        
        for idx, product in enumerate(all_products, 1):
            print(f"\nProduit {idx}/{len(all_products)}: {product['name']}")
            verification = inventory_page.verify_product_elements(product)
            
            # Vérification de l'image - Tolérant pour problem_user et visual_user
            if username not in ["problem_user", "visual_user"]:
                assert verification['has_visible_image'], \
                    f"Image non visible pour {product['name']}"
                assert verification['image_has_src'], \
                    f"Image sans src pour {product['name']}"
                print(f"  ✓ Image visible avec src")
            else:
                print(f"  ⚠️  Images peuvent être cassées (user avec bugs)")
            
            # Vérification du bouton Add to cart
            assert verification['has_add_button'], \
                f"Bouton 'Add to cart' non visible pour {product['name']}"
            assert verification['button_is_enabled'], \
                f"Bouton 'Add to cart' non activé pour {product['name']}"
            print(f"  ✓ Bouton 'Add to cart' présent et activé")
            
            # Vérification du nom cliquable
            assert verification['has_clickable_name'], \
                f"Nom non cliquable pour {product['name']}"
            print(f"  ✓ Nom de produit cliquable")
        
        # ===== STEP 4: Cliquer sur "Sauce Labs Backpack" =====
        print(f"\n--- STEP 4: Navigation vers 'Sauce Labs Backpack' ---")
        inventory_page.click_product_by_name("Sauce Labs Backpack")
        time.sleep(2)  # Attendre la navigation
        print(f"✓ Clic effectué sur 'Sauce Labs Backpack'")
        
        # ===== STEP 5: Vérifier la page de détails =====
        print(f"\n--- STEP 5: Vérification de la page de détails ---")
        assert product_detail_page.is_on_detail_page(), \
            "Pas sur la page de détails du produit"
        print(f"✓ Sur la page de détails du produit")
        
        detail_name = product_detail_page.get_product_name()
        detail_price = product_detail_page.get_product_price()
        
        assert detail_name == "Sauce Labs Backpack", \
            f"Nom incorrect: attendu 'Sauce Labs Backpack', obtenu '{detail_name}'"
        print(f"✓ Nom du produit correct: {detail_name}")
        
        assert detail_price == "$29.99", \
            f"Prix incorrect: attendu '$29.99', obtenu '{detail_price}'"
        print(f"✓ Prix du produit correct: {detail_price}")
        
        assert product_detail_page.is_product_image_visible(), \
            "Image du produit non visible"
        print(f"✓ Image du produit visible")
        
        # ===== STEP 6: Retourner à la liste des produits =====
        print(f"\n--- STEP 6: Retour à la liste des produits ---")
        product_detail_page.back_to_products()
        time.sleep(1)  # Attendre le retour
        
        assert inventory_page.is_on_inventory_page(), \
            "Pas revenu à la page inventaire"
        print(f"✓ Retour réussi à la liste des produits")
        
        # ===== STEP 7: Vérifier le nombre total de produits =====
        print(f"\n--- STEP 7: Vérification du nombre total de produits ---")
        product_count = inventory_page.get_product_count()
        
        assert product_count == 6, \
            f"Nombre de produits incorrect: {product_count} (attendu: 6)"
        print(f"✓ Nombre total de produits: {product_count} ✓")
        
        print(f"\n{'='*70}")
        print(f"✅ TOUS LES TESTS RÉUSSIS POUR {username}")
        print(f"{'='*70}\n")


class TestProductElements:
    """
    Tests spécifiques pour les éléments des produits
    Utilisent standard_user pour éviter les bugs intentionnels
    """
    
    def test_all_products_have_images(self, authenticated_user, inventory_page):
        """Vérifie que tous les produits ont des images visibles"""
        products = inventory_page.get_all_products()
        
        for product in products:
            assert product['image'].is_displayed(), \
                f"Image non visible pour {product['name']}"
            assert product['image'].get_attribute('src'), \
                f"Image sans src pour {product['name']}"
    
    def test_all_products_have_add_to_cart_button(self, authenticated_user, inventory_page):
        """Vérifie que tous les produits ont un bouton Add to cart"""
        products = inventory_page.get_all_products()
        
        for product in products:
            assert product['add_button'].is_displayed(), \
                f"Bouton non visible pour {product['name']}"
            assert product['add_button'].is_enabled(), \
                f"Bouton non activé pour {product['name']}"
    
    def test_all_products_have_clickable_names(self, authenticated_user, inventory_page):
        """Vérifie que tous les produits ont des noms cliquables"""
        products = inventory_page.get_all_products()
        
        for product in products:
            assert product['name_link'].is_displayed(), \
                f"Nom non visible pour {product['name']}"
            assert product['name_link'].is_enabled(), \
                f"Nom non cliquable pour {product['name']}"


class TestProductNavigation:
    """Tests pour la navigation entre produits"""
    
    @pytest.mark.parametrize("product_name,expected_price", [
        ("Sauce Labs Backpack", "$29.99"),
        ("Sauce Labs Bike Light", "$9.99"),
        ("Sauce Labs Fleece Jacket", "$49.99")
    ])
    def test_product_detail_navigation(self, authenticated_user, inventory_page, 
                                      product_detail_page, product_name, expected_price):
        """Teste la navigation vers les détails de différents produits"""
        
        # Naviguer vers le produit
        inventory_page.click_product_by_name(product_name)
        time.sleep(1)
        
        # Vérifier la page de détails
        assert product_detail_page.is_on_detail_page()
        assert product_detail_page.get_product_name() == product_name
        assert product_detail_page.get_product_price() == expected_price
        
        # Retourner à l'inventaire
        product_detail_page.back_to_products()
        time.sleep(0.5)
        assert inventory_page.is_on_inventory_page()


# ============================================================
# TEST TEMPORAIRE DE DEBUG - À SUPPRIMER APRÈS
# ============================================================
def test_debug_product_structure(authenticated_user):
    """Test de debug pour comprendre la structure HTML"""
    driver = authenticated_user
    
    # Attendre le chargement
    time.sleep(2)
    
    # Trouver tous les items
    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    print(f"\n📦 Nombre de produits trouvés: {len(items)}")
    
    # Analyser le premier produit
    if items:
        first_item = items[0]
        print(f"\n🔍 Structure HTML du premier produit:")
        print(first_item.get_attribute('outerHTML')[:800])
        
        # Chercher le nom avec espace
        try:
            name_with_space = first_item.find_element(By.CSS_SELECTOR, ".inventory_item_name ")
            print(f"\n✓ Classe avec espace trouvée: '{name_with_space.text}'")
        except:
            print(f"\n❌ Classe avec espace NON trouvée")
        
        # Chercher le nom sans espace
        try:
            name_without_space = first_item.find_element(By.CSS_SELECTOR, ".inventory_item_name")
            print(f"✓ Classe sans espace trouvée: '{name_without_space.text}'")
        except:
            print(f"❌ Classe sans espace NON trouvée")
        
        # Chercher les liens
        try:
            links = first_item.find_elements(By.TAG_NAME, "a")
            print(f"\n🔗 Liens trouvés dans le produit: {len(links)}")
            for idx, link in enumerate(links):
                print(f"  Lien {idx+1}:")
                print(f"    - id: {link.get_attribute('id')}")
                print(f"    - href: {link.get_attribute('href')}")
                print(f"    - class: {link.get_attribute('class')}")
                try:
                    inner_text = link.find_element(By.CSS_SELECTOR, "div").text
                    print(f"    - texte intérieur: {inner_text}")
                except:
                    print(f"    - texte: {link.text}")
        except Exception as e:
            print(f"❌ Erreur lors de la recherche des liens: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])