from code_ownership.File import File
import glob
import csv
from utils import create_folder
from os.path import join


class Repository:
    def __init__(self, path: str):
        self.path = path
        self.name = path.split("/")[-1]
        self.files = list()
        # self.files = [each for each in glob.glob(self.path+'/**/*.java',recursive=True)]
        self.csvPath = ""
        self._findJavaFiles()

    def _findJavaFiles(self):
        '''
        find all .java files in current directory
        :return:
        '''
        javaFiles = glob.glob(self.path + '/**/*.java', recursive=True)
        for each in javaFiles:
            self.files.append(File(each))
        return self

    def countAuthorCommit(self, outputPath: str):
        '''
        for each file in the repository use git command to obtain commit and save results in outputPath,
        and calculate count of authors' appearance and ratio of it
        :param outputPath:
        :return:
        '''
        for each in self.files:
            each.logCommit(outputPath).json2Commit().fillAuthorCommitDict()

        return self

    def authorCommitDict2CSV(self, csvPath: str, csvName: str, localPath: str):
        '''
        wirte extraction info of all files into a csv file
        :param outputPath: output path for csv file
        :param localPath: parent path for repo path
        :return:
        '''
        create_folder(csvPath, False)
        csvPath = join(csvPath, csvName)
        result = []
        for eachFile in self.files:
            for eachAuthor in eachFile.authorCommitDict:
                temp = []
                'exclude path on my local computer'
                temp.append(eachFile.path.split(localPath)[1])
                temp.append(eachFile.name)
                temp.append(eachAuthor)
                temp.append(float(len(eachFile.authorCommitDict[eachAuthor])) / float(eachFile.commitNum))
                temp.append(len(eachFile.authorCommitDict[eachAuthor]))
                temp.append(eachFile.commitNum)
                result.append(temp)
        with open(csvPath, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["File Path", "File Name", "Author Name", "Ownership", "commits", "total commits"])
            writer.writerows(result)
        self.csvPath = csvPath
        return self

    def _getCSVLine(self, filePath: str) -> list:
        try:
            with open(self.csvPath) as f:
                reader = csv.reader(f)
                rows = [row for row in reader]
        except FileNotFoundError:
            print("No such file as {}".format(filePath))
        result = []
        for each in rows[1:]:
            if each[0] == filePath:
                result.append(each)
        return result

    def getOwnership(self, filePath: str, name: str) -> float:
        '''
        get ownership from csv file
        :param filePath: csv file
        :param name: author name
        :return:
        '''
        lists = self._getCSVLine(filePath)
        for each in lists:
            if each[2] == name:
                return each[3]
        return 0

    def getContribution(self, filePath: str, name: str) -> int:
        '''
        return number of commit $name commits in file $filePath
        :param filePath:
        :param name:
        :return:
        '''
        lists = self._getCSVLine(filePath)
        for each in lists:
            if each[2] == name:
                return each[4]
        return 0

    def getTotalCommits(self, filePath: str) -> int:
        '''
        return total number of commits in file $filePath
        :param filePath:
        :return:
        '''
        lists = self._getCSVLine(filePath)
        return lists[0][5]

    def getAuthorCommitDict(self, filePath: list):
        '''
        get the highest ownership in list of filePath and filePath2 calculated by searching the highest value for
        commit by DevA/ commitNumInFilePath1 + commitNumInFilePath1
        :param filePath: list of file path
        :return: author commit dict
        '''
        'Find file of filePath'
        aCD = dict()
        for eachFile in self.files:
            if eachFile.path in filePath:
                for eachCommiter in eachFile.authorCommitDict:
                    if eachCommiter in aCD:
                        aCD[eachCommiter] = aCD[eachCommiter].union(eachFile.authorCommitDict[eachCommiter])
                    else:
                        aCD[eachCommiter] = eachFile.authorCommitDict[eachCommiter]
        return aCD

    def extract_owner_csv(self):
        '''
        find the highest ownership developer in one java file and export them into another csv
        :param filePath:
        :return:
        '''

        with open(self.csvPath,"r") as csvfile:
            source = csvfile.readlines()
            lines = []
            for each in source:
                row = []
                for column in each.split(","):
                    row.append(column.strip())
                lines.append(row)
            s = set()
            highest_ownership_rows=[]
            for i in range(1,len(lines)):
                if i< len(lines) and lines[i][0] not in s:
                    temp = lines[i][0]
                    s.add(temp)
                    candidates = []
                    while i< len(lines) and temp == lines[i][0]:
                        candidates.append(lines[i])
                        i+=1
                    candidates.sort(key=lambda x: float(x[3]), reverse=True)
                    highest_ownership_rows.append(candidates[0])
            owner_csv_path = "/".join(self.csvPath.split("/")[:-1])+"/owner.csv"
            with open(owner_csv_path, "w") as owner_csv:
                writer = csv.writer(owner_csv)
                writer.writerow(["File Path", "File Name", "Author Name", "Ownership", "commits", "total commits"])
                writer.writerows(highest_ownership_rows)

        return self

