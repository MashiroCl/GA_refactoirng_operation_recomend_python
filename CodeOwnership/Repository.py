from CodeOwnership.File import File
import glob
import csv
from utils import create_folder
class Repository():
    def __init__(self,path:str):
        self.path=path
        self.name=path.split("/")[-1]
        self.files=[]
        self.csvPath=""
    def _findJavaFiles(self)->list:
        '''
        find all .java files in current directory
        :return:
        '''
        javaFiles=glob.glob(self.path+'/**/*.java',recursive=True)
        for each in javaFiles:
            self.files.append(File(each))

    def countAuthorCommit(self,outputPath:str):
        '''
        for each file in the repository use git command to obtain commit and save results in outputPath,
        and calculate count of authors' appearance and ratio of it
        :param outputPath:
        :return:
        '''
        create_folder(outputPath)
        self._findJavaFiles()
        for each in self.files:
            each.getCommit(outputPath)
            each.json2Commit()
            each.commitAuthorCount()
            each.commitAuthorRatio()

    def writeCSV(self,outputPath:str):
        '''
        wirte extraction info of all files into a csv file
        :param outputPath: output path for csv file
        :return:
        '''
        result=[]
        for eachFile in self.files:
            for each2 in eachFile.authorCommitDictRatio:
                temp = []
                temp.append(eachFile.path)
                temp.append(eachFile.name)
                temp.append(each2)
                temp.append(eachFile.authorCommitDictRatio[each2])
                temp.append(eachFile.authorCommitDict[each2])
                temp.append(eachFile.commitNum)
                result.append(temp)
        csvPath=str(outputPath+"/"+self.name+".csv")
        with open(csvPath,"w") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["File Path","File Name","Author Name","Ownership","commits","total commits"])
            writer.writerows(result)
        self.csvPath=csvPath


    def _getCSVLine(self,filePath:str)->list:
        with open(self.csvPath) as f:
            reader=csv.reader(f)
            rows=[row for row in reader]
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
        lists=self._getCSVLine(filePath)
        for each in lists:
            if each[2]==name:
                return each[4]
        return 0
    def getTotalCommits(self,filePath:str)->int:
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
        aCD = {}
        for eachFile in self.files:
            if eachFile.path in filePath:
                for eachCommiter in eachFile.authorCommitDict:
                    if eachCommiter in aCD:
                        aCD[eachCommiter]+=eachFile.authorCommitDict[eachCommiter]
                    else:
                        aCD[eachCommiter] = eachFile.authorCommitDict[eachCommiter]
        return  aCD

if __name__=="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
    outputPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/outputTest"
    repo=Repository(path)
    repo.countAuthorCommit(outputPath=outputPath)
    repo.writeCSV("/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/csv")
    filePath1="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/src/test/java/net/engio/mbassy/common/MessageManager.java"
    filePath2="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/src/test/java/net/engio/mbassy/common/AssertSupport.java"
    result = repo.getHighestOwnership(filePath1,filePath2)
    result2 = repo.getNumOfCommiters(filePath1,filePath2)
    print(result)
    print(result2)
    '''
    user输入名字，存储到solution中作为一个值solution.user
    然后RO涉及到的两个文件中是否有solution.user对应的ownership
        有的话就在evaluation里当一个值,
        没有的话就是0
    
    class jClass里需要有java文件路径信息
    
    '''
