pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
            sh 'echo "building the repo"'
        }
      }
    
    stage('Installing dependencies') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    
  
    stage('Deploy')
    {
      steps {
        echo "deploying the application"
        sh "sudo python3 app.py"
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