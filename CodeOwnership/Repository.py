from File import File
import glob
import csv
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
        self.findJavaFiles()
        for each in self.files:
            each.getCommit(outputPath)
            each.json2Commit()
            each.commitAuthorCount()
            each.commitAuthorRatio()

        # for each in self.files:
        #     print(each.name)
        #     print(each.authorCommitDictRatio)

    def writeCSV(self,outputPath:str):
        result=[]
        for eachFile in self.files:
            for each2 in eachFile.authorCommitDictRatio:
                temp = []
                temp.append(eachFile.path)
                temp.append(eachFile.name)
                temp.append(each2)
                temp.append(eachFile.authorCommitDictRatio[each2])
                result.append(temp)
        csvPath=str(outputPath+"/"+self.name+".csv")
        with open(csvPath,"w") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["File Path","File Name","Author Name","Ownership"])
            writer.writerows(result)
        self.csvPath=csvPath


    def getOwnership(self,filePath:str)->list:
        with open(self.csvPath) as f:
            reader=csv.reader(f)
            rows=[row for row in reader]
        result=[]
        for each in rows[1:]:
            if each[0]==filePath:
                result.append(each)
        return result

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
