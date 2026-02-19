pipeline {
    agent any

    environment {
        IMAGE_NAME = "yogeshwari101/notes-app"
        TAG = "latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Pulling code from GitHub..."
                git branch: 'main', url: 'https://github.com/yogeshwari101/Note_taking_application_with_integrated-CI-CD-Pipelines.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t $IMAGE_NAME:$TAG ."
            }
        }

        stage('Docker Hub Login') {
            steps {
                echo "Logging into Docker Hub..."
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "Pushing image to Docker Hub..."
                sh "docker push $IMAGE_NAME:$TAG"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                sh "kubectl set image deployment/notes-app notes-app=$IMAGE_NAME:$TAG --record || kubectl apply -f k8s/deployment.yaml"
            }
        }
    }

    post {
        success {
            echo "Deployment successful!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}

