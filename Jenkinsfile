def testCommand = ""
def slackUser = "@raghav"
def slackChannel = ""
def jenkins
node {
   fileLoader.withGit('https://github.com/jenkins-pipeline-scripts.git', 'master', 'github', '') {
       jenkins = fileLoader.load('jenkins');
   }
}
jenkins.start(testCommand, slackUser, slackChannel)
