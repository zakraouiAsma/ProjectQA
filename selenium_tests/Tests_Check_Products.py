import json
import sys
import time
import os
from FunctionSauceDemo import (
    OpenChrome, CloseChrome, check_connection_user, check_products_catalog
)

CHROME_PORTABLE_PATH = r'C:\Chrome_Sources\chrome-win64\chrome.exe'
                         
CHROME_DRIVER_PATH = r'C:\Chrome_Sources\chromedriver-win64\chromedriver.exe'
URL = "https://www.saucedemo.com/"
json_path = os.path.join(os.path.dirname(__file__), "DataProducts.json")


def run_tests():
    """
    Fonction principale pour exécuter les tests  de verif products depuis le fichier JSON
    """
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    
    test_cases = data.get("test_cases", [])
    global_start = time.time()
    scenario_times = []
    
    for idx, case in enumerate(test_cases):
        print(f"\n{'='*60}\nTest Case {idx+1}: {case['description']}")
        start = time.time()
        driver = OpenChrome(CHROME_DRIVER_PATH, CHROME_PORTABLE_PATH)
        
        try:
            # Connexion utilisateur
            if not check_connection_user(driver, case["username"], case["password"]):
                print("[FAIL] Connexion échouée")
                CloseChrome(driver)
                scenario_times.append(0)
                continue
            
            # Vérifier le catalogue des produits
            products_to_verify = case.get("products_to_verify", [])
            if products_to_verify:
                print("\n📦 Vérification du catalogue des produits...")
                results = check_products_catalog(driver, products_to_verify)
                print(f"📊 Résultats: {results['passed']}/{results['total_tests']} vérifications réussies")
            else:
                print("⚠️ Pas de produits à vérifier dans le test case")
            
        except Exception as e:
            print(f"[ERROR] Une erreur est survenue: {str(e)}")
        finally:
            CloseChrome(driver)
            elapsed = time.time() - start
            scenario_times.append(elapsed)
            print(f"Temps d'exécution: {elapsed:.2f}s")
    
    global_elapsed = time.time() - global_start
    print(f"\n{'='*60}")
    print(f"Temps total: {global_elapsed:.2f}s")
    print(f"Nombre de tests exécutés: {len(test_cases)}")


if __name__ == "__main__":
    run_tests()

