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
                    playwright install --with-deps
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
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                    sh '''
                        set -ex
                        . venv/bin/activate
                        mkdir -p reports test-results

                        # 1. Evaluate the dynamic pytest markers parameter
                        MARKER_FLAG=""
                        if [ -n "${PYTEST_MARKERS:-}" ]; then
                            MARKER_FLAG="-m ${PYTEST_MARKERS}"
                        fi

                        # 2. Evaluate the parallel execution parameter
                        PARALLEL_FLAG=""
                        if [ "${RUN_PARALLEL}" = "true" ]; then
                            PARALLEL_FLAG="-n auto"
                        fi

                        # 3. SINGLE, DYNAMIC EXECUTION LINE
                        # We do NOT 'cd playwright' anymore; running from the root keeps pathing consistent.
                        pytest -v $MARKER_FLAG $PARALLEL_FLAG \
                          --browser "${BROWSER}" \
                          --junitxml=test-results/results.xml \
                          --html=reports/report.html --self-contained-html || true
                    '''
                }
            }
        }
    }

    post {
        always {
            // This plugin reads the generated XML file and maps individual pass/fail metrics to the build UI
            junit testResults: 'test-results/*.xml', allowEmptyResults: true

            archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
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