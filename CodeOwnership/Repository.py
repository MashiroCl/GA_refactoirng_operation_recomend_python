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
    def findJavaFiles(self)->list:
        javaFiles=glob.glob(self.path+'/**/*.java',recursive=True)
        for each in javaFiles:
            self.files.append(File(each))

    def countAuthorCommit(self,outputPath:str):
        create_folder(outputPath)
        self.findJavaFiles()
        for each in self.files:
            each.getCommit(outputPath)
            each.json2Commit()
            each.commitAuthorCount()
            each.commitAuthorRatio()

    def writeCSV(self,outputPath:str):
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


    def getCSVLine(self,filePath:str)->list:
        with open(self.csvPath) as f:
            reader=csv.reader(f)
            rows=[row for row in reader]
        result=[]
        for each in rows[1:]:
            if each[0]==filePath:
                result.append(each)
        return result

    def getOwnership(self,filePath:str,name:str)->float:
        lists=self.getCSVLine(filePath)
        for each in lists:
            if each[2]==name:
                return each[3]
        return 0
    def getContribution(self,filePath:str,name:str)->int:
        lists=self.getCSVLine(filePath)
        for each in lists:
            if each[2]==name:
                return each[4]
        return 0
    def getTotalCommits(self,filePath:str)->int:
        lists=self.getCSVLine(filePath)
        return lists[0][5]

if __name__=="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
    outputPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/outputTest"
    repo=Repository(path)
    repo.countAuthorCommit(outputPath=outputPath)
    repo.writeCSV("/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/csv")
    filePath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/src/main/java/net/engio/mbassy/common/AbstractConcurrentSet.java"
    result=repo.getOwnership(filePath)
    print(result)
    '''
    user输入名字，存储到solution中作为一个值solution.user
    然后RO涉及到的两个文件中是否有solution.user对应的ownership
        有的话就在evaluation里当一个值,
        没有的话就是0
    
    class jClass里需要有java文件路径信息
    
    '''
