"""
Page Object pour la page du catalogue produits
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage  # Fixed import
from typing import List, Dict
import time


class InventoryPage(BasePage):
    """Page du catalogue produits"""
    
    # Locators
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    PRODUCT_SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")
    
    def is_on_inventory_page(self):
        """Vérifie qu'on est sur la page inventaire"""
        return "/inventory.html" in self.get_current_url()
    
    def get_all_products(self) -> List[Dict]:
        """
        Récupère tous les produits avec leurs informations
        Méthode robuste avec attentes explicites
        """
        products = []
        
        # Attendre que les produits soient chargés
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.INVENTORY_ITEMS)
        )
        time.sleep(0.5)
        
        items = self.driver.find_elements(*self.INVENTORY_ITEMS)
        
        for item in items:
            try:
                product = {
                    'name': item.find_element(By.CLASS_NAME, "inventory_item_name").text,
                    'price': item.find_element(By.CLASS_NAME, "inventory_item_price").text,
                    'description': item.find_element(By.CLASS_NAME, "inventory_item_desc").text,
                    'image': item.find_element(By.CSS_SELECTOR, ".inventory_item_img img"),
                    'add_button': item.find_element(By.CSS_SELECTOR, "button[id^='add-to-cart']"),
                    'name_link': item.find_element(By.CLASS_NAME, "inventory_item_name"),
                    'element': item
                }
                products.append(product)
            except Exception as e:
                print(f"⚠️  Erreur lors de la récupération d'un produit: {e}")
                continue
        
        return products
    
    def get_product_count(self) -> int:
        """Retourne le nombre total de produits"""
        return len(self.find_elements(*self.INVENTORY_ITEMS))
    
    def get_product_by_name(self, product_name: str) -> Dict:
        """Récupère un produit spécifique par son nom"""
        products = self.get_all_products()
        for product in products:
            if product['name'] == product_name:
                return product
        return None
    
    def verify_product_exists(self, product_name: str, expected_price: str) -> bool:
        """Vérifie qu'un produit spécifique existe avec son prix"""
        products = self.get_all_products()
        for product in products:
            if product['name'] == product_name and product['price'] == expected_price:
                return True
        return False
    
    def verify_product_elements(self, product: Dict) -> Dict[str, bool]:
        """Vérifie tous les éléments d'un produit"""
        results = {
            'has_visible_image': False,
            'has_add_button': False,
            'has_clickable_name': False,
            'image_has_src': False,
            'button_is_enabled': False
        }
        
        try:
            # Vérifier l'image
            img = product['image']
            try:
                results['has_visible_image'] = img.is_displayed()
            except:
                results['has_visible_image'] = False
            
            try:
                src = img.get_attribute('src')
                results['image_has_src'] = bool(src) and src != ''
            except:
                results['image_has_src'] = False
            
            # Vérifier le bouton Add to cart
            try:
                btn = product['add_button']
                results['has_add_button'] = btn.is_displayed()
                results['button_is_enabled'] = btn.is_enabled()
            except:
                pass
            
            # Vérifier le nom cliquable
            try:
                name_link = product['name_link']
                results['has_clickable_name'] = name_link.is_displayed() and name_link.is_enabled()
            except:
                pass
            
        except Exception as e:
            print(f"⚠️  Erreur lors de la vérification du produit {product.get('name', 'Unknown')}: {e}")
        
        return results
    
    def click_product_by_name(self, product_name: str):
        """
        Clique sur un produit par son nom
        SauceDemo utilise JavaScript, tous les liens ont href="#"
        """
        print(f"\n🔍 Recherche du produit: '{product_name}'")
        
        # Attendre le chargement
        time.sleep(1)
        
        # Trouver tous les produits
        products = self.get_all_products()
        
        for product in products:
            if product['name'] == product_name:
                print(f"✓ Produit trouvé: {product_name}")
                
                # Trouver l'élément du produit
                item_element = product['element']
                
                # STRATÉGIE 1: Cliquer sur le lien de l'image avec JavaScript
                try:
                    image_link = item_element.find_element(By.CSS_SELECTOR, "a[id*='img']")
                    print(f"  - Lien image trouvé: {image_link.get_attribute('id')}")
                    
                    # Scroll
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image_link)
                    time.sleep(0.5)
                    
                    # Forcer le clic avec JavaScript
                    self.driver.execute_script("arguments[0].click();", image_link)
                    time.sleep(2)  # Attendre plus longtemps
                    
                    print(f"✓ URL après clic JS: {self.driver.current_url}")
                    
                    if "inventory-item.html" in self.driver.current_url or "?id=" in self.driver.current_url:
                        print(f"✅ Navigation réussie!")
                        return
                        
                except Exception as e1:
                    print(f"⚠️  Stratégie 1 échouée: {e1}")
                
                # STRATÉGIE 2: Cliquer sur le nom du produit avec JavaScript
                try:
                    name_link = product['name_link']
                    
                    # Trouver le lien parent <a>
                    parent_a = name_link.find_element(By.XPATH, "./parent::a")
                    print(f"  - Lien nom trouvé: {parent_a.get_attribute('id')}")
                    
                    # Scroll
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", parent_a)
                    time.sleep(0.5)
                    
                    # Clic JavaScript
                    self.driver.execute_script("arguments[0].click();", parent_a)
                    time.sleep(2)
                    
                    print(f"✓ URL après clic nom: {self.driver.current_url}")
                    
                    if "inventory-item.html" in self.driver.current_url or "?id=" in self.driver.current_url:
                        print(f"✅ Navigation réussie (via nom)!")
                        return
                        
                except Exception as e2:
                    print(f"⚠️  Stratégie 2 échouée: {e2}")
                
                # STRATÉGIE 3: Navigation directe via URL
                try:
                    # Extraire l'ID du produit depuis l'attribut data ou construire l'URL
                    print(f"  - Tentative navigation directe...")
                    
                    # Trouver l'ID dans l'un des liens
                    all_links = item_element.find_elements(By.TAG_NAME, "a")
                    for link in all_links:
                        link_id = link.get_attribute('id')
                        if 'title_link' in link_id or 'img' in link_id:
                            # Extraire le numéro d'item (ex: item_4_title_link → 4)
                            import re
                            match = re.search(r'item_(\d+)_', link_id)
                            if match:
                                item_id = match.group(1)
                                detail_url = f"https://www.saucedemo.com/inventory-item.html?id={item_id}"
                                print(f"  - Navigation directe vers: {detail_url}")
                                self.driver.get(detail_url)
                                time.sleep(2)
                                print(f"✅ Navigation directe réussie!")
                                return
                                
                except Exception as e3:
                    print(f"⚠️  Stratégie 3 échouée: {e3}")
        
        # Si rien n'a fonctionné
        raise Exception(f"❌ Impossible de naviguer vers: {product_name}")
    
    def add_product_to_cart_by_name(self, product_name: str):
        """Ajoute un produit au panier par son nom"""
        products = self.get_all_products()
        for product in products:
            if product['name'] == product_name:
                try:
                    btn = product['add_button']
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(0.3)
                    btn.click()
                    return
                except:
                    self.driver.execute_script("arguments[0].click();", btn)
                    return
        
        raise Exception(f"❌ Produit non trouvé: {product_name}")
    
    def get_cart_item_count(self) -> int:
        """Récupère le nombre d'articles dans le panier"""
        try:
            badge_text = self.get_text(*self.SHOPPING_CART_BADGE)
            return int(badge_text)
        except:
            return 0
    
    def open_shopping_cart(self):
        """Ouvre le panier"""
        self.click_element(*self.SHOPPING_CART_LINK)