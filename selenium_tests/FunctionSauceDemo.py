from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

CHROME_PORTABLE_PATH = r'C:\Chrome_Sources\chrome-win64\chrome.exe'
CHROME_DRIVER_PATH = r'C:\Chrome_Sources\chromedriver-win64\chromedriver.exe'
URL = "https://www.saucedemo.com/"
UNITTEST = False
def OpenChrome(chromedriver_path,chrome_portable_path):
 
    # Configurer les options de Chrome
    chrome_options = Options()
    chrome_options.binary_location = chrome_portable_path
    
    prefs = {
    # Désactiver le gestionnaire de mots de passe
    "profile.password_manager_enabled": False,
    "credentials_enable_service": False
    }
    chrome_options.add_experimental_option("prefs",prefs)
    # chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-default-browser-check")


    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service,options=chrome_options)  # Assurez-vous d'avoir chromedriver installé

    return driver

def CloseChrome(driver):
    driver.quit()

def check_connection_user(driver,username, password, expected_result=True,driverQuit=False):
    """
    Fonction qui teste une connexion avec un username et password
    et vérifie si le résultat correspond à ce qui est attendu
    
    Args:
        driver (str) : chrome driver onglet
        username (str): Nom d'utilisateur
        password (str): Mot de passe
        expected_result (str): True ou False (connected or not connected)
        driverQuit (bool): Si True, ferme le driver à la fin
    
    Returns:
        bool: True si le résultat correspond à l'attendu, False sinon
    """
    URL = "https://www.saucedemo.com/"
    TtimoutOutError = False
    # Créer une instance du navigateur (Chrome)
    # print("line 21")
   
    try:
        # Accéder au site
        driver.get(URL)
        print(f"Test avec: {username}")
        print("Page chargée :", driver.title)
        
        # Remplir le formulaire de connexion
        # Trouver le champ username et saisir les données
        username_field = driver.find_element(By.ID, "user-name")
        username_field.clear()
        username_field.send_keys(username)
        
        # Trouver le champ password et saisir les données
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        
        # Soumettre le formulaire
        login_button = driver.find_element(By.ID, "login-button")
        start = time.time()
        login_button.click()
        
        WebDriverWait(driver,2).until(EC.presence_of_element_located((By.ID,"inventory_container")))

        elapsed = time.time() - start
        if (elapsed >= 2.0):
            raise TimeoutException('Maximum 2 secondes are accepted for connection')
        print("elapsedtime = ",elapsed)
        # Vérifier la connexion réussie
        current_url = driver.current_url
        if "inventory" in current_url:
            print("✅ Connexion réussie!")
            print("Page actuelle :", driver.current_url)
            
            # Afficher le titre de la page produits
            title = driver.find_element(By.CLASS_NAME, "title")
            print("Titre de la page :", title.text)
            
            # Prendre une capture d'écran
            try:
                filename = f"saucedemo_{username}_{time.strftime('%H%M%S')}.png"
                driver.save_screenshot(filename)
                print(f"📸 Capture d'écran sauvegardée: {filename}")
            except Exception as screenshot_error:
                print(f"⚠️ Erreur lors de la capture d'écran: {str(screenshot_error)}")
            
            # Vérifier si le résultat correspond à l'attendu
            if expected_result == True:
                print("✅ Résultat attendu atteint: utilisateur connecté")
                return True
            else:
                print("❌ Résultat inattendu: L'utilisateur est connecté")
                return False
        else:
            print("❌ Échec de la connexion")
            
            # Vérifier si le résultat correspond à l'attendu
            if expected_result ==False:
                print("✅ Résultat attendu atteint: utilisateur non connecté")
                return True
            else:
                print("❌ Résultat inattendu: utilisateur non connecté mais connecté attendu")
                return False
                
    except TimeoutException as timeout:
        print("Un time out erreur est survenue :", timeout.__class__)
        TtimoutOutError= True
        return False
    except Exception as e:
        print("Une erreur est survenue :", str(e))
        return False
        
    finally:
        print("-" * 50)
        if driverQuit:
            try:
                driver.quit()
            except:
                pass


