"""
Script principal des tests SauceDemo
Auteur: Automatisé
Date: 2024-01-12
Description: Exécute les tests de gestion des erreurs de connexion
"""

import json
import time
import os
from datetime import datetime
from FunctionForConnection import (
    charger_locators,
    ouvrir_chrome,
    fermer_chrome,
    naviguer_vers_url,
    executer_test_case
)
from GenerateReportHTML import (
    generate_test_report
)

# ==============================================
# FONCTIONS UTILITAIRES
# ==============================================

def charger_tests(fichier="Tests.json"):
    """Charge les tests depuis le fichier JSON"""
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"❌ Fichier {fichier} non trouvé")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON dans {fichier}: {e}")
        return None

def afficher_introduction(tests_data):
    """Affiche l'introduction du programme"""
    print("\n" + "="*60)
    print("🚀 TESTS SELENIUM - SAUCEDEMO")
    print("="*60)
    
    if tests_data:
        print(f"\n📋 Suite de tests: {tests_data.get('test_suite', 'Non spécifié')}")
        print(f"📝 Description: {tests_data.get('description', '')}")
        print(f"🌐 URL: {tests_data.get('url', 'Non spécifié')}")
        print(f"🧪 Nombre de tests: {len(tests_data.get('test_cases', []))}")
    
    print("\n🎯 Objectif: Tester les scénarios de connexion échouée")
    print("🔧 Points techniques: Gérer les messages d'erreur dynamiques, localiser les éléments d'erreur")
    
    print("\n⚙️ Configuration système:")
    chrome_portable = os.path.exists(r'C:\Chrome_Sources\chrome-win64\chrome.exe')
    chromedriver = os.path.exists(r'C:\Chrome_Sources\chromedriver-win64\chromedriver.exe')
    
    print(f"   Chrome portable: {'✅' if chrome_portable else '❌'}")
    print(f"   ChromeDriver: {'✅' if chromedriver else '❌'}")
    
    if not chromedriver:
        print("\n⚠️  IMPORTANT: ChromeDriver non trouvé!")
        print("   Téléchargez-le sur: https://chromedriver.chromium.org/")
        print("   Placez-le dans: C:\\Chrome_Sources\\")
    
    print("\n⏳ Démarrage dans 5 secondes...")
    time.sleep(5)

def afficher_resultats(resultats, duree_totale):
    """Affiche les résultats des tests"""
    print("\n" + "="*60)
    print("📊 RÉSULTATS DES TESTS")
    print("="*60)
    
    # Calculer les statistiques
    total_tests = len(resultats)
    tests_reussis = sum(1 for r in resultats if r["succes"])
    tests_echoues = total_tests - tests_reussis
    taux_reussite = (tests_reussis / total_tests * 100) if total_tests > 0 else 0
    
    # Tableau des résultats détaillés
    print(f"\n┌{'─'*70}┐")
    print(f"│ {'ID':<6} {'TEST':<25} {'STATUT':<8} {'DURÉE':<8} {'DÉTAILS':<15} │")
    print(f"├{'─'*70}┤")
    
    for resultat in resultats:
        statut = "✅" if resultat["succes"] else "❌"
        nom_court = resultat["test_name"][:22] + "..." if len(resultat["test_name"]) > 25 else resultat["test_name"]
        details_court = resultat["details"][:12] + "..." if len(resultat["details"]) > 15 else resultat["details"]
        
        print(f"│ {resultat['test_id']:<6} {nom_court:<25} {statut:<8} {resultat['duree']:.2f}s {'':<2} {details_court:<15} │")
    
    print(f"└{'─'*70}┘")
    
    # Tableau des statistiques
    print(f"\n┌{'─'*40}┐")
    print(f"│ 📋 TOTAL DES TESTS EXÉCUTÉS : {total_tests:2d}        │")
    print(f"│ ✅ TESTS RÉUSSIS           : {tests_reussis:2d}        │")
    print(f"│ ❌ TESTS ÉCHOUÉS           : {tests_echoues:2d}        │")
    print(f"│ 📊 TAUX DE RÉUSSITE        : {taux_reussite:6.1f}%     │")
    print(f"│ ⏱️  TEMPS TOTAL            : {duree_totale:6.1f}s     │")
    print(f"└{'─'*40}┘")
    
    # Message final
    print("\n" + "="*60)
    print("📋 CONCLUSION")
    print("="*60)
    
    if tests_reussis == total_tests:
        print("\n🎉🎉🎉 FÉLICITATIONS ! TOUS LES TESTS SONT RÉUSSIS ! 🎉🎉🎉")
    elif taux_reussite >= 80:
        print(f"\n👍 EXCELLENT ! {tests_reussis}/{total_tests} tests réussis")
    else:
        print(f"\n⚠️  {tests_echoues} test(s) échoué(s). Vérification nécessaire.")
    
    # Fichiers générés
    print("\n📁 Captures d'écran générées:")
    screenshots = [r["screenshot"] for r in resultats if r["screenshot"] and os.path.exists(r["screenshot"])]
    for screenshot in screenshots:
        print(f"  📄 {screenshot}")

