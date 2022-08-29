from Repository import Repository
from PullRequestService import PullRequestService
from DeveloperGraph import DeveloperGraph
from jxplatform2.Jxplatform2 import Jxplatform2
import os


class Starter:
    def extract_codeOwnership(self, repo:str):
        repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/"+repo
        csvPath = os.path.join(repoPath, "MORCOoutput", "ownership.csv")
        commitOutputPath = os.path.join(repoPath, "MORCOoutput")
        csvOutputPath = os.path.join(repoPath, "MORCOoutput", "csv")
        if not os.path.exists(csvOutputPath):
            os.makedirs(csvOutputPath)
        csvName = "ownership.csv"
        localPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data"
        Repository(repoPath).countAuthorCommit(commitOutputPath).authorCommitDict2CSV(csvOutputPath, csvName, localPath).extract_owner_csv()

    def extract_pullRequest(self, repo, repoURL:str, output:str):
        "use the java script"
        # repo = "jeromq"
        # repoURL = "https://github.com/zeromq/jeromq"
        # output = os.path.join("/Users/leichen/ResearchAssistant/InteractiveRebase/data/", repo, "/MORCOoutput/csv/pullrequest.csv")


    def build_developerGraph(self, repo:str):
        "Remember to set the start date and end date"
        relationshipCsvPath = os.path.join("/Users/leichen/ResearchAssistant/InteractiveRebase/data/", repo, "MORCOoutput/csv/pullrequest.csv")
        res = PullRequestService().loadPullRequest(relationshipCsvPath)
        developerGraph = DeveloperGraph(res)
        developerGraph.set_bd_line("2011-12-24","2022-12-24")
        developerGraph.generate_vertices().build()
        return developerGraph

    def jxplatform2(self, repo:str):
        # repoName = sys.argv[1]
        # j="/Users/leichen/Code/pythonProject/pythonProject/salabResearch/Jxplatform2/JxplatformExtract.jar"
        j = "/Users/leichen/Desktop/JxplatformExtract.jar"
        # j = "/home/chenlei/MORCO/MORCOpy/Jxplatform2/JxplatformExtract.jar"
        t = os.path.join("/Users/leichen/ResearchAssistant/InteractiveRebase/data/", repo)
        # t="/Users/leichen/ResearchAssistant/InteractiveRebase/data/ganttproject-1.10.2"
        # t="/home/chenlei/MORCO/data/"+repoName
        c = t
        outputPath = "/Users/leichen/Desktop/jeromq.json"
        # outputPath="/home/chenlei/MORCO/extractResult/"+repoName+".json"
        jx = Jxplatform2(j, t, c, outputPath)
        jx.extractInfo()

if __name__ == "__main__":
    starter = Starter()
    starter.extract_codeOwnership("quasar")
    # res = starter.build_developerGraph("javapoet")
    # print(res.vertices)
