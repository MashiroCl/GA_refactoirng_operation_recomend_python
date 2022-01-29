from code_ownership.File import File
import glob
import csv
from utils import create_folder
from os.path import join
class Repository():
    def __init__(self,path:str):
        self.path=path
        self.name=path.split("/")[-1]
        self.files=list()
        # self.files = [each for each in glob.glob(self.path+'/**/*.java',recursive=True)]
        self.csvPath=""
        self._findJavaFiles()

    def _findJavaFiles(self):
        '''
        find all .java files in current directory
        :return:
        '''
        javaFiles=glob.glob(self.path+'/**/*.java',recursive=True)
        for each in javaFiles:
            self.files.append(File(each))
        return self

    def countAuthorCommit(self,outputPath:str):
        '''
        for each file in the repository use git command to obtain commit and save results in outputPath,
        and calculate count of authors' appearance and ratio of it
        :param outputPath:
        :return:
        '''
        for each in self.files:
            each.logCommit(outputPath).json2Commit().fillAuthorCommitDict()

        return self

    def authorCommitDict2CSV(self, csvPath:str, csvName:str):
        '''
        wirte extraction info of all files into a csv file
        :param outputPath: output path for csv file
        :return:
        '''
        create_folder(csvPath)
        csvPath=join(csvPath,csvName)
        result=[]
        for eachFile in self.files:
            for eachAuthor in eachFile.authorCommitDict:
                temp = []
                temp.append(eachFile.path)
                temp.append(eachFile.name)
                temp.append(eachAuthor)
                temp.append(float(len(eachFile.authorCommitDict[eachAuthor]))/float(eachFile.commitNum))
                temp.append(len(eachFile.authorCommitDict[eachAuthor]))
                temp.append(eachFile.commitNum)
                result.append(temp)
        with open(csvPath,"w") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["File Path","File Name","Author Name","Ownership","commits","total commits"])
            writer.writerows(result)
        self.csvPath=csvPath

    def _getCSVLine(self,filePath:str)->list:
        try:
            with open(self.csvPath) as f:
                reader=csv.reader(f)
                rows=[row for row in reader]
        except FileNotFoundError:
            print("No such file as {}".format(filePath))
        result=[]
        for each in rows[1:]:
            if each[0]==filePath:
                result.append(each)
        return result

    def getOwnership(self,filePath:str,name:str)->float:
        '''
        get ownership from csv file
        :param filePath: csv file
        :param name: author name
        :return:
        '''
        lists=self._getCSVLine(filePath)
        for each in lists:
            if each[2]==name:
                return each[3]
        return 0

    def getContribution(self,filePath:str,name:str)->int:
        '''
        return number of commit $name commits in file $filePath
        :param filePath:
        :param name:
        :return:
        '''
        lists=self._getCSVLine(filePath)
        for each in lists:
            if each[2]==name:
                return each[4]
        return 0

    def getTotalCommits(self,filePath:str)->int:
        '''
        return total number of commits in file $filePath
        :param filePath:
        :return:
        '''
        lists=self._getCSVLine(filePath)
        return lists[0][5]

    def getAuthorCommitDict(self,filePath:list):
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
        return  aCD


