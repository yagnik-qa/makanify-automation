pipeline {
    agent any

    stages {
        stage('Diagnostics') {
            steps {
                sh '''
                    echo "=== CLI Diagnostics ==="
                    echo "PATH: $PATH"
                    
                    echo "--- checking python3 ---"
                    if command -v python3 >/dev/null 2>&1; then
                        echo "Found python3: $(which python3)"
                        python3 --version
                    else
                        echo "python3 not found"
                    fi

                    echo "--- checking python ---"
                    if command -v python >/dev/null 2>&1; then
                        echo "Found python: $(which python)"
                        python --version
                    else
                        echo "python not found"
                    fi

                    echo "--- checking docker ---"
                    if command -v docker >/dev/null 2>&1; then
                        echo "Found docker: $(which docker)"
                        docker --version
                    else
                        echo "docker not found"
                    fi
                '''
            }
        }
    }
}
