pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Chamseddine-svg/UTopia_CSF_ME.git'
            }
        }

        stage('Setup Python') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            # Create virtual environment safely on Linux / WSL
                            python3 -m venv --system-site-packages --prompt env env
                            . env/bin/activate
                            pip install --upgrade pip --break-system-packages
                            pip install -r requirements.txt --break-system-packages
                        '''
                    } else {
                        bat '''
                            REM Create virtual environment on Windows
                            python -m venv env
                            call env\\Scripts\\activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . env/bin/activate
                            pytest tests/selenium --capture=tee-sys --html=selenium_report.html
                        '''
                    } else {
                        bat '''
                            call env\\Scripts\\activate
                            pytest tests\\selenium --maxfail=1 --capture=tee-sys --html=selenium_report.html
                        '''
                    }
                }
            }
        }

        stage('Archive Screenshots & Report') {
            steps {
                archiveArtifacts artifacts: 'screenshots/*', allowEmptyArchive: true
                archiveArtifacts artifacts: 'selenium_report.html', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Tests passed! Screenshots & report archived.'
        }
        failure {
            echo 'Tests failed! Screenshots & report archived.'
        }
    }
}