def check_products_catalog(driver, products_to_verify):
    """
    Fonction qui vérifie les produits dans le catalogue avec les requirements suivants:
    1. Vérifier la présence de tous les produits avec leurs prix
    2. Vérifier que chaque produit a: une image, un bouton "Add to cart", un nom cliquable
    3. Cliquer sur un produit spécifique et vérifier la page de détails
    4. Retourner à la liste et vérifier le nombre total de produits (6)
    
    Args:
        driver: Chrome driver
        products_to_verify: Liste des produits à vérifier depuis le JSON
    
    Returns:
        dict: Résumé des résultats de vérification
    """
    results = {
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    try:
        # S'assurer que nous sommes sur la page d'inventaire
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "inventory_container")))
        print("\n✅ Page d'inventaire chargée")
        
        # 7. Vérifier le nombre total de produits (6)
        print("\n" + "="*60)
        print("ÉTAPE 1: Vérifier le nombre total de produits")
        print("="*60)
        
        product_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        total_products = len(product_items)
        print(f"Nombre de produits trouvés: {total_products}")
        
        results["total_tests"] += 1
        if total_products == 6:
            print("✅ Le nombre de produits est correct (6)")
            results["passed"] += 1
            results["details"].append(f"✅ Nombre de produits: {total_products}/6")
        else:
            print(f"❌ Le nombre de produits est incorrect: {total_products} au lieu de 6")
            results["failed"] += 1
            results["details"].append(f"❌ Nombre de produits: {total_products} au lieu de 6")
        
        # 1 & 2. Vérifier la présence des produits et leurs propriétés
        print("\n" + "="*60)
        print("ÉTAPE 2: Vérifier la présence et les propriétés des produits")
        print("="*60)
        
        for product_data in products_to_verify:
            product_name = product_data["name"]
            expected_price = product_data["price_label"]
            
            print(f"\n🔍 Vérification du produit: {product_name}")
            
            # Chercher le produit par son nom
            try:
                # Chercher l'élément produit contenant le nom du produit
                product_element = None
                for item in product_items:
                    try:
                        name_elem = item.find_element(By.CLASS_NAME, "inventory_item_name")
                        if product_name in name_elem.text:
                            product_element = item
                            break
                    except:
                        continue
                
                if not product_element:
                    results["total_tests"] += 1
                    results["failed"] += 1
                    results["details"].append(f"❌ {product_name}: Produit non trouvé")
                    print(f"  ❌ Produit '{product_name}' non trouvé")
                    continue
                
                # Vérifier le prix
                price_elem = product_element.find_element(By.CLASS_NAME, "inventory_item_price")
                actual_price = price_elem.text
                
                results["total_tests"] += 1
                if actual_price == expected_price:
                    print(f"  ✅ Prix correct: {actual_price}")
                    results["passed"] += 1
                else:
                    print(f"  ❌ Prix incorrect: {actual_price} au lieu de {expected_price}")
                    results["failed"] += 1
                
                # Vérifier l'image visible
                results["total_tests"] += 1
                try:
                    img = product_element.find_element(By.TAG_NAME, "img")
                    if img.is_displayed():
                        print(f"  ✅ Image visible")
                        results["passed"] += 1
                    else:
                        print(f"  ❌ Image non visible")
                        results["failed"] += 1
                except:
                    print(f"  ❌ Image non trouvée")
                    results["failed"] += 1
                
                # Vérifier le bouton "Add to cart"
                results["total_tests"] += 1
                try:
                    add_to_cart_btn = product_element.find_element(By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
                    if add_to_cart_btn.is_displayed():
                        print(f"  ✅ Bouton 'Add to cart' présent")
                        results["passed"] += 1
                    else:
                        print(f"  ❌ Bouton 'Add to cart' non visible")
                        results["failed"] += 1
                except:
                    print(f"  ❌ Bouton 'Add to cart' non trouvé")
                    results["failed"] += 1
                
                # Tester que le nom du produit est réellement cliquable
                results["total_tests"] += 1
                try:
                    product_name_elem = product_element.find_element(By.CLASS_NAME, "inventory_item_name")
                    
                    # Vérifier que l'élément est visible et peut être cliqué
                    if product_name_elem.is_displayed() and product_name_elem.is_enabled():
                        # Cliquer sur le nom du produit
                        product_name_elem.click()
                        
                        # Vérifier que la page de détails a chargé
                        try:
                            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_details")))
                            detail_name = driver.find_element(By.CLASS_NAME, "inventory_details_name")
                            
                            # Vérifier que c'est le bon produit
                            if product_name in detail_name.text:
                                print(f"  ✅ Nom du produit cliquable - Page de détails correcte")
                                results["passed"] += 1
                            else:
                                print(f"  ❌ Mauvaise page de détails - reçu '{detail_name.text}'")
                                results["failed"] += 1
                        except TimeoutException:
                            print(f"  ❌ Page de détails ne s'est pas chargée")
                            results["failed"] += 1
                        
                        # Retourner à la liste des produits
                        try:
                            back_button = driver.find_element(By.ID, "back-to-products")
                            back_button.click()
                            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "inventory_container")))
                            # Rafraîchir la liste des produits
                            product_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
                            time.sleep(0.5)
                        except Exception as back_error:
                            print(f"  ⚠️ Erreur lors du retour: {str(back_error)}")
                    else:
                        print(f"  ❌ Nom du produit non cliquable ou non visible")
                        results["failed"] += 1
                except Exception as click_error:
                    print(f"  ❌ Erreur lors du test de clic: {str(click_error)}")
                    results["failed"] += 1
                
            except Exception as e:
                print(f"  ❌ Erreur lors de la vérification: {str(e)}")
                results["total_tests"] += 1
                results["failed"] += 1
        
        # 3 & 4 & 5 & 6. Cliquer sur "Sauce Labs Backpack" et vérifier la page de détails
        print("\n" + "="*60)
        print("ÉTAPE 3: Cliquer sur 'Sauce Labs Backpack' et vérifier la page de détails")
        print("="*60)
        
        results["total_tests"] += 1
        try:
            # Trouver et cliquer sur le produit "Sauce Labs Backpack"
            backpack_product = None
            for item in product_items:
                try:
                    name_elem = item.find_element(By.CLASS_NAME, "inventory_item_name")
                    if "Sauce Labs Backpack" in name_elem.text:
                        backpack_product = item
                        break
                except:
                    continue
            
            if backpack_product:
                backpack_name = backpack_product.find_element(By.CLASS_NAME, "inventory_item_name")
                backpack_name.click()
                print("✅ Clic sur 'Sauce Labs Backpack' effectué")
                
                # Vérifier la page de détails
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_details")))
                
                # Vérifier le titre du produit
                try:
                    detail_title = driver.find_element(By.CLASS_NAME, "inventory_details_name")
                    print(f"  📄 Titre de la page de détails: {detail_title.text}")
                    results["passed"] += 1
                except:
                    print("  ❌ Impossible de vérifier le titre")
                    results["failed"] += 1
                
                # Prendre une capture d'écran de la page de détails
                try:
                    filename = f"backpack_detail_{time.strftime('%H%M%S')}.png"
                    driver.save_screenshot(filename)
                    print(f"  📸 Capture d'écran sauvegardée: {filename}")
                except:
                    pass
                
                # 6. Retourner à la liste des produits
                results["total_tests"] += 1
                try:
                    back_button = driver.find_element(By.ID, "back-to-products")
                    back_button.click()
                    print("✅ Retour à la liste des produits effectué")
                    
                    # Vérifier qu'on est revenu à la page d'inventaire
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "inventory_container")))
                    print("✅ Vérification: nous sommes bien revenu à la liste des produits")
                    results["passed"] += 1
                except Exception as e:
                    print(f"❌ Erreur lors du retour: {str(e)}")
                    results["failed"] += 1
            else:
                print("❌ Produit 'Sauce Labs Backpack' non trouvé")
                results["failed"] += 1
        except Exception as e:
            print(f"❌ Erreur lors de la vérification de la page de détails: {str(e)}")
            results["failed"] += 1
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")
        results["details"].append(f"❌ Erreur générale: {str(e)}")
    
    # Afficher le résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    print(f"Total de vérifications: {results['total_tests']}")
    print(f"✅ Réussi: {results['passed']}")
    print(f"❌ Échoué: {results['failed']}")
    print(f"Taux de réussite: {(results['passed']/results['total_tests']*100):.1f}%" if results['total_tests'] > 0 else "N/A")
    
    return results

