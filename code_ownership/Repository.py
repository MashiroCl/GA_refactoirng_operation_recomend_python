import csv
import glob
from os.path import join
from typing import List
from code_ownership.File import File
from utils import create_folder

CSV_HEAD = ["File Path", "File Name", "Author Name", "Ownership", "commits",
            "total commits"]  # head line for ownership csv file
OWNER_CSV_NAME = "owner.csv"  # output owner csv file name
OWNERSHIP_THRESHOLD = 0.2  # threshold to decide whether choose 2nd highest ownership owner


def ownership2csv(ownerships: List[List[str]], csv_path: str):
    with open(csv_path, "w") as owner_csv:
        writer = csv.writer(owner_csv)
        writer.writerow(CSV_HEAD)
        writer.writerows(ownerships)


def is_testclass(s: str):
    if "test" in s or "Test" in s:
        return True
    return False


class Repository:
    def __init__(self, path: str):
        self.path = path
        self.name = path.split("/")[-1]
        self.files = self._extract_java_files()
        self.csvPath = ""

    def _extract_java_files(self) -> List[File]:
        '''
        find all .java files in current directory
        :return:
        '''
        javaFiles = glob.glob(self.path + '/**/*.java', recursive=True)
        files = []
        for each in javaFiles:
            files.append(File(each))
        return files

    def get_java_files(self) -> List[File]:
        return self.files

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

    def authorCommitDict2CSV(self, csv_path: str, csv_name: str, localPath: str):
        '''
        wirte extraction info of all files into a csv file
        :param localPath: parent path for repo path
        :return:
        '''
        create_folder(csv_path, False)
        csv_path = join(csv_path, csv_name)
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

    # Write ownerships to csvs
    def extract_owner_csv(self):
        '''
        find the highest ownership developer in one java file and export them into another csv
        :param filePath:
        :return:
        '''
        csv_lines = self._extract_csv()
        highest_ownership_rows = []
        row = 1
        while row < len(csv_lines):
            if row < len(csv_lines) and csv_lines[row][0]:
                while is_testclass(csv_lines[row][0]):
                    row +=1
                temp = csv_lines[row][0]
                candidates = []
                while row < len(csv_lines) and temp == csv_lines[row][0]:
                    candidates.append(csv_lines[row])
                    row += 1
                highest_ownership_rows += self.select_owners(candidates)
        owner_csv_path = "/".join(self.csvPath.split("/")[:-1]) + "/" + OWNER_CSV_NAME

        ownership2csv(highest_ownership_rows, owner_csv_path)
        return self

    # todo: 输出原始csv 改名，再extract
    def select_owners(self, candidates: List[List[str]]) -> List[List[str]]:
        '''
        select owners who has the highest/ 2nd highest ownership on the file.
        If ownership_1st - ownership_2nd <0.2, then choose 2nd, otherwise not select 2nd
        candidates: ownerships of contributors to the file (candidates[0][0]) in the format of CSV_HEAD
        '''
        candidates.sort(key=lambda x: float(x[3]), reverse=True)
        # print(candidates)
        if len(candidates) < 2:
            return [candidates[0]]
        elif float(candidates[0][3]) - float(candidates[1][3]) < OWNERSHIP_THRESHOLD:
            return [candidates[0], candidates[1]]
        return [candidates[0]]
