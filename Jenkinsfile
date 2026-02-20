pipeline {
    agent any

    environment {
        IMAGE_NAME = "yogeshwari101/myapp"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Clone Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
                sh 'docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                credentialsId: 'dockerhub',
                usernameVariable: 'USER',
                passwordVariable: 'PASS')]) {

                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push $IMAGE_NAME:$IMAGE_TAG
                    docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }

        stage('Update Kubernetes Image') {
            steps {
                sh '''
                kubectl set image deployment/myapp myapp=$IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }
}
