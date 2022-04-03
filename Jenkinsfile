pipeline {
  agent any
  stages {
    stage('Building docker image') {
      steps {
        sh 'sudo docker build -t montechristo .'
      }
    }
    
  
    stage('Running docker image') {
      steps {
        sh "sudo docker run -p 80:80 montechristo"
      }
    }
  }
  
  post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {                   
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}