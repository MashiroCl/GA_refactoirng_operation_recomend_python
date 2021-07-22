'File Class represent a java file'
import os
import json
from Commit import Commit
class File():
    def __init__(self,path:str):
        self.path=path
        self.parentPath=None
        self.name=path.split("/")[-1]
        self.log=None
        self.commits=None
        self.commitNum=0
        self.authorCommitDict=dict()
        self.authorCommitDictRatio=dict()
    def setParentPath(self)->str:
        paths=self.path.split("/")
        temp=""
        for i in range(len(paths)-1):
            temp+=paths[i]+"/"
        self.parentPath=temp
        return temp

    def getCommit(self,outputPath:str):
        'git log on current java file and ouput a json format log'
        self.setParentPath()
        self.log=outputPath+"/"+self.name.split(".")[0]+".json"
        prettyFormat="--pretty=format:\'{%n  \"commit\": \"%H\",%n \"subject\": \"%s\",%n \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }%n},\'"
        command="cd "+self.parentPath+" && "+"git log "+prettyFormat+" --follow "+self.name +" >"+ self.log
        os.system(command)

    def json2Commit(self):
        'read git log file (json) and extract info'
        with open(self.log) as f:
            data = json.loads("[" + f.read()[:-1] + "]")
        commits = []
        for each in data:
            commits.append(Commit(each))
        self.commits=commits
        self.commitNum=len(commits)

    def commitAuthorCount(self)->dict:
        for each in self.commits:
            if each.authorName in self.authorCommitDict.keys():
                self.authorCommitDict[each.authorName] += 1
            else:
                self.authorCommitDict[each.authorName] =1


    def commitAuthorRatio(self)->dict:
        for each in self.authorCommitDict:
            self.authorCommitDictRatio[each]=self.authorCommitDict[each]/self.commitNum


if __name__ =="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/src/main/java/net/engio/mbassy/bus/BusRuntime.java"
    f=File(path)
    f.getCommit(outputPath="/Users/leichen/Code/pythonProject/pythonProject/salabResearch/CodeOwnership")
    f.json2Commit()
    f.commitAuthorCount()
    f.commitAuthorRatio()
    print(f.authorCommitDict)
    print(f.authorCommitDictRatio)