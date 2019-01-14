def testCommand = ""
def slackUser = "@raghav"
def slackChannel = "#devops"
def jenkins
node {
   fileLoader.withGit('https://github.com/LimeTray/jenkins-pipeline-scripts.git', 'master', 'limetray-github', '') {
       jenkins = fileLoader.load('jenkins');
   }
}
jenkins.start(testCommand, slackUser, slackChannel)