from File import File
import glob
import csv
class Repository():
    def __init__(self,path:str):
        self.path=path
        self.name=path.split("/")[-1]
        self.files=[]
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
        with open(str(outputPath+"/"+self.name+".csv"),"w") as csvfile:
            writer=csv.writer(csvfile)
            writer.writerow(["File Path","File Name","Author Name","Ownership"])
            writer.writerows(result)

if __name__=="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
    outputPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/outputTest"
    repo=Repository(path)
    repo.countAuthorCommit(outputPath=outputPath)
    repo.writeCSV("/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/csv")
