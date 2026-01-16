# ProjectQA - Test Automation Suite


## 📋 Test Check Products

### Description

Le test **Check Products** (`Tests_Check_Products.py`) est un test Selenium automatisé qui vérifie l'intégrité des produits disponibles sur le catalogue de SauceDemo. Ce test exécute une suite complète de vérifications pour s'assurer que chaque produit possède les bonnes informations (nom, prix, description, etc.).

### 🎯 Objectif Principal

Vérifier que les 6 produits disponibles sur la plateforme SauceDemo sont correctement affichés avec :
- ✅ Les noms de produits exacts
- ✅ Les prix corrects
- ✅ Les descriptions valides
- ✅ Les images présentes
- ✅ Les boutons d'action fonctionnels

### 📂 Fichiers Associés

| Fichier | Description |
|---------|-------------|
| `Tests_Check_Products.py` | Fichier principal de test |
| `FunctionProductSauceDemo.py` | Fonctions de vérification des produits |
| `FunctionForConnection.py` | Fonctions de connexion et navigation |
| `GenerateReportHTML.py` | Génération de rapports HTML |
| `DataProducts.json` | Données de référence des produits |
| `Locatorss.json` | Sélecteurs CSS/XPath des éléments |

### 🏃 Exécution du Test

#### Prérequis
- Python 3.8+
- Selenium installé
- ChromeDriver compatible avec votre version de Chrome
- Fichiers JSON de configuration présents

#### Commande d'exécution

```bash
cd selenium_tests
python Tests_Check_Products.py
```

#### Flux d'exécution

1. **Chargement des configurations** : Charge les locators depuis `Locatorss.json`
2. **Lecture des données** : Récupère les cas de test depuis `DataProducts.json`
3. **Pour chaque produit** :
   - Ouvre une instance Chrome
   - Se connecte à SauceDemo
   - Vérifie les informations du produit
   - Génère un rapport de résultat
   - Ferme l'instance Chrome
4. **Génération du rapport** : Crée un rapport HTML dans le dossier `reports/`

### 📊 Structure des Résultats

Chaque test génère :

#### Tests Individuels (6 produits)
- Vérification 1/6 : Sauce Labs Backpack
- Vérification 2/6 : Sauce Labs Bike Light
- Vérification 3/6 : Sauce Labs Bolt T-Shirt
- Vérification 4/6 : Sauce Labs Fleece Jacket
- Vérification 5/6 : Sauce Labs Onesie
- Vérification 6/6 : Test.allTheThings() T-Shirt (Red)

#### Tests Globaux
Vérifications supplémentaires du catalogue :
- ✅ Tous les produits sont visibles
- ✅ Les prix sont affichés correctement
- ✅ Les images se chargent
- ✅ Les boutons "Add to Cart" sont fonctionnels

### 📈 Rapport Généré

Un rapport HTML est automatiquement généré après chaque exécution :

**Format du nom** : `test_report_YYYYMMDD_HHMMSS.html`

**Contenu du rapport** :
- 📋 Informations du test (date, heure, plateforme)
- 📊 Statistiques des tests individuels (taux de réussite, temps)
- 🌍 Résultats des tests globaux
- 📈 Résumé final avec détails des échechs éventuels

### 🔧 Configuration

#### DataProducts.json
Contient les cas de test avec les produits à vérifier :
```json
{
  "test_cases": [
    {
      "description": "Vérification du catalogue de produits",
      "username": "standard_user",
      "password": "secret_sauce",
      "products_to_verify": [...]
    }
  ]
}
```

#### Locatorss.json
Définit les sélecteurs des éléments HTML :
```json
{
  "saucedemo": {
    "login_page": {...},
    "inventory_page": {...}
  }
}
```

### ✅ Résultats Attendus

