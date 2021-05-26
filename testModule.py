from jClass import *
from readJson import readJson
from metricCalculation import *
from moveMethod import moveMethod

def test_jClass():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))

    # for each in jClist:
    #     print(each.getField())
    for each in jClist:
        print("___________________")

        for each2 in each.getMethod():
            print(each2.getFull())





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

    moveMethod(testMethod,jClist[0],jClist[3])
    for each in jClist[0].getMethod():
        print(each.getFull())
    for each in jClist[3].getMethod():
        print(each.getFull())
    # print(each.getFull() for each in jClist[0].getMethod())
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(each.getFull() for each in jClist[3].getMethod())



def test_DAM():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
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

# test_jClass()
# test_addMethod()
# test_DAM()
test_CIS_NOM()
# s=1
# a=2
# b=3
# list=[s,a,b]
#
# d=1
# list.remove(d)
# print(list)