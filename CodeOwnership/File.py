'File Class represent a java file'
import os
import json
from Commit import Commit
class File():
    def __init__(self,path:str):
        self.path=path
        self.name=path.split("/")[-1]
        self.parentPath = ("/").join(path.split("/")[:-1])+"/"
        self.logpath=None
        self.commits=None
        self.commitNum=0
        self.authorCommitDict=dict()

    def logCommit(self,outputPath:str):
        '''
        git log on current java file and ouput a json format log
        :param outputPath: output path for git log json file
        :return:
        '''
        self.logpath=outputPath+"/"+self.name.split(".")[0]+".json"
        prettyFormat="--pretty=format:\'{%n  \"commit\": \"%H\",%n \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }%n},\'"
        command="cd "+self.parentPath+" && "+"git log "+prettyFormat+" --follow "+self.name +" >"+ self.logpath
        os.system(command)

        return self

    def json2Commit(self):
        '''
        read git log file (json) and extract info
        :return:
        '''
        with open(self.logpath) as f:
            data = json.loads("[" + f.read()[:-1] + "]")
        commits = []
        for each in data:
            commits.append(Commit(each))
        self.commits=commits
        self.commitNum=len(commits)
        return self

    def fillAuthorCommitDict(self):
        '''
        filled author commit dict with dict like {authorName: {commitId 1, commitId 2}}
        using git log info in cur file
        :return:
        '''
        for each in self.commits:
            if each.authorName not in self.authorCommitDict.keys():
                self.authorCommitDict[each.authorName] = set()
            self.authorCommitDict[each.authorName].add(each.commitID)
        return self



if __name__ =="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/src/main/java/net/engio/mbassy/bus/BusRuntime.java"
    f=File(path)
    print(f.parentPath)
    print(("/").join(path.split("/")[:-1]))
    # f.getCommit(outputPath="/Users/leichen/Code/pythonProject/pythonProject/salabResearch/CodeOwnership")
    # f.json2Commit()
    # f.commitAuthorCount()
    # f.commitAuthorRatio()
    # print(f.authorCommitDict)
    # print(f.authorCommitDictRatio)
