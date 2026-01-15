"""
Fonctions Selenium pour les tests SauceDemo
Auteur: Automatisé
Date: 2024-01-12
Description: Fonctions pour exécuter les tests de connexion
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import time
import os

# ==============================================
# CONSTANTES DE CONFIGURATION
# ==============================================

CHROME_PORTABLE_PATH = r'C:\Chrome_Sources\chrome-win64\chrome.exe'
CHROME_DRIVER_PATH = r'C:\Chrome_Sources\chromedriver-win64\chromedriver.exe'
DEFAULT_TIMEOUT = 10

# ==============================================
# FONCTIONS DE GESTION DES LOCATORS
# ==============================================

def charger_locators(fichier="Locatorss.json"):
    """Charge les locators depuis le fichier JSON"""
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier {fichier} non trouvé")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON dans {fichier}: {e}")
        return None

def trouver_element(driver, locators_data, element_key, parent=None):
    """
    Trouve un élément en utilisant les locators du JSON
    
    Args:
        driver: Instance Selenium
        locators_data: Données des locators chargées
        element_key: Clé de l'élément (ex: 'username')
        parent: Élément parent (optionnel)
    
    Returns:
        WebElement: Élément trouvé ou None
    """
    if not locators_data:
        print(f"❌ Locators non chargés")
        return None
    
    # Chercher dans la page de login
    page = "login_page"
    
    # Vérifier la structure des locators
    if "saucedemo" not in locators_data:
        print(f"❌ Clé 'saucedemo' non trouvée dans les locators")
        return None
    
    if page not in locators_data["saucedemo"]:
        print(f"❌ Page '{page}' non trouvée dans les locators")
        return None
    
    if element_key not in locators_data["saucedemo"][page]:
        print(f"❌ Élément '{element_key}' non trouvé dans {page}")
        print(f"   Clés disponibles: {list(locators_data['saucedemo'][page].keys())}")
        return None
    
    element_info = locators_data["saucedemo"][page][element_key]
    
    # Récupérer les valeurs
    by_method = element_info.get("by", "").lower()
    selector = element_info.get("selector", "")
    
    if not selector:
        print(f"❌ Selector vide pour l'élément '{element_key}'")
        return None
    
    # Convertir la méthode de localisation
    by = None
    if by_method == "id":
        by = By.ID
    elif by_method == "class":
        by = By.CLASS_NAME
    elif by_method == "css":
        by = By.CSS_SELECTOR
    elif by_method == "xpath":
        by = By.XPATH
    elif by_method == "name":
        by = By.NAME
    else:
        print(f"❌ Méthode de localisation inconnue: {by_method}")
        return None
    
    try:
        if parent:
            return parent.find_element(by, selector)
        else:
            return driver.find_element(by, selector)
    except Exception as e:
        print(f"❌ Impossible de trouver l'élément '{element_key}' avec {by_method}='{selector}': {e}")
        return None

# ==============================================
# FONCTIONS PRINCIPALES DE TEST
# ==============================================

def ouvrir_chrome(use_portable=False):
    """
    Ouvre un navigateur Chrome
    
    Args:
        use_portable (bool): True pour utiliser Chrome portable
    
    Returns:
        webdriver.Chrome: Instance du driver
    """
    if use_portable and os.path.exists(CHROME_PORTABLE_PATH) and os.path.exists(CHROME_DRIVER_PATH):
        try:
            chrome_options = Options()
            chrome_options.binary_location = CHROME_PORTABLE_PATH
            
            prefs = {
                "profile.password_manager_enabled": False,
                "credentials_enable_service": False
            }
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-extensions")
            
            service = Service(CHROME_DRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome portable ouvert")
        except Exception as e:
            print(f"⚠️  Erreur Chrome portable: {e}")
            print("🔧 Utilisation de Chrome système")
            driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome()
    
    driver.maximize_window()
    return driver

def fermer_chrome(driver):
    """Ferme le navigateur Chrome"""
    if driver:
        driver.quit()
        print("🔴 Navigateur fermé")

def naviguer_vers_url(driver, url):
    """
    Navigue vers une URL
    
    Args:
        driver: Instance Selenium
        url: URL à visiter
    
    Returns:
        str: Titre de la page
    """
    driver.get(url)
    titre = driver.title
    print(f"🌐 Navigation: {url}")
    print(f"📄 Titre: {titre}")
    return titre

def remplir_formulaire_connexion(driver, locators_data, username, password):
    """
    Remplit le formulaire de connexion
    
    Args:
        driver: Instance Selenium
        locators_data: Locators chargés
        username: Nom d'utilisateur
        password: Mot de passe
    
    Returns:
        bool: True si réussi
    """
    try:
        # Trouver les éléments
        champ_user = trouver_element(driver, locators_data, "username")
        champ_pass = trouver_element(driver, locators_data, "password")
        bouton_login = trouver_element(driver, locators_data, "login_button")
        
        if not all([champ_user, champ_pass, bouton_login]):
            print("❌ Impossible de trouver tous les éléments du formulaire")
            return False
        
        # Remplir le formulaire
        champ_user.clear()
        champ_pass.clear()
        
        champ_user.send_keys(username)
        champ_pass.send_keys(password)
        
        bouton_login.click()
        print(f"✅ Formulaire rempli: {username} / {'*' * len(password) if password else '(vide)'}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du remplissage du formulaire: {e}")
        return False

def verifier_message_erreur(driver, locators_data, message_attendu):
    """
    Vérifie le message d'erreur
    
    Args:
        driver: Instance Selenium
        locators_data: Locators chargés
        message_attendu: Message attendu
    
    Returns:
        tuple: (bool succès, str message_obtenu)
    """
    try:
        # Attendre l'apparition du message d'erreur
        conteneur = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))
        )
        
        # Essayer de trouver le message spécifique
        try:
            element_message = conteneur.find_element(By.CSS_SELECTOR, "[data-test='error']")
            message_obtenu = element_message.text.strip()
        except:
            message_obtenu = conteneur.text.strip()
        
        print(f"📝 Message obtenu: '{message_obtenu}'")
        print(f"📝 Message attendu: '{message_attendu}'")
        
        if message_obtenu == message_attendu:
            print("✅ Message d'erreur correct")
            return True, message_obtenu
        else:
            print("❌ Message d'erreur incorrect")
            return False, message_obtenu
            
    except Exception as e:
        print(f"❌ Aucun message d'erreur trouvé: {e}")
        return False, "Aucun message trouvé"

def tester_bouton_fermeture(driver, locators_data):
    """
    Teste le bouton de fermeture du message d'erreur
    
    Args:
        driver: Instance Selenium
        locators_data: Locators chargés
    
    Returns:
        bool: True si le bouton fonctionne
    """
    try:
        bouton = trouver_element(driver, locators_data, "error_close_button")
        
        if not bouton:
            print("❌ Bouton de fermeture non trouvé")
            return False
        
        # Vérifier que le bouton est visible et cliquable
        if bouton.is_displayed() and bouton.is_enabled():
            print("✅ Bouton de fermeture est cliquable")
            
            # Sauvegarder l'état avant clic
            try:
                conteneur_avant = driver.find_element(By.CLASS_NAME, "error-message-container")
                visible_avant = conteneur_avant.is_displayed()
            except:
                visible_avant = False
            
            # Cliquer sur le bouton
            bouton.click()
            print("✅ Clic sur le bouton de fermeture")
            
            # Attendre un peu
            time.sleep(1)
            
            # Vérifier que le message a disparu
            try:
                conteneur_apres = driver.find_element(By.CLASS_NAME, "error-message-container")
                visible_apres = conteneur_apres.is_displayed()
            except:
                visible_apres = False
            
            if visible_avant and not visible_apres:
                print("✅ Message d'erreur a disparu")
                return True
            else:
                print("❌ Message d'erreur toujours visible")
                return False
        else:
            print("❌ Bouton de fermeture non cliquable")
            return False
            
    except Exception as e:
        print(f"❌ Erreur avec le bouton de fermeture: {e}")
        return False

def verifier_connexion_reussie(driver, locators_data):
    """
    Vérifie si la connexion a réussi
    
    Args:
        driver: Instance Selenium
        locators_data: Locators chargés
    
    Returns:
        tuple: (bool succès, str message)
    """
    try:
        # Vérifier l'URL
        if "inventory" in driver.current_url:
            print("✅ URL de l'inventaire détectée")
            
            # Vérifier la présence du conteneur d'inventaire
            WebDriverWait(driver, DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "inventory_container"))
            )
            print("✅ Page d'inventaire chargée")
            
            return True, "Connexion réussie"
        else:
            print("❌ URL incorrecte après connexion")
            return False, f"URL actuelle: {driver.current_url}"
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de connexion: {e}")
        return False, f"Erreur: {str(e)}"

def executer_test_case(driver, test_case, locators_data):
    """
    Exécute un cas de test
    
    Args:
        driver: Instance Selenium
        test_case: Dictionnaire avec les données du test
        locators_data: Locators chargés
    
    Returns:
        dict: Résultats du test
    """
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_case['test_name']}")
    print(f"{'='*60}")
    print(f"📝 {test_case['description']}")
    
    resultat = {
        "test_id": test_case["test_id"],
        "test_name": test_case["test_name"],
        "succes": False,
        "details": "",
        "duree": 0,
        "screenshot": None
    }
    
    debut = time.time()
    
    try:
        # Remplir le formulaire
        username = test_case["test_data"]["username"]
        password = test_case["test_data"]["password"]
        
        if not remplir_formulaire_connexion(driver, locators_data, username, password):
            resultat["details"] = "Échec du remplissage du formulaire"
            resultat["duree"] = time.time() - debut
            return resultat
        
        # Vérifier le résultat attendu
        if test_case["expected_result"] == "success":
            # Test de connexion réussie
            connexion_ok, message = verifier_connexion_reussie(driver, locators_data)
            
            if connexion_ok:
                resultat["succes"] = True
                resultat["details"] = "Connexion réussie"
                print("✅ TEST RÉUSSI: Connexion établie")
            else:
                resultat["details"] = f"Échec de connexion: {message}"
                print("❌ TEST ÉCHOUÉ: Connexion non établie")
                
        elif test_case["expected_result"] == "error":
            # Test de message d'erreur
            message_attendu = test_case["test_data"]["expected_error"]
            erreur_ok, message_obtenu = verifier_message_erreur(driver, locators_data, message_attendu)
            
            if erreur_ok:
                # Tester le bouton de fermeture si demandé
                if test_case.get("verify_close_button", False):
                    bouton_ok = tester_bouton_fermeture(driver, locators_data)
                    
                    if bouton_ok:
                        resultat["succes"] = True
                        resultat["details"] = f"Message correct: {message_obtenu} | Bouton fermeture OK"
                        print("✅ TEST RÉUSSI: Message correct et bouton fonctionnel")
                    else:
                        resultat["details"] = f"Message correct: {message_obtenu} | Bouton fermeture KO"
                        print("❌ TEST ÉCHOUÉ: Bouton de fermeture ne fonctionne pas")
                else:
                    resultat["succes"] = True
                    resultat["details"] = f"Message correct: {message_obtenu}"
                    print("✅ TEST RÉUSSI: Message correct")
            else:
                resultat["details"] = f"Message incorrect: '{message_obtenu}' au lieu de '{message_attendu}'"
                print("❌ TEST ÉCHOUÉ: Message d'erreur incorrect")
        
        # Prendre une capture d'écran
        try:
            nom_fichier = f"screenshot_{test_case['test_id']}_{test_case['test_name']}.png"
            driver.save_screenshot(nom_fichier)
            resultat["screenshot"] = nom_fichier
            print(f"📸 Capture: {nom_fichier}")
        except Exception as e:
            print(f"⚠️  Impossible de prendre une capture: {e}")
    
    except Exception as e:
        resultat["details"] = f"Erreur pendant le test: {str(e)}"
        print(f"🔥 ERREUR: {e}")
    
    resultat["duree"] = time.time() - debut
    return resultat