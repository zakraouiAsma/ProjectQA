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
                sh '''
                python${PYTHON_VERSION} -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest pytest-html selenium
                '''
            }
        }

        stage('Exécuter les tests Selenium') {
            steps {
                sh '''
                source venv/bin/activate
                mkdir -p reports
                pytest selenium_tests/ --html=reports/rapport_selenium.html --self-contained-html -v
                '''
            }
        }

        stage('Publier le rapport HTML') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'rapport_selenium.html',
                    reportName: 'Rapport Selenium HTML'
                ])
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminée avec succès ! Tous les tests Selenium sont passés.'
        }
        failure {
            echo 'La pipeline a échoué. Vérifiez le rapport HTML des tests.'
        }
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
