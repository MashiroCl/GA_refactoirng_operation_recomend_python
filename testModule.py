from jClass import *
from readJson import readJson
from metricCalculation import *
from executeRO import ExecuteRO
from RefactoringOperation import Solution,MoveMethod
from Qmood import Qmood


def test_jClass():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
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
    jsonFileRTE = "/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
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
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    MFAl=[]
    for each in jClist:
        MFAl.append(MFA(each))
    return MFAl

def test_CAM():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
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
    mDict,cDict=s.binaryEncoding(jMethod,jClist)

    print(mDict)
    print(cDict)

def test_calculateQmood():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))
    # for each in jClist:
    #     print(each.getClassName())
    qmood=Qmood()
    temp=jClist[4]
    print(temp.getClassName())
    qmood.calculateQmood(temp,jClist)
    print("DAM: ",qmood.DAM)
    print("MOA: ", qmood.MOA)
    print("MFA: ", qmood.MFA)
    print("CAM: ", qmood.CAM)
# test_jClass()
# test_addMethod()
# test_DAM()
# test_CIS_NOM()
# test_MOA()
# test_getFPType()
print(test_DCC())
# print(test_MFA())
# print(test_CAM())
# a="[[1,2,3],[4,5,6]]"
# b=list(a)
# print(b)
# print(test_NOP())
# test_RefactoringOperation()
# test_calculateQmood()
