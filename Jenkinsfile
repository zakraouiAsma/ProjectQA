pipeline {
    agent any

    environment {
        PYTHON_VERSION = "3.11"
    }

    stages {
        stage('Checkout du code') {
            steps {
                git branch: 'main', url: 'https://github.com/zakraouiAsma/ProjectQA'
            }
        }

        stage('Setup Python') {
            steps {
                bat """
                python -m venv venv
                call venv\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                pip install pytest pytest-html selenium
                """
            }
        }

        stage('Exécuter les tests Selenium') {
            steps {
                bat """
                call venv\\Scripts\\activate.bat
                if not exist reports mkdir reports
                python selenium_tests\\Tests_Check_Products.py
                """ 
            }
        }

        stage('Generer rapport HTML') {
            steps {
                script {
                    // Verifier si le rapport HTML existe
                    if (fileExists('reports/rapport_selenium.html')) {
                        echo 'Rapport HTML detecte avec succes !'
                    } else {
                        echo 'Attention: Rapport HTML non trouve'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminee avec succes ! Tous les tests Selenium sont passes.'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
        failure {
            echo 'La pipeline a echoue. Verifiez le rapport HTML des tests.'
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
        always {
            // Archiver tous les rapports et screenshots
            archiveArtifacts artifacts: 'reports/**, selenium_tests/*.png', allowEmptyArchive: true
            
            // Afficher le resultat
            script {
                if (fileExists('reports/rapport_selenium.html')) {
                    echo '======================================'
                    echo 'Rapport HTML genere avec succes !'
                    echo 'Localisation: reports/rapport_selenium.html'
                    echo '======================================'
                } else {
                    echo 'Attention: Aucun rapport HTML genere'
                }
            }
        }
    }
}
