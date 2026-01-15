from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import sys
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

CHROME_PORTABLE_PATH = r'C:\Chrome_Sources\chrome-win64\chrome.exe'
CHROME_DRIVER_PATH = r'C:\Chrome_Sources\chromedriver-win64\chromedriver.exe'

# Charger l'URL depuis le fichier JSON
with open('DataProducts.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    URL = config.get('url', "https://www.saucedemo.com/")

# Charger les locators depuis le fichier JSON
with open('locators.json', 'r', encoding='utf-8') as f:
    LOCATORS = json.load(f)['saucedemo_locators']

def get_locator(section, locator_name):
    """
    Récupère un locator depuis le fichier de configuration
    
    Args:
        section (str): La section (login_page, inventory_page, product_detail_page)
        locator_name (str): Le nom du locator
    
    Returns:
        tuple: (By method, locator value)
    """
    try:
        locator_config = LOCATORS[section][locator_name]
        by_method = getattr(By, locator_config['by'])
        return (by_method, locator_config['value'])
    except KeyError as e:
        print(f"⚠️ Locator non trouvé: {section}/{locator_name}")
        raise

UNITTEST = False


def check_single_product(driver, product_data):
    """
    Fonction qui vérifie un seul produit dans le catalogue avec les requirements suivants:
    1. Chercher le produit par son nom
    2. Vérifier que les données correspondent au JSON (nom, prix)
    3. Vérifier sa présence avec ses propriétés (image, bouton "Add to cart", nom cliquable)
    4. Cliquer sur le produit et vérifier la page de détails
    5. Retourner à la liste des produits
    
    Args:
        driver: Chrome driver
        product_data (dict): Dictionnaire contenant le nom et le prix du produit
                           Ex: {"name": "Sauce Labs Backpack", "price_label": "$29.99"}
    
    Returns:
        dict: Résumé des résultats de vérification pour ce produit
    """
    product_name = product_data.get("name", "")
    expected_price = product_data.get("price_label", "")
    
    result = {
        "product_name": product_name,
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    try:
        # S'assurer que nous sommes sur la page d'inventaire
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(get_locator('inventory_page', 'inventory_container')))
        
        # Récupérer tous les produits
        product_items = driver.find_elements(*get_locator('inventory_page', 'product_items'))
        
        print(f"\n🔍 Vérification du produit: {product_name}")
        
        # Chercher le produit par son nom
        product_element = None
        for item in product_items:
            try:
                name_elem = item.find_element(*get_locator('inventory_page', 'product_name'))
                if product_name in name_elem.text:
                    product_element = item
                    break
            except:
                continue
        
        if not product_element:
            result["total_tests"] += 1
            result["failed"] += 1
            result["details"].append(f"❌ Produit '{product_name}' non trouvé")
            print(f"  ❌ Produit '{product_name}' non trouvé")
            return result
        
        print(f"  ✅ Produit '{product_name}' trouvé dans la page")
        
        # Vérifier le prix
        result["total_tests"] += 1
        try:
            price_elem = product_element.find_element(*get_locator('inventory_page', 'product_price'))
            actual_price = price_elem.text
            
            if actual_price == expected_price:
                print(f"  ✅ Prix correct: {actual_price}")
                result["passed"] += 1
                result["details"].append(f"✅ Prix correct: {actual_price}")
            else:
                print(f"  ❌ Prix incorrect: {actual_price} au lieu de {expected_price}")
                result["failed"] += 1
                result["details"].append(f"❌ Prix incorrect: {actual_price} vs {expected_price}")
        except Exception as price_error:
            print(f"  ❌ Impossible de vérifier le prix: {str(price_error)}")
            result["failed"] += 1
            result["details"].append(f"❌ Erreur lors de la vérification du prix")
        
        # Vérifier l'image visible
        result["total_tests"] += 1
        try:
            # Attendre que l'image soit visible avec un timeout augmenté (5 secondes)
            img = WebDriverWait(product_element, 5).until(
                EC.visibility_of_element_located(get_locator('inventory_page', 'product_image'))
            )
            print(f"  ✅ Image visible")
            result["passed"] += 1
            result["details"].append(f"✅ Image visible")
        except TimeoutException:
            print(f"  ❌ Image non visible après 5 secondes")
            result["failed"] += 1
            result["details"].append(f"❌ Image non visible (timeout)")
        except:
            print(f"  ❌ Image non trouvée")
            result["failed"] += 1
            result["details"].append(f"❌ Image non trouvée")
        
        # Vérifier le bouton "Add to cart"
        result["total_tests"] += 1
        try:
            add_to_cart_btn = product_element.find_element(*get_locator('inventory_page', 'add_to_cart_button'))
            if add_to_cart_btn.is_displayed():
                print(f"  ✅ Bouton 'Add to cart' présent")
                result["passed"] += 1
                result["details"].append(f"✅ Bouton 'Add to cart' présent")
            else:
                print(f"  ❌ Bouton 'Add to cart' non visible")
                result["failed"] += 1
                result["details"].append(f"❌ Bouton 'Add to cart' non visible")
        except:
            print(f"  ❌ Bouton 'Add to cart' non trouvé")
            result["failed"] += 1
            result["details"].append(f"❌ Bouton 'Add to cart' non trouvé")
        
        # Tester que le nom du produit est réellement cliquable
        result["total_tests"] += 1
        try:
            product_name_elem = product_element.find_element(*get_locator('inventory_page', 'product_name'))
            
            # Vérifier que l'élément est visible et peut être cliqué
            if product_name_elem.is_displayed() and product_name_elem.is_enabled():
                # Cliquer sur le nom du produit
                product_name_elem.click()
                
                # Vérifier que la page de détails a chargé
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located(get_locator('product_detail_page', 'inventory_details_container')))
                    detail_name = driver.find_element(*get_locator('product_detail_page', 'product_detail_name'))
                    
                    # Vérifier que c'est le bon produit
                    if product_name in detail_name.text:
                        print(f"  ✅ Nom du produit cliquable - Page de détails correcte")
                        result["passed"] += 1
                        result["details"].append(f"✅ Page de détails correcte")
                    else:
                        print(f"  ❌ Mauvaise page de détails - reçu '{detail_name.text}'")
                        result["failed"] += 1
                        result["details"].append(f"❌ Mauvaise page de détails")
                except TimeoutException:
                    print(f"  ❌ Page de détails ne s'est pas chargée")
                    result["failed"] += 1
                    result["details"].append(f"❌ Page de détails ne s'est pas chargée")
                
                # Retourner à la liste des produits
                try:
                    back_button = driver.find_element(*get_locator('product_detail_page', 'back_to_products_button'))
                    back_button.click()
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located(get_locator('inventory_page', 'inventory_container')))
                    time.sleep(0.5)
                except Exception as back_error:
                    print(f"  ⚠️ Erreur lors du retour: {str(back_error)}")
            else:
                print(f"  ❌ Nom du produit non cliquable ou non visible")
                result["failed"] += 1
                result["details"].append(f"❌ Nom du produit non cliquable")
        except Exception as click_error:
            print(f"  ❌ Erreur lors du test de clic: {str(click_error)}")
            result["failed"] += 1
            result["details"].append(f"❌ Erreur lors du test de clic")
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")
        result["details"].append(f"❌ Erreur générale: {str(e)}")
    
    return result


