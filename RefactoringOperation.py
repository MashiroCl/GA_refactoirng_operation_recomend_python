from jClass import jClass
from jMethod import jMethod
from readJson import readJson
from Encoding import Encoding

#represent refactoring operations
class Solution():
    def __init__(self,operation="solution"):
        self.operation=operation
        self.parameters=None
        self.mDict=dict()
        self.cDict=dict()
        self.cLen=0
        self.mLen=0
        'in case of MoveMethod'
        self.len=self.mLen+self.cLen+self.cLen
    def setParameters(self,parameters):
        self.parameters=parameters

    def setmDict(self,mDict):
        self.mDict=mDict

    def setcDict(self, cDict):
        self.cDict=cDict

    # def binaryEncoding(self,methodList:list,classList:list):
    #     # length of "0b" is 2
    #     mBinaryLen=len(bin(len(methodList)))-2
    #     cBinaryLen=len(bin(len(classList)))-2
    #     mDict=dict()
    #     cDict=dict()
    #     for i in range(len(methodList)):
    #         body=bin(i).split("0b")[1]
    #         head=(mBinaryLen-len(body))*"0"
    #         mDict[methodList[i]]=head+body
    #     for i in range(len(classList)):
    #         body=bin(i).split("0b")[1]
    #         head=(mBinaryLen-len(body))*"0"
    #         cDict[classList[i]]=head+body
    #     self.setmDict(mDict)
    #     self.setcDict(cDict)
    #     return mDict,cDict

    # def binaryEncoding(self,jClist):
    #     eC,eM = Encoding(),Encoding()
    #     dC,dM = dict(),dict()
    #     bClass = eC.binaryEncoding(jClist)
    #     for i in range(len(jClist)):
    #         dC[bClass[i]] = jClist[i]
    #         methods = jClist[i].getMethod()
    #         bMethod = eM.binaryEncoding(methods)
    #         for j in range(len(methods)):
    #             dM[bClass[i] + bMethod[j]] = methods[j]
    #     self.setcDict(dC)
    #     self.setmDict(dM)
    #     return eC,eM

    def setSoltuionLen(self):
        self.len=self.len=self.mLen+self.cLen+self.cLen

    def binaryEncoding(self,jClist):

        'find the maximum number contained in one class'
        lenM=0
        for each in jClist:
            if len(each.getMethod())>lenM:
                lenM=len(each.getMethod())

        dC, dM = dict(), dict()
        e = Encoding()

        'binary encoding class'
        lenC=len(jClist)
        num=0
        for i in range(len(jClist)):
            dC[e.binaryEncoding(lenC,i)]=jClist[i]
            for each in jClist[i].getMethod():
                dM[e.binaryEncoding(lenM,num)]=each
                num+=1
        self.setmDict(dM)
        self.setcDict(dC)
        self.mLen=len(bin(lenM).split("0b")[1])-2
        self.cLen=len(bin(lenC).split("0b")[1])-2

    def binaryDecoding(self,str):
        'only works for structure like MoveMethod(m, C , C)'

        l=[self.mLen,self.cLen,self.cLen]
        # print(" l is ",l)
        eTemp=Encoding()
        result=eTemp.binaryDecoding(str,l)
        method=self.getMbyEncoding(result[0])
        # print("result[1] is ",result[1])
        C1 = self.getCbyEncoding(result[1])
        C2 = self.getCbyEncoding(result[2])
        print(C1)
        print(C2)
        return method,C1,C2


    def getEncodingbyC(self,c:jClass):
        for each in self.cDict:
            if self.cDict[each]==c:
                return each

    def getEncodingbyM(self,m:jMethod):
        for each in self.mDict:
            if self.mDict[each] == m:
                return each

    def getCbyEncoding(self,encodedC:str):
        for each in self.cDict:
            if each==encodedC:
                return self.cDict[each]

    def getMbyEncoding(self,encodedM:str):
        for each in self.mDict:
            if each==encodedM:
                return self.mDict[each]

class MoveMethod(Solution):
    def __init__(self,method:jMethod,c1:jClass,c2:jClass):
        super(MoveMethod, self).__init__("MoveMethod")
        self.method=method
        self.sourceClass=c1
        self.targetClass=c2

    def getInfo(self)->list:
        print([self.method,self.sourceClass,self.targetClass])
        return [self.method,self.sourceClass,self.targetClass]

    '''
    MoveMethod(method,sourceClass,TargetClass)
    '''
    def execute(self):
        self.sourceClass.deleteMethod(self.method)
        self.targetClass.addMethod(self.method)


if __name__ =="__main__":
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    load=readJson(jsonFileRTE)
    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))

    s=Solution()
    s.binaryEncoding(jClist)
    print(s.getEncodingbyC(jClist[0]))
    print(s.getEncodingbyC(jClist[1]))
    method=jClist[0].getMethod()[0]
    print(s.getEncodingbyM(method))
    # mm=MoveMethod(method,jClist[0],jClist[1])
    # mm.execute()
    #
    # print(jClist[0].getMethod())
    # print(jClist[1].getMethod())

    print("__________________________")
    string="00000000000001"
    m,c1,c2=s.binaryDecoding(string)
    mm=MoveMethod(m,c1,c2)
    print(m)
    print(c1.getMethod())
    print(c2.getMethod())

    print("__________________________")
    mm.execute()
    print(c1.getMethod())
    print(c2.getMethod())





