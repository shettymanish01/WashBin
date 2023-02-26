pipeline {
    
    agent {
        label 'CICD'
    } 
    
    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
        BUILD_COMMIT = "${GIT_COMMIT}"
        CONTAINER_NAME = "washbin-test-container"
    }
    
    stages {
        
        stage('Checkout'){
           steps {
                git credentialsId: 'washbingit', 
                url: 'https://github.com/shettymanish01/WashBin',
                branch: 'dev'
           }
        }

        stage('Build Docker'){
            steps{
                script{
                    sh '''
                    echo 'Buid Docker Image'
                    docker build -t shettymanish01/testsite:${BUILD_NUMBER} .
                    '''
                }
            }
        }

        stage('Test'){
            steps{
                script{
                    sh '''
                    echo 'Testing'
                    docker container rm -f $CONTAINER_NAME || true
                    docker container run --name $CONTAINER_NAME -d shettymanish01/testsite:${BUILD_NUMBER}
                    docker container exec -t $CONTAINER_NAME /bin/bash
                    curl localhost:5000/health
                    exit             
                    docker container rm -f $CONTAINER_NAME                            
                    '''
                }
            }
        }

        stage('Push the Image'){
           steps{
                script{
                    sh '''
                    echo 'Push to Repo'
                    docker push shettymanish01/testsite:${BUILD_NUMBER}
                    docker image rm shettymanish01/testsite:${BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('Checkout K8S manifest SCM'){
            steps {
                git credentialsId: 'washbingit', 
                url: 'https://github.com/shettymanish01/washbin_deployment.git',
                branch: 'main'
            }
        }

        stage('Update K8S manifest & push to Repo'){
            steps {
                script{
                    withCredentials([usernamePassword(credentialsId: 'washbingit', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                        sh '''
                        cat deploymentservicedev.yaml
                        sed -i '' "s/testsite.*/testsite:${BUILD_NUMBER}/g" deploymentservicedev.yaml
                        cat deploymentservicedev.yaml
                        git add deploymentservicedev.yaml
                        git commit -m 'Updated the deploy yaml | Jenkins Pipeline Dev '
                        git remote -v
                        git push https://github.com/shettymanish01/washbin_deployment.git HEAD:main
                        '''                        
                    }
                }
            }
        }
        
        stage('Deploy to k8s'){
            steps{
                script{
                    kubernetesDeploy (configs: 'deploymentservicedev.yaml',kubeconfigId: 'k8sconfigpwd')
                }
            }
        }
       
    }
}
