import csv
from DeveloperGraph import DeveloperGraph
from PullRequestService import PullRequestService
from CodeOwnership import CodeOwnership

class CSVoperation:
    '''
    conduct operation on csv to change author name (the same author use different name when submittinng commit)
    '''
    def __init__(self,csvPath:str):
        self.csv = None
        self.lines = list()
        try:
             with open(csvPath) as f:
                 self.lines = list(filter(lambda x:len(x[0])!=0,[each.split(",") for each in f.read().split("\n")[1:]]))
        except FileNotFoundError:
            print("no such file",csvPath)

    def replaceAuthorName(self, old:str, new:str):
        for i in range(len(self.lines)):
            if self.lines[i][2] == old:
                self.lines[i][2] = new
        return self

    def rowMerge(self):
        newLines = list()
        self.lines.sort(key=lambda x: (x[0], x[2]))
        i=0
        while i < (len(self.lines)):
            merged_line = self.lines[i];
            i = i + 1
            while(i<len(self.lines) and self.lines[i][0]==merged_line[0] and self.lines[i][2]==merged_line[2]):
                for j in range(3,5):
                    merged_line[j] = float(merged_line[j]) +  float(self.lines[i][j])
                i = i + 1
            merged_line[3] = float(merged_line[4])/float(merged_line[5])
            newLines.append(merged_line)
        self.lines = newLines
        return self

    def write2csv(self,newcsvPath:str):
        with open(newcsvPath,"w") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["File Path","File Name","Author Name","Ownership","commits","total commits"])
            writer.writerows(self.lines)
        return self


if __name__ == "__main__":
    '''
    1. Use code in main function in CodeOwnership.py to extract a csv
    2. Use code below to conduct operations on that csv
    3. Use java code to extract pullrequest.csv
    4. Build DeveloperGraph and extract info into a csv
    
    '''
    'Before GA, code csv about ownership should be generated' \
    'This generation must be done before GA'

    'conduct operations if needed'
    # ownershipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/ownership.csv"
    # newCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/ownership.csv"
    # CSVoperation(ownershipCsvPath).replaceAuthorName("benjamin", "bennidi").rowMerge().write2csv(newCsvPath)

    relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/pullrequest.csv"
    res = PullRequestService().loadPullRequest(relationshipCsvPath)
    developerGraph = DeveloperGraph(res).generate_vertices().build()

    # CodeOwnership().findAuthorSet(decodedBinarySequences=).calculateRelationship(developerGraph)
