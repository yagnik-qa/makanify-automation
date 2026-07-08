pipeline {
    agent any

    stages {
        stage('Detailed Diagnostics') {
            steps {
                sh '''
                    echo "=== System Info ==="
                    uname -a
                    if [ -f /etc/os-release ]; then
                        cat /etc/os-release
                    fi
                    
                    echo "=== Current User ==="
                    whoami
                    id
                    
                    echo "=== Sudo Access Check ==="
                    if command -v sudo >/dev/null 2>&1; then
                        if sudo -n true >/dev/null 2>&1; then
                            echo "Passwordless sudo is AVAILABLE"
                        else
                            echo "Sudo is installed but requires a password"
                        fi
                    else
                        echo "Sudo is NOT installed"
                    fi

                    echo "=== Package Managers ==="
                    for cmd in apt-get apk yum dnf brew; do
                        if command -v $cmd >/dev/null 2>&1; then
                            echo "Package manager found: $cmd ($(which $cmd))"
                        fi
                    done

                    echo "=== Utilities ==="
                    for cmd in curl wget tar unzip zip gpg; do
                        if command -v $cmd >/dev/null 2>&1; then
                            echo "Utility found: $cmd ($(which $cmd))"
                        fi
                    done
                '''
            }
        }
    }
}
