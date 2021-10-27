from Jxplatform2.jClass import jClass
from utils import readJson
from QMOOD.metricCalculation import *
from executeRO import ExecuteRO
from jMetal.Solution import Solution
from QMOOD.Qmood import Qmood
from Encoding import Encoding
from jMetal.SearchROProblemBinary import SearchROProblemBinary
from Encoding.BinaryEncoding import BinaryEncoding
from Encoding.ROTypeDict import ROTypeDict
from RefactoringOperation.RefactoringOperationEnum import *
from RefactoringOperation.RefactoringOperationDispatcher import *
from CodeOwnership.Repository import Repository
def test_jClass():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
    jsonFileRTE="/Users/leichen/Desktop/res.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))

    # for each in jClist:
    #     print(each.getField())
    for each in jClist:

        # print("Class Name",each.getClassName())
        # print("Field",each.getField())/Users/leichen/Code/CKJM-extended
        # for each2 in each.getMethod():
        #     print(each2.getFull())
        for each2 in each.getMethod():
            print("___________________")
            print(each2.getFull())
            for each3 in each2.getParameterType():
                print(each3+" ")





def test_addMethod():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))

    # for each in jClist:
    #     print(each.getField())


    testMethod=jClist[0].methodList[0]
    # print("Add testMethod",testMethod.getName())
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print("Delete testMethod",testMethod.getFull())
    print("__________________________")

    # for each in jClist:
    #     each.addMethod(testMethod)
    #     # each.addMethod(testMethod)
    #     each.deleteMethod(testMethod)
    # for each in jClist:
    #     print("_____",each.getClass(),"_____")
    #     for each2 in each.getMethod():
    #         print(each2.getFull())

    for each in jClist[0].getMethod():
        print(each.getFull())
    for each in jClist[3].getMethod():
        print(each.getFull())

    print("__________________________")
    eRO=ExecuteRO()
    eRO.moveMethod(testMethod,jClist[0],jClist[3])
    for each in jClist[0].getMethod():
        print(each.getFull())
    for each in jClist[3].getMethod():
        print(each.getFull())
    # print(each.getFull() for each in jClist[0].getMethod())
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(each.getFull() for each in jClist[3].getMethod())



def test_DAM():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
    jsonFileRTE = "/Users/leichen/Desktop/ckjm_ext.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    field=[]
    for each in load:
        jClist.append(jClass(load=each))
    for each in jClist:
        print(DAM(each))


def test_CIS_NOM():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    for each in jClist:
        print("CIS = ",CIS(each))
        print("NOM = ",NOM(each))

def test_MOA():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    jsonFileRTE = "/Users/leichen/Desktop/ckjm_ext.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    for each in jClist:
        print(MOA(each,jClist))

def test_getFPType():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    for each in jClist:
        a,b=getFPType(each)
        print("a   ",a)
        print("b   ",b)

def test_DCC():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    for each in jClist:
        print(DCC(each,jClist))
    return DCC(jClist[0],jClist)

def test_MFA():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    jsonFileRTE="/Users/leichen/Desktop/ckjm_ext.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    MFAl=[]
    for each in jClist:
        MFAl.append(MFA(each))
    return MFAl

def test_CAM():
    jsonFileRTE="/Users/leichen/Desktop/ckjm_ext.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    CAMl=[]
    for each in jClist:
        CAMl.append(CAM(each))
    return CAMl

def test_NOP():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    jsonFileRTE = "/Users/leichen/Desktop/res.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    NOPl=[]
    for each in jClist:
        NOPl.append(NOP(each))
    return NOPl


def test_RefactoringOperation():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    jMethod=[]
    for each in jClist:
        for each2 in each.getMethod():
            jMethod.append(each2)

    s=Solution("test")
    mDict,cDict=s.binaryEncodingFixedLength(jMethod, jClist)

    print(mDict)
    print(cDict)

