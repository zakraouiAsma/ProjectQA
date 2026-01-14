import json
import sys
import time
import os
from datetime import datetime
from FunctionSauceDemo import (
    OpenChrome, CloseChrome, check_connection_user, check_products_catalog
)

CHROME_PORTABLE_PATH = r'C:\Chrome_Sources\chrome-win64\chrome.exe'
                         
CHROME_DRIVER_PATH = r'C:\Chrome_Sources\chromedriver-win64\chromedriver.exe'
URL = "https://www.saucedemo.com/"
json_path = os.path.join(os.path.dirname(__file__), "DataProducts.json")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


def generate_html_report(test_results, total_time):
    """
    Génère un rapport HTML avec les résultats des tests
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rapport Tests Selenium</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .header {{ background-color: #333; color: white; padding: 20px; border-radius: 5px; }}
            .summary {{ background-color: #e8f4f8; padding: 15px; margin: 20px 0; border-left: 4px solid #0088cc; }}
            .test-case {{ background-color: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .test-case.passed {{ border-left: 4px solid #28a745; }}
            .test-case.failed {{ border-left: 4px solid #dc3545; }}
            .status {{ font-weight: bold; padding: 5px 10px; border-radius: 3px; }}
            .status.passed {{ background-color: #d4edda; color: #155724; }}
            .status.failed {{ background-color: #f8d7da; color: #721c24; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f9f9f9; font-weight: bold; }}
            .footer {{ margin-top: 30px; padding: 20px; background-color: white; border-radius: 5px; text-align: center; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Rapport d'Execution des Tests Selenium</h1>
            <p>Date: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
        </div>
        
        <div class="summary">
            <h2>Resume</h2>
            <p><strong>Nombre de tests:</strong> {len(test_results)}</p>
            <p><strong>Tests reussis:</strong> <span style="color: green;">{sum(1 for r in test_results if r['status'] == 'PASS')}</span></p>
            <p><strong>Tests echoues:</strong> <span style="color: red;">{sum(1 for r in test_results if r['status'] == 'FAIL')}</span></p>
            <p><strong>Temps total:</strong> {total_time:.2f}s</p>
        </div>
        
        <h2>Details des Tests</h2>
    """
    
    for idx, result in enumerate(test_results, 1):
        status_class = 'passed' if result['status'] == 'PASS' else 'failed'
        status_badge = f'<span class="status {status_class}">{result["status"]}</span>'
        
        html_content += f"""
        <div class="test-case {status_class}">
            <h3>Test Case {idx}: {result['description']}</h3>
            {status_badge}
            <table>
                <tr>
                    <th>Information</th>
                    <th>Valeur</th>
                </tr>
                <tr>
                    <td>Utilisateur</td>
                    <td>{result.get('username', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Temps d'execution</td>
                    <td>{result['duration']:.2f}s</td>
                </tr>
                <tr>
                    <td>Message</td>
                    <td>{result.get('message', 'N/A')}</td>
                </tr>
            </table>
        </div>
        """
    
    html_content += """
        <div class="footer">
            <p>Rapport genere automatiquement par le script de test Selenium</p>
        </div>
    </body>
    </html>
    """
    
    report_path = os.path.join(REPORTS_DIR, "rapport_selenium.html")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n[INFO] Rapport HTML genere: {report_path}")
    return report_path


def run_tests():
    """
    Fonction principale pour exécuter les tests  de verif products depuis le fichier JSON
    """
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    
    test_cases = data.get("test_cases", [])
    global_start = time.time()
    test_results = []
    
    for idx, case in enumerate(test_cases):
        print(f"\n{'='*60}\nTest Case {idx+1}: {case['description']}")
        start = time.time()
        driver = OpenChrome(CHROME_DRIVER_PATH, CHROME_PORTABLE_PATH)
        
        test_result = {
            'description': case['description'],
            'username': case.get('username', 'N/A'),
            'status': 'PASS',
            'message': 'Test reussi',
            'duration': 0
        }
        
        try:
            # Connexion utilisateur
            if not check_connection_user(driver, case["username"], case["password"]):
                print("[FAIL] Connexion echouee")
                test_result['status'] = 'FAIL'
                test_result['message'] = 'Connexion echouee'
                CloseChrome(driver)
                elapsed = time.time() - start
                test_result['duration'] = elapsed
                test_results.append(test_result)
                continue
            
            # Vérifier le catalogue des produits
            products_to_verify = case.get("products_to_verify", [])
            if products_to_verify:
                print("\n[INFO] Verification du catalogue des produits...")
                results = check_products_catalog(driver, products_to_verify)
                print(f"[RESULTS] Resultats: {results['passed']}/{results['total_tests']} verifications reussies")
                test_result['message'] = f"Resultats: {results['passed']}/{results['total_tests']} verifications reussies"
            else:
                print("[WARNING] Pas de produits a verifier dans le test case")
            
        except Exception as e:
            print(f"[ERROR] Une erreur est survenue: {str(e)}")
            test_result['status'] = 'FAIL'
            test_result['message'] = f"Erreur: {str(e)}"
        finally:
            CloseChrome(driver)
            elapsed = time.time() - start
            test_result['duration'] = elapsed
            test_results.append(test_result)
            print(f"Temps d'execution: {elapsed:.2f}s")
    
    global_elapsed = time.time() - global_start
    print(f"\n{'='*60}")
    print(f"Temps total: {global_elapsed:.2f}s")
    print(f"Nombre de tests executes: {len(test_cases)}")
    
    # Générer le rapport HTML
    generate_html_report(test_results, global_elapsed)


if __name__ == "__main__":
    run_tests()