def executer_tous_les_tests():
    """Fonction principale qui exécute tous les tests"""
    # Charger les données
    tests_data = charger_tests("Tests.json")
    if not tests_data:
        print("❌ Impossible de charger les tests")
        return
    
    locators_data = charger_locators("Locatorss.json")
    if not locators_data:
        print("⚠️  Utilisation des locators par défaut")
    
    # Afficher l'introduction
    afficher_introduction(tests_data)
    
    # Préparer les résultats
    resultats = []
    debut_total = time.time()
    
    # Déterminer le mode Chrome
    use_portable = os.path.exists(r'C:\Chrome_Sources\chrome-win64\chrome.exe') and \
                   os.path.exists(r'C:\Chrome_Sources\chromedriver-win64\chromedriver.exe')
    
    # Exécuter chaque test
    test_cases = tests_data.get("test_cases", [])
    
    for test_case in test_cases:
        print(f"\n{'🔹'*30}")
        print(f"🔍 Exécution du test: {test_case['test_id']} - {test_case['test_name']}")
        print(f"{'🔹'*30}")
        
        # Créer un nouveau navigateur pour chaque test (isolation)
        driver = ouvrir_chrome(use_portable=use_portable)
        
        try:
            # Naviguer vers l'URL
            url = tests_data.get("url", "https://www.saucedemo.com/")
            naviguer_vers_url(driver, url)
            
            # Exécuter le test
            resultat = executer_test_case(driver, test_case, locators_data)
            resultats.append(resultat)
            
            # Pause entre les tests
            time.sleep(2)
            
        except Exception as e:
            print(f"🔥 ERREUR CRITIQUE: {e}")
            resultats.append({
                "test_id": test_case["test_id"],
                "test_name": test_case["test_name"],
                "succes": False,
                "details": f"Erreur critique: {str(e)}",
                "duree": 0,
                "screenshot": None
            })
        
        finally:
            # Fermer le navigateur
            fermer_chrome(driver)
    
    # Calculer le temps total
    duree_totale = time.time() - debut_total
    
    # Afficher les résultats
    afficher_resultats(resultats, duree_totale)
    
    # Générer le rapport HTML
    print(f"\n{'='*60}")
    print(f"📊 GÉNÉRATION DU RAPPORT HTML")
    print(f"{'='*60}")
    
    try:
        # Transformer les résultats pour matcher la structure attendue par generate_test_report
        resultats_transformes = []
        for r in resultats:
            resultats_transformes.append({
                "passed": r["succes"],  # Convertir succes en passed
                "product": r["test_name"],
                "price": r.get("details", ""),
                "total_tests": 1,
                "passed_tests": 1 if r["succes"] else 0,
                "failed_tests": 0 if r["succes"] else 1
            })
        
        # Préparer les données pour le rapport
        global_results = {
            "total_tests": len(resultats),
            "passed": sum(1 for r in resultats if r["succes"]),
            "failed": sum(1 for r in resultats if not r["succes"]),
            "details": [f"{'✅' if r['succes'] else '❌'} {r['test_name']}: {r['details']}" for r in resultats]
        }
        
        # Générer le rapport
        html_report = generate_test_report(resultats_transformes, global_results, tests_data.get('description', 'Tests SauceDemo'))
        
        # Sauvegarder le rapport
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        report_filename = os.path.join(reports_dir, f"test_report_saucedemo_{time.strftime('%Y%m%d_%H%M%S')}.html")
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"✅ Rapport généré: {report_filename}")
        print(f"📊 Ouvrir le fichier dans un navigateur pour voir le rapport détaillé")
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Informations finales
    print(f"\n📅 Date d'exécution: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Mode Chrome: {'Portable' if use_portable else 'Système'}")
    print(f"📍 Locators: {'JSON' if locators_data else 'Par défaut'}")
    
    return resultats

# ==============================================
# POINT D'ENTRÉE PRINCIPAL
# ==============================================

if __name__ == "__main__":
    print("\n🔧" * 25)
    print("🔧 TESTS AUTOMATISÉS SAUCEDEMO")
    print("🔧 Gestion des erreurs de connexion")
    print("🔧" * 25)
    
    try:
        resultats = executer_tous_les_tests()
        
        # Sauvegarder les résultats dans un fichier JSON
        if resultats:
            with open("test_results.json", "w", encoding="utf-8") as f:
                json.dump({
                    "date": datetime.now().isoformat(),
                    "resultats": resultats
                }, f, indent=2, ensure_ascii=False)
            print("\n💾 Résultats sauvegardés dans: test_results.json")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrompus par l'utilisateur")
    
    except Exception as e:
        print(f"\n🔥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "="*60)
        print("👋 Programme terminé")
        print("="*60)