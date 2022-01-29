from jxplatform2.jClass import jClass
from jxplatform2.jMethod import jMethod
from utils import readJson
from encoding.Encoding import Encoding

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

    def setSoltuionLen(self):
        self.len=self.mLen+self.cLen+self.cLen

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
            dC[e.binaryEncodingFixedLength(lenC, i)]=jClist[i]
            for each in jClist[i].getMethod():
                dM[e.binaryEncodingFixedLength(lenM, num)]=each
                num+=1
        self.setmDict(dM)
        self.setcDict(dC)
        self.mLen=len(bin(lenM).split("0b")[1])-2
        self.cLen=len(bin(lenC).split("0b")[1])-2

    def binaryDecoding(self,str):
        'only works for structure like MoveMethod(m, C , C)'

        l=[self.mLen,self.cLen,self.cLen]
        eTemp=Encoding()
        result=eTemp.divideBinarySequence(str, l)
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

    def bool2str(self,s:str):
        'RO is in True, False form'
        temp = ""
        for each in s:
            if each == True:
                temp += "1"
            else:
                temp += "0"
        return temp


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
        self.sourceClass.removeMethod(self.method)
        self.targetClass.addMethod(self.method)


if __name__ =="__main__":
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    load=readJson(jsonFileRTE)
    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))

    s=Solution()
    s.binaryEncoding(jClist)
    RO=[False, True, False, True, True, True, False, True, True, False, False, True, False, False]
    m,c1,c2=s.binaryDecoding(s.bool2str(RO))
    print(m.getName(),c1.getClassName(),c2.getClassName())






