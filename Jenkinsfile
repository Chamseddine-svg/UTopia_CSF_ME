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
                sh '''
                    python3 -m venv env
                    . env/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    . env/bin/activate
                    pytest tests/selenium --maxfail=1 --capture=tee-sys --html=selenium_report.html
                '''
            }
        }

        stage('Archive Screenshots & Report') {
            steps {
                archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
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