```
========================================================
RÉSUMÉ FINAL DES 6 TESTS INDIVIDUELS
========================================================
✅ PASS - Sauce Labs Backpack ($29.99)
✅ PASS - Sauce Labs Bike Light ($9.99)
✅ PASS - Sauce Labs Bolt T-Shirt ($15.99)
✅ PASS - Sauce Labs Fleece Jacket ($49.99)
✅ PASS - Sauce Labs Onesie ($7.99)
✅ PASS - Test.allTheThings() T-Shirt ($15.99)

📊 Résultats des tests individuels:
   Tests réussis: 6/6
   Tests échoués: 0/6
   Taux de réussite: 100.0%
```



### 📝 Logs et Sortie Console

Le test affiche des informations détaillées en temps réel :
- 🟢 Actions en cours (Ouverture, Navigation, Connexion)
- ✅ Actions réussies
- ❌ Erreurs rencontrées
- 📊 Statistiques et résumés
- 📁 Chemin du rapport généré

### 🔗 Intégration avec Jenkins

Le test peut être intégré dans un pipeline Jenkins via le `Jenkinsfile` pour une exécution automatisée.

---

## 📚 DOCUMENTATION DÉTAILLÉE DES TESTS

### TEST 1️⃣ : Check Products (Vérification du Catalogue)

#### SLIDE 1 : Configuration & Scope

**Configuration** 📋
```json
{
  "test_name": "Check Products",
  "file": "Tests_Check_Products.py",
  "scope": "Vérification complète du catalogue produits",
  "credentials": "standard_user / secret_sauce",
  "data_file": "DataProducts.json",
  "config_file": "Locatorss.json",
  "reports_dir": "reports/",
  "report_pattern": "test_report_YYYYMMDD_HHMMSS.html"
}
```

**Scope Fonctionnel** 🎯
| Fonctionnalité | Test | XRAY ID |
|---|---|---|
| Affichage des produits | Vérifier les 6 produits visibles | `QA-101` |
| Informations produits | Nom + Prix + Description | `QA-102` |
| Images produits | Chargement des images | `QA-103` |
| Boutons d'action | Add to Cart fonctionnel | `QA-104` |
| Taux de réussite | 100% des vérifications | `QA-105` |

**Job Jenkins Dédié** 🔧
```groovy
pipeline {
    agent any
    
    triggers {
        cron('H 9 * * *')  // 9h chaque jour
    }
    
    stages {
        stage('Run Check Products Test') {
            steps {
                dir('selenium_tests') {
                    sh 'python Tests_Check_Products.py'
                }
            }
        }
        
        stage('Generate Report') {
            steps {
                publishHTML([
                    reportDir: 'selenium_tests/reports',
                    reportFiles: 'test_report_*.html',
                    reportName: 'Check Products Report'
                ])
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'selenium_tests/reports/**/*.html'
        }
    }
}
```

---

#### SLIDE 2 : Code & Exécution

**Code Principal** 💻
```python
# Tests_Check_Products.py - Exécution
from FunctionProductSauceDemo import check_single_product, check_products_catalog
from GenerateReportHTML import generate_test_report

def run_tests():
    # 1. Charger les configurations
    locators_data = charger_locators("Locatorss.json")
    
    # 2. Lire les données produits
    with open("DataProducts.json") as f:
        test_cases = json.load(f).get("test_cases", [])
    
    # 3. Pour chaque cas de test
    for case in test_cases:
        # 4. Exécuter 6 vérifications (un par produit)
        for product in case["products_to_verify"]:
            driver = ouvrir_chrome(use_portable=True)
            naviguer_vers_url(driver, URL)
            remplir_formulaire_connexion(driver, locators_data, ...)
            result = check_single_product(driver, product)
            fermer_chrome(driver)
        
        # 5. Générer le rapport HTML
        html_report = generate_test_report(test_results, global_results)
        with open(f"reports/test_report_{timestamp}.html", 'w') as f:
            f.write(html_report)
```

