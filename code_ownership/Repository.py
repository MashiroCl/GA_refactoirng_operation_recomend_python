import csv
import glob
from os.path import join
from typing import List
from code_ownership.File import File
from utils import create_folder

CSV_HEAD = ["File Path", "File Name", "Author Name", "Ownership", "commits", "total commits"]


def ownership2csv(ownerships:List[List[str]], csv_path:str):
    with open(csv_path, "w") as owner_csv:
        writer = csv.writer(owner_csv)
        writer.writerow(CSV_HEAD)
        writer.writerows(ownerships)


class Repository:
    def __init__(self, path: str):
        self.path = path
        self.name = path.split("/")[-1]
        self.files = self._findJavaFiles()
        self.csvPath = ""

    def _findJavaFiles(self) -> List[File]:
        '''
        find all .java files in current directory
        :return:
        '''
        javaFiles = glob.glob(self.path + '/**/*.java', recursive=True)
        files = []
        for each in javaFiles:
            files.append(File(each))
        return files

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

    def authorCommitDict2CSV(self, csv_path: str, csvName: str, localPath: str):
        '''
        wirte extraction info of all files into a csv file
        :param outputPath: output path for csv file
        :param localPath: parent path for repo path
        :return:
        '''
        create_folder(csv_path, False)
        csv_path = join(csv_path, csvName)
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
        ownership2csv(result, csv_path)
        self.csvPath = csv_path
        return self

    def _extract_csv(self) -> List[List[str]]:
        with open(self.csvPath, "r") as csvfile:
            data = csvfile.readlines()
            lines = []
            for each in data:
                row = []
                for column in each.split(","):
                    row.append(column.strip())
                lines.append(row)
        return lines

    #Write ownerships to csvs

    def extract_owner_csv(self):
        '''
        find the highest ownership developer in one java file and export them into another csv
        :param filePath:
        :return:
        '''
        csv_lines = self._extract_csv()
        s = set()
        highest_ownership_rows = []
        for i in range(1, len(csv_lines)):
            if i < len(csv_lines) and csv_lines[i][0] not in s:
                temp = csv_lines[i][0]
                s.add(temp)
                candidates = []
                while i < len(csv_lines) and temp == csv_lines[i][0]:
                    candidates.append(csv_lines[i])
                    i += 1
                candidates.sort(key=lambda x: float(x[3]), reverse=True)
                # consider not rank according to alphabet
                highest_ownership_rows.append(candidates[0])
        owner_csv_path = "/".join(self.csvPath.split("/")[:-1]) + "/owner.csv"

        ownership2csv(highest_ownership_rows,owner_csv_path)
        return self
