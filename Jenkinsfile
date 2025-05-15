pipeline {
    agent any

    environment {
        IMAGE_NAME = "weather_app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/berkustuner/weather_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh 'docker stop weather_app || true'
                sh 'docker rm weather_app || true'
                sh 'docker run -d -p 5000:5000 --name weather_app $IMAGE_NAME'
            }
        }
    }

    triggers {
        githubPush()
    }
}