**Exécution & Résultats** ✅
```bash
$ python Tests_Check_Products.py

========================================================
Test Case 1: Vérification du catalogue de produits
========================================================
Test 1/6 - Vérification: Sauce Labs Backpack ($29.99)
✅ Test 1 complété en 8.45s

Test 2/6 - Vérification: Sauce Labs Bike Light ($9.99)
✅ Test 2 complété en 7.82s

... (4 autres produits)

========================================================
RÉSUMÉ FINAL DES 6 TESTS INDIVIDUELS
========================================================
✅ PASS - Sauce Labs Backpack ($29.99)
✅ PASS - Sauce Labs Bike Light ($9.99)
✅ PASS - Sauce Labs Bolt T-Shirt ($15.99)
✅ PASS - Sauce Labs Fleece Jacket ($49.99)
✅ PASS - Sauce Labs Onesie ($7.99)
✅ PASS - Test.allTheThings() T-Shirt ($15.99)

📊 Résultats:
   Tests réussis: 6/6
   Tests échoués: 0/6
   Taux de réussite: 100.0%
   Temps total: 52.34s

✅ Rapport généré: reports/test_report_20260116_140530.html
```

---

### TEST 2️⃣ : Sauce Demo Test (Gestion des Erreurs de Connexion)

#### SLIDE 1 : Configuration & Scope

**Configuration** 📋
```json
{
  "test_name": "SauceDemo Test",
  "file": "TestSauceDemo.py",
  "scope": "Tests de gestion des erreurs de connexion",
  "credentials": "Multiples (user_invalide, standard_user, etc.)",
  "data_file": "Tests.json",
  "config_file": "Locators.json",
  "reports_dir": "selenium_tests/reports/",
  "report_pattern": "test_report_YYYYMMDD_HHMMSS.html"
}
```

**Scope Fonctionnel** 🎯
| Scénario | Description | XRAY ID |
|---|---|---|
| Utilisateur invalide | Erreur "nom d'utilisateur non reconnu" | `QA-201` |
| Mot de passe vide | Erreur "Mot de passe requis" | `QA-202` |
| Username vide | Erreur "Nom d'utilisateur requis" | `QA-203` |
| Connexion réussie | Redirection vers inventaire | `QA-204` |
| Messages d'erreur | Affichage dynamique des erreurs | `QA-205` |

**Job Jenkins Dédié** 🔧
```groovy
pipeline {
    agent any
    
    triggers {
        cron('H 15 * * *')  // 15h chaque jour
        pollSCM('H/30 * * * *')  // Toutes les 30 minutes
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run SauceDemo Tests') {
            steps {
                dir('selenium_tests') {
                    sh 'python TestSauceDemo.py'
                }
            }
        }
        
        stage('Generate HTML Report') {
            steps {
                script {
                    publishHTML([
                        reportDir: 'selenium_tests/reports',
                        reportFiles: '*.html',
                        reportName: 'SauceDemo Test Report'
                    ])
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ Tous les tests sont passés'
        }
        failure {
            echo '❌ Certains tests ont échoué'
            emailext(
                to: 'qa-team@company.com',
                subject: 'SauceDemo Tests Failed',
                body: 'Vérifiez les rapports Jenkins'
            )
        }
        always {
            junit 'test_results.json'
            archiveArtifacts artifacts: 'selenium_tests/reports/**'
        }
    }
}
```

---

#### SLIDE 2 : Code & Exécution

