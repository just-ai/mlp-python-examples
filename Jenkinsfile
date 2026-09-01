pipeline {
    options {
        gitLabConnection("gitlab just-ai")
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 180, unit: 'MINUTES')
        timestamps()
    }
    agent {
        label 'caila-dev-cloud-agent'
    }

    parameters {
        activeChoice(name: 'COMPONENTS',
                choiceType: 'PT_MULTI_SELECT',
                randomName: 'choice-parameter-components',
                filterable: false,
                filterLength: 1,
                script: groovyScript(
                        script: [classpath: [], sandbox: true, script: '''return ['python-client:selected', 'python-composite-action:selected', 'python-fit-action:selected', 'python-rest-client:selected', 'python-simple-action:selected']'''],
                        fallbackScript: [classpath: [], sandbox: true, script: 'return []']
                ),
                description: '')
    }
    stages {
        stage('notify gitlab') {
            steps {
                updateGitlabCommitStatus name: "build", state: "running"
            }
        }
        stage('Build') {
            steps {
                script {
                    echo "========================================================="
                    echo params.COMPONENTS

                    for (cmp in params.COMPONENTS.split(",")) {
                        stage("Build ${cmp}") {
                            script {
                                echo "========================================================="
                                echo cmp
                                try {
                                    sh """cd ${WORKSPACE}/${cmp} && sh ./build.sh ${env.BRANCH_NAME}"""
                                } catch(Exception e) {
                                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                                        error("build ${cmp} failed.")
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        stage('Merge release to main') {
            when {
                expression {
                    env.BRANCH_NAME == 'release'
                }
            }
            steps {
                sh """git checkout main --force"""
                sh """git pull"""
                sh """git merge origin/release -m 'Automatic merge from release to main'"""
                sh """git push"""
            }
        }
    }
    post {
//        always {
//            cleanWs()
//        }
        failure {
            updateGitlabCommitStatus name: "build", state: "failed"
        }
        success {
            updateGitlabCommitStatus name: "build", state: "success"
        }
        unstable {
            updateGitlabCommitStatus name: "build", state: "failed"
        }
    }
}
