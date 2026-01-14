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
    }

    post {
        success {
            echo 'Pipeline terminee avec succes ! Tous les tests Selenium sont passes.'
        }
        failure {
            echo 'La pipeline a echoue. Verifiez le rapport HTML des tests.'
        }
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
