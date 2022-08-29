from code_ownership.Repository import Repository
import os


class CodeOwnership:
    '''
    search author pair list according to decoded sequence
    calculate relationship according to author pair list and developer graph
    '''

    def __init__(self, repo_path, ownership_csv_path):
        self.repo_path = repo_path
        self.repo = Repository(self.repo_path)
        self.ownership_csv_path = ownership_csv_path
        self.authorPairList = list()
        self.filepath_owner_map = {}
        with open(self.ownership_csv_path) as f:
            owners_lines = [each.split(",") for each in f.readlines()]
            # each[0]:file path, each[2] owner name
            for each in owners_lines:
                self.filepath_owner_map[each[0]] = each[2]

    def findAuthorPairList(self, decodedSequences):
        '''
        author set is like {{dev1,dev2},{dev2,dev3}}
        one set of 2 developers are the developers who own the highest ownership for the 2 files on which refactoring is applied to
        :param decodedBinarySequences:
        :return:
        '''
        filePaths = []
        for decodedSequence in decodedSequences:
            try:
                filePaths.append(decodedSequence["class1"].getFilePath())
                filePaths.append(decodedSequence["class2"].getFilePath())
            except KeyError:
                print(" class not exist in decoded sequence findAuthorPairList")
            except TypeError:
                print(" type error decoded sequence findAuthorPairList")
        'find owner of the 2 files in owner.csv'
        i = 0
        while i < len(filePaths) - 1:
            relatedDeveloper = [self.filepath_owner_map[filePaths[i]], self.filepath_owner_map[filePaths[i + 1]]]
            self.authorPairList.append(relatedDeveloper)
            i = i + 2
        return self

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
            relationship += self.fuzzy_compare(developerA, developerB, developerGraph)
        return relationship / (len(self.authorPairList) if len(self.authorPairList) != 0 else 1)

    def name_process(self, name: str):
        return name.strip().replace(" ", "").replace("-", "").lower()

    def fuzzy_compare(self, devA, devB, developerGraph):
        '''
        check if devA and devB is in developerGraph or not
        '''
        devA = self.name_process(devA)
        devB = self.name_process(devB)
        # id devA and devB are the same person who has never appears in pull request (example in mbassador: benni & benni)
        if devA == devB:
            return 1
        if devA in developerGraph.vertices.keys():
            if devB in developerGraph.vertices[devA].keys():
                return developerGraph.vertices[devA][devB]
        return 0

    @DeprecationWarning
    def calculateOwnership(self, decodedBinarySequences):
        '''
        Warning: this method is no longer support, the calculation of ownership is useless
        :param decodedBinarySequences:
        :return:
        '''
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
        maxCommitNum = 0
        totalCommit = set()
        for eachAuthor in authorCommitDict:
            curCommit = authorCommitDict[eachAuthor]
            curCommitNum = len(curCommit)
            if curCommitNum > maxCommitNum:
                maxCommitNum = curCommitNum
            totalCommit = totalCommit.union(curCommit)
        totalCommitNum = len(totalCommit)
        if totalCommitNum == 0:
            totalCommitNum = 1
        highestOwenership = maxCommitNum / totalCommitNum

        commitersNum = 1
        if len(authorCommitDict) != 0:
            commitersNum = len(authorCommitDict)

        numOfCommiters = 1 / commitersNum

        return highestOwenership, numOfCommiters


if __name__ == "__main__":
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/atomix"
    csvPath = os.path.join(repoPath, "MORCOoutput", "ownership.csv")
    commitOutputPath = os.path.join(repoPath, "MORCOoutput")
    csvOutputPath = os.path.join(repoPath, "MORCOoutput", "csv")
    csvName = "ownership.csv"
    localPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data"
    Repository(repoPath).countAuthorCommit(commitOutputPath).authorCommitDict2CSV(csvOutputPath, csvName, localPath)
