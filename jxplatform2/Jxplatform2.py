import os
import sys
class Jxplatform2:
    def __init__(self,jxplatPath:str,target:str,classPath:str,outputPath:str):
        self.jxplatPath=jxplatPath
        self.target=target
        self.classPath=classPath
        self.outputPath=outputPath
    def extractInfo(self):
        command="java -jar "+self.jxplatPath+" "+self.target +" "+ self.outputPath
        # command="java "+self.jxplatPath+" "+self.target +" "+ self.outputPath
        print(command)
        os.system(command)

if __name__ == "__main__":
    # repoName = sys.argv[1]
    j="/Users/leichen/Code/pythonProject/pythonProject/salabResearch/Jxplatform2/JxplatformExtract.jar"
    # j="/Users/leichen/Desktop/JxplatformExtract.jar"
    # j = "/home/chenlei/MORCO/MORCOpy/Jxplatform2/JxplatformExtract.jar"
    t="/Users/leichen/ResearchAssistant/InteractiveRebase/data/calen-chan"
    # t="/Users/leichen/ResearchAssistant/InteractiveRebase/data/ganttproject-1.10.2"
    # t="/home/chenlei/MORCO/data/"+repoName
    c=t
    outputPath="/Users/leichen/Desktop/calen.json"
    # outputPath="/home/chenlei/MORCO/extractResult/"+repoName+".json"
    jx=Jxplatform2(j,t,c,outputPath)
    jx.extractInfo()