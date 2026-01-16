# ProjectQA - Test Automation Suite

Suite d'automatisation de tests Selenium pour valider les scénarios d'achat et les fonctionnalités de la plateforme SauceDemo.

---

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
