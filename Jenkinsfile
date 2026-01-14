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

        stage('Generer rapport Jenkins') {
            steps {
                script {
                    def logContent = readFile('reports/test_execution.log').take(10000).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
                    
                    def htmlReport = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Rapport Tests Selenium - Jenkins</title>
                        <style>
                            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
                            .header { background-color: #333; color: white; padding: 20px; border-radius: 5px; }
                            .section { background-color: white; padding: 20px; margin: 15px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                            .section h2 { color: #333; border-bottom: 2px solid #0088cc; padding-bottom: 10px; }
                            .logs { background-color: #f0f0f0; padding: 15px; border-radius: 3px; font-family: monospace; white-space: pre-wrap; word-wrap: break-word; max-height: 600px; overflow-y: auto; border-left: 4px solid #0088cc; }
                            .footer { text-align: center; color: #666; margin-top: 30px; }
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <h1>Rapport d'Execution des Tests Selenium</h1>
                            <p>Build Jenkins: ${BUILD_NUMBER}</p>
                            <p>URL du Build: ${BUILD_URL}</p>
                        </div>
                        
                        <div class="section">
                            <h2>Logs d'Execution (extrait)</h2>
                            <div class="logs">${logContent}</div>
                        </div>
                        
                        <div class="footer">
                            <p>Rapport genere automatiquement par Jenkins</p>
                            <p>Date: ${new Date()}</p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    writeFile file: 'reports/jenkins_rapport.html', text: htmlReport
                    echo 'Rapport Jenkins genere avec succes!'
                }
            }
        }
    }

    post {
        always {
            script {
                // Afficher un résumé et archiver les rapports
                archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true

                echo '======================================'
                echo 'RESUME DE L EXECUTION'
                echo '======================================'
                if (fileExists('reports/rapport_selenium.html')) {
                    echo '[OK] Rapport Selenium genere: reports/rapport_selenium.html'
                }
                if (fileExists('reports/jenkins_rapport.html')) {
                    echo '[OK] Rapport Jenkins genere: reports/jenkins_rapport.html'
                }
                if (fileExists('reports/test_execution.log')) {
                    echo '[OK] Fichier log sauvegarde: reports/test_execution.log'
                }
                echo '======================================'
            }
        }
        success {
            echo 'Pipeline terminee avec SUCCES !'
        }
        failure {
            echo 'Pipeline ECHOUEE - Verifiez les logs et rapports.'
        }
    }
}
