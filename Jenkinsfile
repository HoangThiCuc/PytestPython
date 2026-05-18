pipeline {
    // You can specify a specific agent if you have docker, but 'any' works for standard setups
    agent any

    environment {
        // Keeps Python console output from being buffered so you see it in real-time
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Automatically pulls the code from the repo where this Jenkinsfile lives
                checkout scm
            }
        }

        stage('Setup Environment & Playwright') {
            steps {
                sh '''
                // Create and activate virtual environment
                python3 -m venv venv
                . venv/bin/activate

                // Upgrade pip and install dependencies
                pip install --upgrade pip
                pip install -r requirements.txt

                // CRITICAL FOR CI: Install Playwright browsers and OS-level dependencies
                playwright install --with-deps chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                // We wrap this in a catchError so the pipeline continues to the 'post' section even if tests fail
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                    . venv/bin/activate
                    // Run pytest, generate JUnit XML, and output Playwright artifacts to a specific folder
                    pytest -v --junitxml=reports/test-results.xml --output=test-results/
                    '''
                }
            }
        }
    }

    post {
        always {
            // 1. Publish the Pytest XML report to the Jenkins UI
            junit 'reports/test-results.xml'

            // 2. Archive Playwright artifacts (traces, videos, screenshots) if any were generated
            archiveArtifacts artifacts: 'test-results/**/*', allowEmptyArchive: true

            // 3. Clean up the workspace so the Jenkins server doesn't run out of disk space over time
            cleanWs()
        }
    }
}