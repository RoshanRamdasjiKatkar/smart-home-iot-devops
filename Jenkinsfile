pipeline {
    agent any

    environment {
        GCP_VM_USER = 'root'
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('2. Quality Gate: Pytest') {
            steps {
                sh '''
                    python3 -m venv venv || virtualenv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    PYTHONPATH=. pytest tests/ -v
                '''
            }
        }

        stage('3. SSH Deployment to Production VM') {
            steps {
                sshagent(['gcp-vm-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${GCP_VM_USER}@localhost "
                            mkdir -p ~/smart-home
                            docker stop iot-backend || true
                            docker rm iot-backend || true
                            docker run -d --name iot-backend --restart unless-stopped -p 8000:8000 -v /var/lib/jenkins/workspace/cicd:/app -w /app python:3.11-slim bash -c 'pip install fastapi uvicorn pydantic && uvicorn app.main:app --host 0.0.0.0 --port 8000'
                        "
                    """
                }
            }
        }
    }

    post {
        success {
            echo "CI/CD Pipeline Successful: Pytest Passed & Microservices Live on GCP!"
        }
        failure {
            echo "Pipeline Failed! Check stage logs."
        }
    }
}