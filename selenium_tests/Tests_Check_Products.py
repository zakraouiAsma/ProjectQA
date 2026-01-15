import json
import sys
import time
import os
from FunctionSauceDemo import (
    check_single_product, check_products_catalog,
    
)
from GenerateReportHTML import (
    generate_test_report
)
from FunctionForConnection import (
    ouvrir_chrome, fermer_chrome, naviguer_vers_url, 
    remplir_formulaire_connexion, charger_locators
)  

CHROME_PORTABLE_PATH = r'C:\Chrome_Sources\chrome-win64\chrome.exe'
                         
CHROME_DRIVER_PATH = r'C:\Chrome_Sources\chromedriver-win64\chromedriver.exe'
URL = "https://www.saucedemo.com/"
json_path = os.path.join(os.path.dirname(__file__), "DataProducts.json")


def run_tests():
    """
    Fonction principale pour exécuter les tests de verification de produits
    Utilise les fonctions de FunctionForConnection pour la connexion
    Pour CHAQUE produit:
    1. Ouvre Chrome (via FunctionForConnection)
    2. Se connecte (via FunctionForConnection)
    3. Vérifie le produit (via FunctionSauceDemo)
    4. Ferme Chrome (via FunctionForConnection)
    """
    # Charger les locators
    locators_data = charger_locators("Locatorss.json")
    
    if not locators_data:
        print("❌ Impossible de charger les locators")
        return
    
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    
    test_cases = data.get("test_cases", [])
    
    for idx, case in enumerate(test_cases):
        print(f"\n{'='*60}\nTest Case {idx+1}: {case['description']}")
        
        products_to_verify = case.get("products_to_verify", [])
        
        if not products_to_verify:
            print(" ⚠️ Pas de produits à vérifier dans le test case")
            continue
        
        # Données des produits et credentials
        username = case.get("username", "")
        password = case.get("password", "")
        
        # Exécuter 6 tests (un par produit)
        global_start = time.time()
        test_results = []
        
        for product_idx, product_data in enumerate(products_to_verify):
            product_name = product_data.get("name", "")
            product_price = product_data.get("price_label", "")
            
            print(f"\n{'='*60}")
            print(f"Test {product_idx + 1}/6 - Vérification du produit: {product_name} ({product_price})")
            print(f"{'='*60}")
            
            start = time.time()
            driver = None
            
            try:
                # 1. Ouvrir Chrome (via FunctionForConnection)
                print(f"🟢 Ouverture de Chrome...")
                driver = ouvrir_chrome(use_portable=True)
                
                # 2. Naviguer vers l'URL
                print(f"🟢 Navigation vers {URL}...")
                naviguer_vers_url(driver, URL)
                
                # 3. Se connecter (via FunctionForConnection)
                print(f"🟢 Connexion avec {username}...")
                connexion_ok = remplir_formulaire_connexion(driver, locators_data, username, password)
                
                if not connexion_ok:
                    print(f"❌ Connexion échouée pour le test {product_idx + 1}")
                    test_results.append({
                        "product": product_name,
                        "price": product_price,
                        "passed": False,
                        "reason": "Connexion échouée"
                    })
                    continue
                
                # Attendre le chargement de la page
                time.sleep(2)
                
                # 4. Vérifier ce produit spécifique
                print(f"🟢 Vérification du produit...")
                result = check_single_product(driver, product_data)
                
                # Sauvegarder le résultat
                test_results.append({
                    "product": product_name,
                    "price": product_price,
                    "passed": result["failed"] == 0,
                    "total_tests": result["total_tests"],
                    "passed_tests": result["passed"],
                    "failed_tests": result["failed"]
                })
                
                elapsed = time.time() - start
                print(f"\n✅ Test {product_idx + 1} complété en {elapsed:.2f}s")
                
            except Exception as e:
                print(f"❌ Erreur lors du test {product_idx + 1}: {str(e)}")
                test_results.append({
                    "product": product_name,
                    "price": product_price,
                    "passed": False,
                    "reason": str(e)
                })
            
            finally:
                # 5. Fermer Chrome (via FunctionForConnection)
                if driver:
                    try:
                        print(f"🟢 Fermeture de Chrome...")
                        fermer_chrome(driver)
                    except:
                        pass
        
        # Afficher le résumé final des 6 tests individuels
        global_elapsed = time.time() - global_start
        print(f"\n{'='*60}")
        print(f"RÉSUMÉ FINAL DES 6 TESTS INDIVIDUELS")
        print(f"{'='*60}")
        
        passed_count = sum(1 for r in test_results if r["passed"])
        failed_count = len(test_results) - passed_count
        
        for result in test_results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"{status} - {result['product']} ({result['price']})")
        
        print(f"\n📊 Résultats des tests individuels:")
        print(f"   Tests réussis: {passed_count}/6")
        print(f"   Tests échoués: {failed_count}/6")
        print(f"   Temps total: {global_elapsed:.2f}s")
        print(f"   Taux de réussite: {(passed_count/len(test_results)*100):.1f}%")
        
        # Exécuter la fonction globale pour les vérifications supplémentaires
        
        
        driver = None
        try:
            # Ouvrir Chrome
            print(f"🟢 Ouverture de Chrome pour les tests globaux...")
            driver = ouvrir_chrome(use_portable=True)
            
            # Naviguer vers l'URL
            print(f"🟢 Navigation vers {URL}...")
            naviguer_vers_url(driver, URL)
            
            # Se connecter
            print(f"🟢 Connexion avec {username}...")
            time.sleep(1)
            connexion_ok = remplir_formulaire_connexion(driver, locators_data, username, password)
            
            if connexion_ok:
                time.sleep(2)
                # Exécuter les tests globaux avec les données complètes des produits
                print(f"\n🟢 Exécution des vérifications globales...")
                global_results = check_products_catalog(driver, products_to_verify)
                
                print(f"\n✅ Tests globaux complétés avec succès!")
            else:
                print(f"❌ Connexion échouée pour les tests globaux")
        
        except Exception as e:
            print(f"❌ Erreur lors des tests globaux: {str(e)}")
        
        finally:
            # Fermer Chrome
            if driver:
                try:
                    print(f"🟢 Fermeture de Chrome...")
                    fermer_chrome(driver)
                except:
                    pass
        
        # Générer le rapport HTML
        print(f"\n{'='*60}")
        print(f"GÉNÉRATION DU RAPPORT")
        print(f"{'='*60}")
        
        try:
            html_report = generate_test_report(test_results, global_results, case['description'])
            
            # Sauvegarder le rapport dans le dossier reports
            reports_dir = "reports"
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            report_filename = os.path.join(reports_dir, f"test_report_{time.strftime('%Y%m%d_%H%M%S')}.html")
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(html_report)
            
            print(f"✅ Rapport généré: {report_filename}")
            print(f"📊 Ouvrir le fichier dans un navigateur pour voir le rapport détaillé")
        except Exception as e:
            print(f"❌ Erreur lors de la génération du rapport: {str(e)}")
    
    global_elapsed = time.time() - global_start
    print(f"\n{'='*60}")
    print(f"Temps total: {global_elapsed:.2f}s")
    print(f"Nombre de cas de test exécutés: {len(test_cases)}")


if __name__ == "__main__":
    run_tests()

