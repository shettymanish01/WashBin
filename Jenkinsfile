pipeline {
    
    agent any 
    
    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        
        stage('Checkout'){
           steps {
                git credentialsId: 'washbingit', 
                url: 'https://github.com/shettymanish01/WashBin',
                branch: 'master'
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

        stage('Push the artifacts'){
           steps{
                script{
                    sh '''
                    echo 'Push to Repo'
                    docker push shettymanish01/testsite:${BUILD_NUMBER}
                    '''
                }
            }
        }
        
        
        stage('Update K8S manifest'){
            steps {
                script{
                    sh '''
                    cat deploymentservice.yaml
                    sed -i '' "s/latest/${BUILD_NUMBER}/g" deploymentservice.yaml
                    cat deploymentservice.yaml
                    '''                        
                }
            }
        }

        stage('Deploy to k8s'){
            steps{
                script{
                    kubernetesDeploy (configs: 'deploymentservice.yaml',kubeconfigId: 'k8sconfigpwd')
                }
            }
        }
    }
}