def test_calculateQmood():
    jsonFileRTE="/Users/leichen/Desktop/ckjm_ext.json"
    load=readJson(jsonFileRTE)
    jClist=[]
    for each in load:
        javaClass=jClass(each)
        if not javaClass.testClass:
            jClist.append(javaClass)

    for each in jClist:
        if(each.classInfo=="1025#AbstractClassVisitor"):
            abstractClassVisitor=each
            print(each.getPackage())
        print(each.classInfo)
    qmood=Qmood()
    # temp=jClist[4]
    # print(temp.getClassName())
    # qmood.calculateSingleQmood(temp,jClist)

    result=qmood.calculateQmood([abstractClassVisitor])
    print("DAM: ",qmood.DAM)
    print("DCC: ", qmood.DCC)
    print("MOA: ", qmood.MOA)
    print("CAM: ", qmood.CAM)
    print("NOP: ",qmood.NOP)
    print("NOM: ", qmood.NOM)
    print("MFA: ", qmood.MFA)
    print("CIS: ", qmood.CIS)

    for idx,value in enumerate(result):
        print(idx,value,result[value])

def testEncoding():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    load=readJson(jsonFileRTE)

    e = Encoding()
    jClist=[]
    Dc=dict()
    Dm=dict()
    for each in load:
        jClist.append(jClass(load=each))


    bClass=e.binaryEncodingFixedLength(jClist)
    for i in range(len(jClist)):
        Dc[bClass[i]]=jClist[i]
        methods=jClist[i].getMethod()
        bMethod=e.binaryEncodingFixedLength(methods)
        for j in range(len(methods)):
            Dm[bClass[i]+bMethod[j]]=methods[j]
    return Dm,Dc

def testFilePath():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    for each in jClist:
        print(each.filePath)

def testSearchROProblemBinary():
    jsonFileRTE="/Users/leichen/Desktop/ckjm_ext.json"
    load=readJson(jsonFileRTE)
    jClist=[]
    for each in load:
        javaClass=jClass(each)
        if not javaClass.testClass:
            jClist.append(javaClass)
    # print(jClist)
    sropb = SearchROProblemBinary(jClist)
    print(sropb.number_of_bits)


def testBinaryEncoding():
    jsonFileRTE="/Users/leichen/Desktop/ckjm_ext.json"
    jsonFileRTE = "/Users/leichen/Desktop/jedis.json"
    load=readJson(jsonFileRTE)
    jClist=[]
    for each in load:
        javaClass=jClass(each)
        if not javaClass.testClass:
            jClist.append(javaClass)
    be = BinaryEncoding()
    be.encoding(jClist)
    # # for each in be.encodingDict.getEncodingDict()["class"]:
    # #     print(be.encodingDict.getEncodingDict()["class"][each]["field"])
    print(be.encodingDict.getEncodingDict()["class"])
    # print(be.chromosomeLen)
    # decoded = be.decoding(["100000101111100001110111010100000001010111001101010001111"])
    # print(decoded)
    # print(decoded[0]["class1"])
    # print(decoded[0]["class1method"])
    # print(decoded[0]["class1"]["method"])
    # print(decoded[0]["class1"]["method"].values())
    # print(decoded[0]["class2"]["classInfo"].getMethod()[0].getSignature())

def testROTypeDict():
    rotd = ROTypeDict()
    print(rotd.ROTypeDict)

def testDispatch():
    dispatch(RefactoringOperationEnum.NULL.value)("1","Hello")


# test_jClass()
# test_addMethod()
# test_DAM()
# test_CIS_NOM()
# test_MOA()
# test_getFPType()
# print(test_DCC())
# print(test_MFA())
# print(test_CAM())
# a="[[1,2,3],[4,5,6]]"
# b=list(a)
# print(b)
# print(test_NOP())
# test_RefactoringOperation()
# test_calculateQmood()
# testFilePath()
# print(test_MFA())
# test_MOA()
# testSearchROProblemBinary()
testBinaryEncoding()
# testROTypeDict()
# testDispatch()

