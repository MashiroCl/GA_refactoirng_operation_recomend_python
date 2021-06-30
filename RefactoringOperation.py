from jClass import jClass
from jMethod import jMethod

#represent refactoring operations
class Solution():
    def __init__(self,operation:str):
        self.operation=operation
        self.parameters=None
        self.mDict=None
        self.cDict=None

    def setParameters(self,parameters):
        self.parameters=parameters

    def setmDict(self,mDict):
        self.mDict=mDict

    def setcDict(self, cDict):
        self.cDict=cDict

    def binaryEncoding(self,methodList:list,classList:list):
        # length of "0b" is 2
        mBinaryLen=len(bin(len(methodList)))-2
        cBinaryLen=len(bin(len(classList)))-2
        mDict=dict()
        cDict=dict()
        for i in range(len(methodList)):
            body=bin(i).split("0b")[1]
            head=(mBinaryLen-len(body))*"0"
            mDict[methodList[i]]=head+body
        for i in range(len(classList)):
            body=bin(i).split("0b")[1]
            head=(mBinaryLen-len(body))*"0"
            cDict[classList[i]]=head+body
        self.setmDict(mDict)
        self.setcDict(cDict)
        return mDict,cDict

    def getmDictValue(self,c:jClass):
        for each in self.cDict:
            if jClass==each:
                return self.cDict[each]

    def getcDictValue(self,m:jMethod):
        for each in self.mDict:
            if jMethod == each:
                return self.mDict[each]

    def getcDict(self,encoding:str):
        for idx,value in self.cDict.items():
            pass

class MoveMethod(Solution):
    def __init__(self,method:jMethod,c1:jClass,c2:jClass):
        super(MoveMethod, self).__init__("MoveMethod")
        self.method=method
        self.fromClass=c1
        self.toClass=c2

    def getInfo(self)->list:
        print([self.method,self.fromClass,self.toClass])
        return [self.method,self.fromClass,self.toClass]

    def setCurrentEncoding(self):
        pass


if __name__ =="__main__":
    #MoveMethod(method,class1,class2)
    mm=MoveMethod("m","c1","c2")
    mm.getInfo()
    m=["m1","m2","m3","m4","m5"]
    C=["C1","C2","C3","C4","C5"]
    mm.binaryEncoding(m,C)
    print(4*"0")
    print(mm.binaryEncoding(m,C))

    a={"1":123,"2":234}
    for idx,value in a.items():
        print(value)
    #