from code_ownership.Repository import Repository
import os


if __name__ == "__main__":
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/gwt"
    csvPath = os.path.join(repoPath, "MORCOoutput", "ownership.csv_utils")
    commitOutputPath = os.path.join(repoPath, "MORCOoutput")
    csvOutputPath = os.path.join(repoPath, "MORCOoutput", "csv_utils")
    csvName = "ownership.csv_utils"
    localPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data"
    Repository(repoPath).cal_ownerships(commitOutputPath).authorCommitDict2CSV(csvOutputPath, csvName, localPath)



