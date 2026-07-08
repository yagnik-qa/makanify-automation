pipeline {
    agent any

    environment {
        // Define path to our custom Python installation and add it to PATH
        PATH = "${WORKSPACE}/tools/python/bin:${PATH}"
    }

    stages {
        stage('Setup Portable Python') {
            steps {
                sh '''
                    if [ ! -d "tools/python" ]; then
                        echo "Downloading portable Python 3.11..."
                        mkdir -p tools
                        curl -L "https://github.com/astral-sh/python-build-standalone/releases/download/20240726/cpython-3.11.9+20240726-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz" -o tools/python.tar.gz
                        
                        echo "Extracting Python..."
                        tar -xzf tools/python.tar.gz -C tools/
                        rm tools/python.tar.gz
                    fi
                    echo "Python location: $(which python3)"
                    python3 --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    echo "Installing Playwright Chromium browser and its OS system dependencies..."
                    playwright install chromium --with-deps
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