def check_products_catalog(driver, products_list):
    """
    Fonction globale qui vérifie tous les produits du catalogue

    Vérifie aussi le nombre total de produits
    
    Args:
        driver: Chrome driver
        products_list (list): Liste des dictionnaires de produits à vérifier
                            Ex: [{"name": "Sauce Labs Backpack", "price_label": "$29.99"}, ...]
    
    Returns:
        dict: Résumé complet des résultats pour tous les produits
    """
    global_results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "product_results": [],
        "details": []
    }
    
    try:
        # S'assurer que nous sommes sur la page d'inventaire
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(get_locator('inventory_page', 'inventory_container')))
        print("\n✅ Page d'inventaire chargée")
        
        # Vérifier le nombre total de produits (6)
        print("\n" + "="*60)
        print("ÉTAPE 1: Vérifier le nombre total de produits")
        print("="*60)
        
        product_items = driver.find_elements(*get_locator('inventory_page', 'product_items'))
        total_products = len(product_items)
        print(f"Nombre de produits trouvés: {total_products}")
        
        global_results["total_tests"] += 1
        if total_products == 6:
            print("✅ Le nombre de produits est correct (6)")
            global_results["passed"] += 1
            global_results["details"].append(f"✅ Nombre de produits: {total_products}/6")
        else:
            print(f"❌ Le nombre de produits est incorrect: {total_products} au lieu de 6")
            global_results["failed"] += 1
            global_results["details"].append(f"❌ Nombre de produits: {total_products} au lieu de 6")
        
       
        
        # Vérifier le produit spécial "Sauce Labs Backpack"
        print("\n" + "="*60)
        print("ÉTAPE 3: Vérification spéciale - Sauce Labs Backpack")
        print("="*60)
        
        global_results["total_tests"] += 1
        try:
            product_items = driver.find_elements(*get_locator('inventory_page', 'product_items'))
            backpack_product = None
            for item in product_items:
                try:
                    name_elem = item.find_element(*get_locator('inventory_page', 'product_name'))
                    if "Sauce Labs Backpack" in name_elem.text:
                        backpack_product = item
                        break
                except:
                    continue
            
            if backpack_product:
                backpack_name = backpack_product.find_element(*get_locator('inventory_page', 'product_name'))
                backpack_name.click()
                print("✅ Clic sur 'Sauce Labs Backpack' effectué")
                
                # Vérifier la page de détails
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(get_locator('product_detail_page', 'inventory_details_container')))
                
                # Vérifier le titre du produit
                try:
                    detail_title = driver.find_element(*get_locator('product_detail_page', 'product_detail_name'))
                    print(f"  📄 Titre de la page de détails: {detail_title.text}")
                    global_results["passed"] += 1
                except:
                    print("  ❌ Impossible de vérifier le titre")
                    global_results["failed"] += 1
                
                # Prendre une capture d'écran de la page de détails
                try:
                    import os
                    reports_dir = "reports"
                    if not os.path.exists(reports_dir):
                        os.makedirs(reports_dir)
                    
                    filename = os.path.join(reports_dir, f"backpack_detail_{time.strftime('%H%M%S')}.png")
                    driver.save_screenshot(filename)
                    print(f"  📸 Capture d'écran sauvegardée: {filename}")
                except:
                    pass
                
                # Retourner à la liste des produits
                global_results["total_tests"] += 1
                try:
                    back_button = driver.find_element(*get_locator('product_detail_page', 'back_to_products_button'))
                    back_button.click()
                    print("✅ Retour à la liste des produits effectué")
                    
                    # Vérifier qu'on est revenu à la page d'inventaire
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located(get_locator('inventory_page', 'inventory_container')))
                    print("✅ Vérification: nous sommes bien revenu à la liste des produits")
                    global_results["passed"] += 1
                except Exception as e:
                    print(f"❌ Erreur lors du retour: {str(e)}")
                    global_results["failed"] += 1
            else:
                print("❌ Produit 'Sauce Labs Backpack' non trouvé")
                global_results["failed"] += 1
        except Exception as e:
            print(f"❌ Erreur lors de la vérification de la page de détails: {str(e)}")
            global_results["failed"] += 1
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")
        global_results["details"].append(f"❌ Erreur générale: {str(e)}")
    
    # Afficher le résumé
  
   
    print("="*60)
    print(f"Total de vérifications: {global_results['total_tests']}")
    print(f"✅ Réussi: {global_results['passed']}")
    print(f"❌ Échoué: {global_results['failed']}")
    print(f"Taux de réussite: {(global_results['passed']/global_results['total_tests']*100):.1f}%" if global_results['total_tests'] > 0 else "N/A")
    
    return global_results

