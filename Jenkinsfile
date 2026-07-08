pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.49.0-jammy'
        }
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                // If secrets/credentials are configured in Jenkins, you can bind them here:
                // withCredentials([usernamePassword(credentialsId: 'makanify-credentials', usernameVariable: 'MAKANIFY_EMAIL', passwordVariable: 'MAKANIFY_PASSWORD')]) {
                sh '''
                    pytest --tracing=retain-on-failure --junitxml=report.xml
                '''
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
