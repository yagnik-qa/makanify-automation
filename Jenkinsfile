pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            playwright install --with-deps
                        '''
                    } else {
                        bat '''
                            python -m venv .venv
                            call .venv\\Scripts\\activate
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                            playwright install
                        '''
                    }
                }
            }
        }

        stage('Run Playwright Tests') {
            steps {
                // If secrets/credentials are configured in Jenkins, you can bind them here:
                // withCredentials([usernamePassword(credentialsId: 'makanify-credentials', usernameVariable: 'MAKANIFY_EMAIL', passwordVariable: 'MAKANIFY_PASSWORD')]) {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate
                            pytest --tracing=retain-on-failure --junitxml=report.xml
                        '''
                    } else {
                        bat '''
                            call .venv\\Scripts\\activate
                            pytest --tracing=retain-on-failure --junitxml=report.xml
                        '''
                    }
                }
                // }
            }
        }
    }

    post {
        always {
            // Archive JUnit test reports and other artifacts
            junit testResults: 'report.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'screenshots/**, test-results/**, reports/**', allowEmptyArchive: true
        }
    }
}
