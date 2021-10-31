import os
class Jxplatform2:
    def __init__(self,jxplatPath:str,target:str,classPath:str,outputPath:str):
        self.jxplatPath=jxplatPath
        self.target=target
        self.classPath=classPath
        self.outputPath=outputPath
    def extractInfo(self):
        command="java -jar "+self.jxplatPath+" "+self.target +" "+ self.outputPath
        print(command)
        os.system(command)

if __name__ == "__main__":
    j="/Users/leichen/Code/pythonProject/pythonProject/salabResearch/Jxplatform2/JxplatformExtract.jar"
    # t="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jedis"
    t="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jedis"
    c=t
    outputPath="/Users/leichen/Desktop/jedis.json"
    jx=Jxplatform2(j,t,c,outputPath)
    jx.extractInfo()