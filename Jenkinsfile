pipeline {
    agent any  // match your Jenkins agent label

    options {
        timestamps()
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Playwright browser')
        string(name: 'PYTEST_MARKERS', defaultValue: 'smoke', description: 'pytest -m expression; empty = all tests')
        booleanParam(name: 'RUN_PARALLEL', defaultValue: false, description: 'pytest-xdist (use carefully with Playwright)')
    }

    environment {
        PYTHONUNBUFFERED = '1'
        CI = 'true'
        PLAYWRIGHT_BROWSERS_PATH = "${WORKSPACE}/.pw-browsers"
        PLAYWRIGHT_HEADLESS=1
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python & Playwright setup') {
            steps {
                sh '''
                    set -eux
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install --with-deps chromium
                '''
            }
        }

        stage('Inject secrets') {
            steps {
                    // 1. Pull the secure file out of Jenkins' vault
                    withCredentials([file(credentialsId: 'playwright-secret-json', variable: 'SECURE_CREDS')]) {
                        sh '''
                            set -eu

                            # 2. Create the folder structure if it doesn't exist
                            mkdir -p playwright/data

                            # 3. Force-delete any stale/locked credentials file left over from a previous crash
                            rm -f playwright/data/credentials.json

                            # 4. Copy Jenkins' secure file into the exact path your Python code expects
                            cp "$SECURE_CREDS" playwright/data/credentials.json
                        '''
                    }
                }
            }

        stage('Run tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        set -eux
                        . venv/bin/activate
                        mkdir -p reports test-results

                        MARKER_FLAG=""
                        if [ -n "${PYTEST_MARKERS:-}" ]; then
                            pytest -m "${PYTEST_MARKERS}" --html=reports/report.html
                        else
                            pytest --html=reports/report.html
                        fi

                        PARALLEL_FLAG=""
                        if [ "${RUN_PARALLEL}" = "true" ]; then
                          PARALLEL_FLAG="-n auto"
                        fi

                        cd playwright
                        pytest -v $MARKER_FLAG $PARALLEL_FLAG \
                          --browser "${BROWSER}" \
                          --junitxml=../reports/test-results.xml \
                          --html=../reports/report.html --self-contained-html
                    '''
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
            archiveArtifacts artifacts: 'reports/**,test-results/**/*,playwright/test-results/**/*',
                allowEmptyArchive: true, fingerprint: true
            // publishHTML optional: needs HTML Publisher plugin
        }
        success {
            echo 'Tests passed'
        }
        failure {
            echo 'Tests failed — check archived traces/videos under test-results/'
        }
        // Omit cleanWs() if you want to inspect workspace after failure
        // cleanWs()
    }
}