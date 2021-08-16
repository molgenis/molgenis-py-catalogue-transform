pipeline {
    agent {
        kubernetes {
            label 'python-stretch'
        }
    }
    environment {
        REPOSITORY = 'molgenis/molgenis-py-catalogue-transform'
        LOCAL_REPOSITORY = "${LOCAL_REGISTRY}/molgenis/catalogue-transform"
    }
    stages {
        stage('Prepare') {
            when {
                allOf {
                    not {
                        changelog '.*\\[skip ci\\]$'
                    }
                }
            }
            steps {
                script {
                    env.GIT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                }
                container('vault') {
                    script {
                        env.GITHUB_TOKEN = sh(script: 'vault read -field=value secret/ops/token/github', returnStdout: true)
                        env.NEXUS_AUTH = sh(script: 'vault read -field=base64 secret/ops/account/nexus', returnStdout: true)
                        env.SONAR_TOKEN = sh(script: 'vault read -field=value secret/ops/token/sonar', returnStdout: true)
                        env.DOCKERHUB_AUTH = sh(script: 'vault read -field=value secret/gcc/token/dockerhub', returnStdout: true)
                    }
                }
                sh "git remote set-url origin https://${GITHUB_TOKEN}@github.com/${REPOSITORY}.git"
                sh "git fetch --tags"
                container('python') {
                    sh "python -m pip install python-semantic-release"
                }
            }
        }
        stage('Build: [ pull request ]') {
            when {
                changeRequest()
            }
            environment {
                TAG = "PR-${CHANGE_ID}-${BUILD_NUMBER}"
                DOCKER_CONFIG="/root/.docker"
            }
            steps {
                container('sonar') {
                    sh "sonar-scanner -Dsonar.github.oauth=${env.GITHUB_TOKEN} -Dsonar.pullrequest.base=${CHANGE_TARGET} -Dsonar.pullrequest.branch=${BRANCH_NAME} -Dsonar.pullrequest.key=${env.CHANGE_ID} -Dsonar.pullrequest.provider=GitHub -Dsonar.pullrequest.github.repository=molgenis/molgenis-py-catalogue-transform"
                }
            }
        }
        stage('Release: [ master ]') {
            when {
                allOf {
                    branch 'master'
                    not {
                        changelog '.*\\[skip ci\\]$'
                    }
                }
            }
            environment {
                REPOSITORY = 'molgenis/molgenis-py-catalogue-transform'
                GIT_AUTHOR_EMAIL = 'molgenis+ci@gmail.com'
                GIT_AUTHOR_NAME = 'molgenis-jenkins'
                GIT_COMMITTER_EMAIL = 'molgenis+ci@gmail.com'
                GIT_COMMITTER_NAME = 'molgenis-jenkins'
                DOCKER_CONFIG = '/root/.docker'
            }
            steps {
                milestone 1
                container('sonar') {
                    sh "sonar-scanner"
                }
                container('python') {
                    sh "git remote set-url origin https://${GITHUB_TOKEN}@github.com/${REPOSITORY}.git"
                    sh "git checkout -f master"
                    sh "git fetch --tags"
                    script {
                        env.TAG = sh(script: 'semantic-release print-version', returnStdout: true)
                    }
                    sh "semantic-release publish -D commit_subject=\"${TAG} [skip ci]\""
                }
                container (name: 'kaniko', shell: '/busybox/sh') {
                    sh "#!/busybox/sh\nmkdir -p ${DOCKER_CONFIG}"
                    sh "#!/busybox/sh\necho '{\"auths\": {\"registry.molgenis.org\": {\"auth\": \"${NEXUS_AUTH}\"}, \"https://index.docker.io/v1/\": {\"auth\": \"${DOCKERHUB_AUTH}\"}, \"registry.hub.docker.com\": {\"auth\": \"${DOCKERHUB_AUTH}\"}}}' > ${DOCKER_CONFIG}/config.json"
                    sh "#!/busybox/sh\n/kaniko/executor --context ${WORKSPACE} --destination ${REPOSITORY}:${TAG}"
                }
            }
            post {
                success {
                    molgenisSlack(message:  ":confetti_ball: Released ${REPOSITORY} v${TAG}. See https://github.com/${REPOSITORY}/releases/tag/v${TAG}", color:'good')
                }
                failure {
                    molgenisSlack(message:  ":cry: Failed to release ${REPOSITORY}", color:'bad')
                }
            }
        }
    }
}