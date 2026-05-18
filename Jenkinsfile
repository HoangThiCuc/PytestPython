pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment & Playwright') {
            steps {
                sh '''
                # Create and activate virtual environment
                python3 -m venv venv
                . venv/bin/activate

                # Upgrade pip and install dependencies
                pip install --upgrade pip
                pip install -r requirements.txt

                # CRITICAL FOR CI: Install Playwright browsers and OS-level dependencies
                playwright install --with-deps chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                    . venv/bin/activate
                    # Run pytest, generate JUnit XML, and output Playwright artifacts
                    pytest -v --junitxml=reports/test-results.xml --output=test-results/
                    '''
                }
            }
        }
    }

    post {
        always {
            // It is safe to use double-slashes here because we are back in Groovy, not Bash!

            // 1. Publish the Pytest XML report to the Jenkins UI (allowEmpty prevents crash if tests never run)
            junit allowEmptyResults: true, testResults: 'reports/test-results.xml'

            // 2. Archive Playwright artifacts (traces, videos, screenshots) if any were generated
            archiveArtifacts artifacts: 'test-results/**/*', allowEmptyArchive: true

            // 3. Clean up the workspace so the Jenkins server doesn't run out of disk space
            cleanWs()
        }
    }
}