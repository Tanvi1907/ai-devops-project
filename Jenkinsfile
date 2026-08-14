pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('gemini-api-key')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Tanvi1907/ai-devops-project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install --break-system-packages -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest test_app.py -v'
            }
        }
    }

    post {
        success {
            echo 'All tests passed successfully!'
        }
        failure {
            echo 'Tests failed. Please check the logs.'
        }
    }
}