**Code Principal** 💻
```python
# TestSauceDemo.py - Structure
from FunctionForConnection import (
    charger_locators, ouvrir_chrome, fermer_chrome,
    naviguer_vers_url, executer_test_case
)
from GenerateReportHTML import generate_test_report

def executer_tous_les_tests():
    # 1. Charger configurations
    tests_data = charger_tests("Tests.json")
    locators_data = charger_locators("Locators.json")
    
    resultats = []
    debut_total = time.time()
    
    # 2. Pour chaque cas de test
    for test_case in tests_data.get("test_cases", []):
        driver = ouvrir_chrome(use_portable=True)
        
        try:
            # 3. Navigation et exécution
            naviguer_vers_url(driver, tests_data["url"])
            resultat = executer_test_case(driver, test_case, locators_data)
            resultats.append(resultat)
        finally:
            fermer_chrome(driver)
    
    # 4. Générer rapport HTML
    duree_totale = time.time() - debut_total
    rapport_html = generer_rapport_html(resultats, duree_totale)
    print(f"✅ Rapport généré: {rapport_html}")

def generer_rapport_html(resultats, duree_totale):
    """Génère rapport HTML avec timestamp"""
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Formater les données
    individual_results = [...]
    global_results = {...}
    
    # Générer HTML
    html_content = generate_test_report(
        individual_results, 
        global_results, 
        "Tests Selenium - SauceDemo"
    )
    
    # Sauvegarder
    filepath = f"reports/test_report_{timestamp}.html"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath
```

**Exécution & Résultats** ✅
```bash
$ python TestSauceDemo.py

============================================================
🚀 TESTS SELENIUM - SAUCEDEMO
============================================================
🎯 Objectif: Tester les scénarios de connexion échouée

⏳ Démarrage dans 5 secondes...

🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
🔍 Exécution du test: TC-001 - Utilisateur invalide
🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
✅ Test TC-001 complété en 5.23s

... (autres tests)

============================================================
📊 RÉSULTATS DES TESTS
============================================================
┌──────────────────────────────────────────────────────────┐
│ ID     TEST                  STATUT   DURÉE   DÉTAILS    │
├──────────────────────────────────────────────────────────┤
│ TC-001 Utilisateur invalide  ✅       5.23s   Succès     │
│ TC-002 Pas de username       ✅       4.89s   Succès     │
│ TC-003 Pas de password       ✅       5.12s   Succès     │
│ TC-004 Connexion réussie     ✅       6.45s   Succès     │
│ TC-005 Messages d'erreur     ✅       5.67s   Succès     │
└──────────────────────────────────────────────────────────┘

┌────────────────────────┐
│ 📋 TOTAL : 5           │
│ ✅ RÉUSSIS : 5         │
│ ❌ ÉCHOUÉS : 0         │
│ 📊 TAUX : 100.0%       │
│ ⏱️  TEMPS : 27.36s     │
└────────────────────────┘

🎉 FÉLICITATIONS ! TOUS LES TESTS SONT RÉUSSIS ! 🎉

✅ Rapport HTML généré: reports/test_report_20260116_140530.html
```

---

## 📊 MATRICE DE COUVERTURE XRAY

```
┌─────────────────────────────────────────────────────────┐
│ TEST                │ XRAY IDs    │ STATUT   │ DERNIER │
├─────────────────────────────────────────────────────────┤
│ Check Products      │ QA-101..105 │ ✅ PASS  │ 16/01  │
│ SauceDemo Test      │ QA-201..205 │ ✅ PASS  │ 16/01  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔗 INTÉGRATION JENKINS

### Vue d'ensemble des Jobs

| Job | Schedule | Triggers | Rapports |
|-----|----------|----------|----------|
| `Check-Products-Daily` | 09:00 UTC | Quotidien | HTML + Archive |
| `SauceDemo-Tests-Hourly` | À la demande | Polling 30min | HTML + Email |
| `Full-Suite-Weekly` | Lundi 08:00 | Webhook | Tous les rapports |

### Pipeline Global

```groovy
// Jenkinsfile - Pipeline principal
pipeline {
    agent any
    
    options {
        timestamps()
        timeout(time: 1, unit: 'HOURS')
    }
    
    stages {
        stage('Check Products Test') {
            steps {
                build job: 'Check-Products-Daily'
            }
        }
        
        stage('SauceDemo Tests') {
            steps {
                build job: 'SauceDemo-Tests-Hourly'
            }
        }
        
        stage('Consolidate Reports') {
            steps {
                sh 'python consolidate_reports.py'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'selenium_tests/reports/**'
            cleanWs()
        }
    }
}
```

---


