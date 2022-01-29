from code_ownership.Repository import Repository
import os

class CodeOwnership:
    def __init__(self,repoPath):
        self.repoPath = repoPath
        self.repo = Repository(self.repoPath)
        self.commitOutputPath = os.path.join(self.repoPath,"MORCOoutput")
        self.csvOutputPath = os.path.join(self.repoPath,"MORCOoutput","csv")
        self.csvName = "ownership.csv"
        self.authorPairList = list()

    def findAuthorPairList(self, decodedBinarySequences):
        '''
        author set is like {{dev1,dev2},{dev2,dev3}}
        one set of 2 developers are the developer who owns the highest ownership for files on which refactoring is applied to
        :param decodedBinarySequences:
        :return:
        '''
        filePaths = []
        for decodedBinarySequence in decodedBinarySequences:
            try:
                filePaths.append(decodedBinarySequence["class1"].getFilePath())
                filePaths.append(decodedBinarySequence["class2"].getFilePath())
            except KeyError:
                pass
            except TypeError:
                pass
        with open(os.path.join(self.csvOutputPath,self.csvName)) as f:
            lines = f.readlines()
        lines = [each.split(",") for each in lines]
        i = 0
        while i < len(filePaths)-1:
            relatedDeveloper = [self._findHighest(filePaths[i], lines), self._findHighest(filePaths[i + 1], lines)]
            self.authorPairList.append(relatedDeveloper)
            i = i + 2
        return self

    def _findHighest(self, filePath:str, ownershipLines: list)->str:
        '''
        find the highest ownership developer in one file
        :param filePath:
        :return:
        '''
        candidates = [each for each in ownershipLines if each[0].strip()==filePath.strip()]
        candidates.sort(key=lambda x: x[2])
        return candidates[0][2]


    def calculateRelationship(self, developerGraph):
        '''

        :param developerGraph:
        :param authorSet: {[dev1,dev2],[dev2,dev3]}
        :return:
        '''
        relationship = 0
        for each in self.authorPairList:
            developerA = each[0]
            developerB = each[1]
            if developerA in developerGraph.vertices.keys():
                if developerB in developerGraph.vertices[developerA].keys():
                    relationship += developerGraph.vertices[developerA][developerB]

        return relationship/(len(self.authorPairList) if len(self.authorPairList)!=0 else 1)



    def calculateOwnership(self, decodedBinarySequences):
        filePath = []
        for decodedBinarySequence in decodedBinarySequences:
            try:
                filePath.append(decodedBinarySequence["class1"].getFilePath())
                filePath.append(decodedBinarySequence["class2"].getFilePath())
            except KeyError:
                pass
            except TypeError:
                pass



        'calculate highest code ownership'
        authorCommitDict = self.repo.getAuthorCommitDict(filePath)
        maxCommitNum=0
        totalCommit = set()
        for eachAuthor in authorCommitDict:
            curCommit = authorCommitDict[eachAuthor]
            curCommitNum = len(curCommit)
            if curCommitNum>maxCommitNum:
                maxCommitNum = curCommitNum
            totalCommit = totalCommit.union(curCommit)
        totalCommitNum=len(totalCommit)
        if totalCommitNum == 0:
            totalCommitNum = 1
        highestOwenership = maxCommitNum/totalCommitNum

        commitersNum = 1
        if len(authorCommitDict)!=0:
            commitersNum=len(authorCommitDict)

        numOfCommiters = 1/commitersNum

        return highestOwenership, numOfCommiters


if __name__=="__main__":
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
    commitOutputPath = os.path.join(repoPath, "MORCOoutput")
    csvOutputPath = os.path.join(repoPath, "MORCOoutput", "csv")
    csvName = "ownership.csv"
    Repository(repoPath).countAuthorCommit(commitOutputPath).authorCommitDict2CSV(csvOutputPath, csvName)
