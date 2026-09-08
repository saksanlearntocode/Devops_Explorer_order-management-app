pipeline {
    agent any

    environment {
        IMAGE_NAME = "sandsang/order-api"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                        ./cluster1/order-api
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKER_USER" \
                            --password-stdin

                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}

                        docker tag \
                            ${IMAGE_NAME}:${BUILD_NUMBER} \
                            ${IMAGE_NAME}:latest

                        docker push ${IMAGE_NAME}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Show Image') {
            steps {
                sh '''
                    echo "================================"
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Image: ${IMAGE_NAME}:${BUILD_NUMBER}"
                    echo "================================"

                    docker images ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        success {
            echo "CI Pipeline completed successfully!"
            echo "Image: ${IMAGE_NAME}:${BUILD_NUMBER}"
        }

        failure {
            echo "CI Pipeline failed!"
        }
    }
}