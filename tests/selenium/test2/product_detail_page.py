"""
Page Object pour la page de détails d'un produit
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage  # Fixed import
import time


class ProductDetailPage(BasePage):
    """Page de détails d'un produit"""
    
    # Locators
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DESCRIPTION = (By.CLASS_NAME, "inventory_details_desc")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_details_price")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".inventory_details_img")
    BACK_BUTTON = (By.ID, "back-to-products")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove']")
    
    def is_on_detail_page(self):
        """
        Vérifie qu'on est sur la page de détails
        Attend jusqu'à 10 secondes que la page se charge
        """
        try:
            # Attendre que l'URL contienne "inventory-item"
            WebDriverWait(self.driver, 10).until(
                lambda d: "inventory-item.html" in d.current_url or "?id=" in d.current_url
            )
            
            # Attendre que le nom du produit soit visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.PRODUCT_NAME)
            )
            
            return True
        except Exception as e:
            print(f"❌ Pas sur la page de détails: {e}")
            print(f"   URL actuelle: {self.driver.current_url}")
            return False
    
    def get_product_name(self) -> str:
        """Récupère le nom du produit"""
        return self.get_text(*self.PRODUCT_NAME)
    
    def get_product_description(self) -> str:
        """Récupère la description du produit"""
        return self.get_text(*self.PRODUCT_DESCRIPTION)
    
    def get_product_price(self) -> str:
        """Récupère le prix du produit"""
        return self.get_text(*self.PRODUCT_PRICE)
    
    def is_product_image_visible(self) -> bool:
        """
        Vérifie si l'image du produit est visible
        Version avec debug détaillé
        """
        print("\n🔍 Vérification de l'image du produit...")
        
        try:
            # Attendre que l'image soit dans le DOM
            img = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PRODUCT_IMAGE)
            )
            print(f"✓ Image trouvée dans le DOM")
            
            # Vérifier les propriétés de l'image
            src = img.get_attribute('src')
            print(f"  - src: {src}")
            
            is_displayed = img.is_displayed()
            print(f"  - is_displayed: {is_displayed}")
            
            width = img.size['width']
            height = img.size['height']
            print(f"  - Dimensions: {width}x{height}")
            
            # Attendre que l'image soit visible
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located(self.PRODUCT_IMAGE)
                )
                print(f"✓ Image est visible")
                return True
            except Exception as e:
                print(f"❌ Image pas visible après attente: {e}")
                
                # Essayer de forcer un wait plus long
                time.sleep(2)
                is_visible_now = img.is_displayed()
                print(f"  - Visible après 2s de plus: {is_visible_now}")
                return is_visible_now
                
        except Exception as e:
            print(f"❌ Erreur lors de la recherche de l'image: {e}")
            
            # Afficher le HTML de la page pour debug
            try:
                detail_container = self.driver.find_element(By.CLASS_NAME, "inventory_details_container")
                print(f"\n📄 HTML du conteneur:")
                print(detail_container.get_attribute('innerHTML')[:500])
            except:
                pass
            
            return False
    
    def get_product_image_src(self) -> str:
        """Récupère l'URL de l'image du produit"""
        return self.find_element(*self.PRODUCT_IMAGE).get_attribute('src')
    
    def click_back_button(self):
        """Clique sur le bouton retour avec JavaScript"""
        try:
            back_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.BACK_BUTTON)
            )
            
            # Scroll
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", back_btn)
            time.sleep(0.3)
            
            # Cliquer avec JavaScript
            self.driver.execute_script("arguments[0].click();", back_btn)
            time.sleep(1.5)
            
        except Exception as e:
            print(f"❌ Erreur click_back_button: {e}")
            raise
    
    def back_to_products(self):
        """Retourne à la liste des produits"""
        print("\n🔙 Retour vers la liste des produits...")
        
        try:
            back_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.BACK_BUTTON)
            )
            
            # Scroll vers le bouton
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", back_btn)
            time.sleep(0.3)
            
            # Cliquer avec JavaScript
            self.driver.execute_script("arguments[0].click();", back_btn)
            time.sleep(1.5)
            
            print(f"✓ URL après retour: {self.driver.current_url}")
            
            if "/inventory.html" in self.driver.current_url:
                print("✅ Retour réussi")
            else:
                print(f"⚠️ URL: {self.driver.current_url}")
                
        except Exception as e:
            print(f"❌ Erreur back_to_products: {e}")
            raise
    
    def add_to_cart(self):
        """Ajoute le produit au panier"""
        self.click_element(*self.ADD_TO_CART_BUTTON)
    
    def remove_from_cart(self):
        """Retire le produit du panier"""
        self.click_element(*self.REMOVE_BUTTON)
    
    def is_added_to_cart(self) -> bool:
        """Vérifie si le produit est dans le panier"""
        return self.is_element_present(*self.REMOVE_BUTTON)