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
                chcp 65001
                pytest selenium_tests --html=reports/rapport_selenium.html --self-contained-html > reports/test_execution.log 2>&1
                """
            }
        }

        stage('Afficher rapport') {
            steps {
                script {
                    echo '======================================'
                    echo 'Rapport Selenium: reports/rapport_selenium.html'
                    echo 'Logs tests: reports/test_execution.log'
                    echo '======================================'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline terminee avec SUCCES !'
        }
        failure {
            echo 'Pipeline ECHOUEE - Verifiez les logs et rapports.'
        }
    }
}
