import os

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


def extract_abs(jxplatPath, target, output_path):
    command = "java -jar " + jxplatPath + " -a " + target + " " + output_path
    print(command)
    os.system(command)

def extract_call_graph(jxplatPath, target, output_path):
    command = "java -jar " + jxplatPath + " -c " + target + " " + output_path
    print(command)
    os.system(command)


if __name__ == "__main__":
    repoName = "HikariCP"
    j="/Users/leichen/Code/pythonProject/pythonProject/salabResearch/jxplatform2/JxplatformExtract.jar"
    # j = "/home/chenlei/MORCO/MORCOpy/jxplatform2/JxplatformExtract.jar"
    t="/Users/leichen/ResearchAssistant/InteractiveRebase/data/"+repoName
    # t="/home/chenlei/MORCO/data/"+repoName
    c=t
    outputPath="/Users/leichen/Desktop/StaticalAnalysis"+repoName+".json"
    # outputPath="/home/chenlei/MORCO/extractResult/"+repoName+".json"
    jx=Jxplatform2(j, t, c, outputPath)
    jx.extractInfo()