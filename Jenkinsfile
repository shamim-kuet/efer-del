pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('push repo to remote dev server host') {
            steps {
                echo 'connect to remote dev server and pull down the latest version'
                sh ' ssh bmp-server@114.130.89.227 "cd /var/www/dev/bmp-efranchise-python; \
                     source env/bin/activate; \
                     git pull origin devops; \
                     pip install -r requirements.txt --no-warn-script-location; \
                     python manage.py migrate; \
                     deactivate; \
                     sudo systemctl restart nginx.service; \
                     sudo systemctl restart gunicorn " '
            }
        }
        stage('Check dev website is up') {
            steps {
                echo 'Check dev website is up'
                sh 'curl -Is https://dev.efeh.britishmarketplace.co.uk/ | head -n 1'
            }
        }
    }
}
