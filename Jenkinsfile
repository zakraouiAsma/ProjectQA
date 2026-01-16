pipeline {
    agent any

    environment {
        PYTHON_VERSION = "3.11"
        PROJECT_PATH = "${WORKSPACE}"
        REPORTS_DIR = "${WORKSPACE}/selenium_tests/reports"
        VENV_PATH = "${WORKSPACE}/venv"
    }

    options {
        timestamps()
        timeout(time: 2, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '30'))
    }

    triggers {
        // Trigger cron pour exécution automatique des tests
        // Check Products à 9h + SauceDemo à 21h + Polling toutes les 30 min
        cron('''
            H 9 * * * 
            H 21 * * *
        ''')
        
        // Polling SCM - Vérifier les changements toutes les 30 minutes
        pollSCM('H/30 * * * *')
    }

    stages {
        stage('🔍 Checkout du Code') {
            steps {
                echo '======================================'
                echo '📥 Récupération du code depuis GitHub'
                echo '======================================'
                git branch: 'main', url: 'https://github.com/zakraouiAsma/ProjectQA'
                echo '✅ Code téléchargé avec succès'
            }
        }

        stage('⚙️ Setup Environnement') {
            steps {
                echo '======================================'
                echo '🔧 Configuration de l\'environnement Python'
                echo '======================================'
                bat """
                echo Création de l'environnement virtuel...
                python -m venv venv
                call venv\\Scripts\\activate.bat
                
                echo Mise à jour de pip...
                python -m pip install --upgrade pip setuptools wheel
                
                echo Installation des dépendances depuis requirements.txt...
                pip install -r requirements.txt
                
                echo Vérification des installations...
                pip list
                
                echo ✅ Environnement configuré avec succès
                python --version
                """
            }
        }

        stage('📂 Préparation des Répertoires') {
            steps {
                echo '======================================'
                echo '📁 Préparation des dossiers'
                echo '======================================'
                bat """
                if not exist reports mkdir reports
                if not exist selenium_tests\\reports mkdir selenium_tests\\reports
                echo ✅ Répertoires prêts
                """
            }
        }

        stage('🧪 Test 1: Check Products') {
            steps {
                echo '======================================'
                echo '🧪 Exécution: Vérification du Catalogue'
                echo '======================================'
                echo 'Test: Tests_Check_Products.py'
                echo 'Scope: 6 produits | Verifications globales'
                echo 'XRAY IDs: QA-101 à QA-105'
                echo '======================================'
                
                bat """
                call venv\\Scripts\\activate.bat
                cd selenium_tests
                chcp 65001
                echo.
                echo Démarrage du test Check Products...
                echo.
                python Tests_Check_Products.py
                cd ..
                """
            }
        }

        stage('🧪 Test 2: SauceDemo Test') {
            steps {
                echo '======================================'
                echo '🧪 Exécution: Gestion des Erreurs Connexion'
                echo '======================================'
                echo 'Test: TestSauceDemo.py'
                echo 'Scope: 5 scénarios de connexion'
                echo 'XRAY IDs: QA-201 à QA-205'
                echo '======================================'
                
                bat """
                call venv\\Scripts\\activate.bat
                cd selenium_tests
                chcp 65001
                echo.
                echo Démarrage du test SauceDemo...
                echo.
                python TestSauceDemo.py
                cd ..
                """
            }
        }

        stage('📊 Génération des Rapports') {
            steps {
                echo '======================================'
                echo '📊 Consolidation des rapports HTML'
                echo '======================================'
                
                bat """
                setlocal enabledelayedexpansion
                cd selenium_tests\\reports
                
                echo.
                echo Fichiers de rapport générés:
                dir *.html 2>nul && (
                    for /f %%F in ('dir /b *.html') do (
                        echo   ✅ %%F
                    )
                ) || (
                    echo   ⚠️ Aucun rapport HTML trouvé
                )
                
                cd ../..
                """
            }
        }

        stage('📈 Analyse des Résultats') {
            steps {
                echo '======================================'
                echo '📈 Analyse et synthèse des résultats'
                echo '======================================'
                
                script {
                    bat """
                    call venv\\Scripts\\activate.bat
                    echo.
                    echo Récapitulatif des tests:
                    echo.
                    type selenium_tests\\test_results.json 2>nul || (
                        echo ℹ️ Fichier test_results.json non disponible
                    )
                    echo.
                    """
                }
            }
        }

        stage('📡 Publication des Rapports') {
            steps {
                echo '======================================'
                echo '📤 Publication des rapports'
                echo '======================================'
                
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'selenium_tests/reports',
                    reportFiles: 'test_report_*.html',
                    reportName: '📊 Rapports de Tests HTML'
                ])
                
                echo '✅ Rapports publiés'
            }
        }
    }

    post {
        always {
            echo '======================================'
            echo '📋 Post-Exécution: Nettoyage'
            echo '======================================'
            
            // Archiver tous les rapports
            archiveArtifacts artifacts: 'selenium_tests/reports/**/*.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'selenium_tests/**/*.json', allowEmptyArchive: true
            
            // Afficher le résumé
            bat """
            echo.
            echo ╔══════════════════════════════════════════╗
            echo ║    RÉSUMÉ D'EXÉCUTION DU PIPELINE        ║
            echo ╚══════════════════════════════════════════╝
            echo.
            echo 📅 Date/Heure: %date% %time%
            echo 🔗 Build URL: %BUILD_URL%
            echo 📦 Workspace: %WORKSPACE%
            echo.
            echo 📁 Rapports disponibles dans:
            echo    selenium_tests/reports/
            echo.
            """
        }

        success {
            echo '======================================'
            echo '✅ PIPELINE EXÉCUTÉ AVEC SUCCÈS !'
            echo '======================================'
            echo 'Tous les tests sont passés.'
            echo 'Les rapports HTML sont disponibles.'
            
            // Notification de succès (optionnel)
            bat """
            echo [SUCCESS] Tous les tests QA ont réussi - Rapports disponibles
            """
        }

        failure {
            echo '======================================'
            echo '❌ PIPELINE ÉCHOUÉ !'
            echo '======================================'
            echo 'Certains tests ont échoué.'
            echo 'Veuillez consulter les logs et rapports.'
            
            // Notification d'échec
            bat """
            echo [FAILURE] Des tests QA ont échoué
            echo Consultez les rapports pour plus de détails
            """
        }

        unstable {
            echo '======================================'
            echo '⚠️ PIPELINE EN ÉTAT INSTABLE'
            echo '======================================'
        }

        cleanup {
            echo '🧹 Nettoyage de l\'espace de travail'
            deleteDir()
        }
    }
}

