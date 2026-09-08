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
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'k8s-jenkins-token',
                        variable: 'K8S_TOKEN'
                    )
                ]) {
                    sh '''
                        kubectl config set-cluster cluster1 \
                        --server=https://192.168.56.11:6443 \
                        --insecure-skip-tls-verify=true

                        kubectl config set-credentials jenkins \
                        --token="$K8S_TOKEN"

                        kubectl config set-context jenkins-context \
                        --cluster=cluster1 \
                        --user=jenkins \
                        --namespace=order-system

                        kubectl config use-context jenkins-context

                        helm upgrade order-api cluster1/order-api/helm/order-api \
                            -n order-system \
                            --set image.repository=${IMAGE_NAME} \
                            --set image.tag=${BUILD_NUMBER}


                        kubectl rollout status deployment/order-api \
                        -n order-system \
                        --timeout=120s
                    '''
                }
            }
        }
    //     stage('Show Image') {
    //         steps {
    //             sh '''
    //                 echo "================================"
    //                 echo "Build Number: ${BUILD_NUMBER}"
    //                 echo "Image: ${IMAGE_NAME}:${BUILD_NUMBER}"
    //                 echo "================================"

    //                 docker images ${IMAGE_NAME}
    //             '''
    //         }
    //     }
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