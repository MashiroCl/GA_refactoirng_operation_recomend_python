'File Class represent a java file'
import os
import json
from CodeOwnership.Commit import Commit
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
        '''
        git log on current java file and ouput a json format log
        :param outputPath: output path for git log json file
        :return:
        '''
        self.setParentPath()
        self.log=outputPath+"/"+self.name.split(".")[0]+".json"
        # print(self.path)
        # print(self.name)
        # print(self.log)
        # prettyFormat="--pretty=format:\'{%n  \"commit\": \"%H\",%n \"subject\": \"%s\",%n \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }%n},\'"
        prettyFormat="--pretty=format:\'{%n  \"commit\": \"%H\",%n \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }%n},\'"
        command="cd "+self.parentPath+" && "+"git log "+prettyFormat+" --follow "+self.name +" >"+ self.log
        os.system(command)

    def json2Commit(self):
        '''
        read git log file (json) and extract info
        :return:
        '''
        with open(self.log) as f:
            data = json.loads("[" + f.read()[:-1] + "]")
        commits = []
        for each in data:
            commits.append(Commit(each))
        self.commits=commits
        self.commitNum=len(commits)

    def commitAuthorCount(self):
        '''
        count number of each authors' appearence in current file and save results in authorCommitDict
        :return:
        '''
        for each in self.commits:
            if each.authorName in self.authorCommitDict.keys():
                self.authorCommitDict[each.authorName] += 1
            else:
                self.authorCommitDict[each.authorName] =1


    def commitAuthorRatio(self):
        '''
        calculate each authors' ownership ratio in crrent file and save results in authorCommitDictRatio
        :return:
        '''
        for each in self.authorCommitDict:
            self.authorCommitDictRatio[each]=self.authorCommitDict[each]/self.commitNum


    def getHighestOwnership(self)->float:
        '''
        find the highest ratio of ownership
        :return: highest ratio
        '''
        max = -1
        for each in self.authorCommitDictRatio:
            if self.authorCommitDictRatio[each] > max:
                max = self.authorCommitDictRatio[each]
        return max

if __name__ =="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/src/main/java/net/engio/mbassy/bus/BusRuntime.java"
    f=File(path)
    f.getCommit(outputPath="/Users/leichen/Code/pythonProject/pythonProject/salabResearch/CodeOwnership")
    f.json2Commit()
    f.commitAuthorCount()
    f.commitAuthorRatio()
    print(f.authorCommitDict)
    print(f.authorCommitDictRatio)
