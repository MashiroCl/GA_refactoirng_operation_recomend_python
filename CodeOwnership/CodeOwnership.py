from .Repository import Repository
import os

class CodeOwnership:
    def __init__(self,repoPath):
        self.repoPath = repoPath
        self.repo = Repository(self.repoPath)
        self.outputPath = os.path.join(self.repoPath,"MORCOoutput")
        self.repo.countAuthorCommit(self.outputPath)


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
