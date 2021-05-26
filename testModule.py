from jClass import *
from readJson import readJson
from metricCalculation import DAM

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
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")

    for each in jClist:
        each.addMethod(testMethod)
        each.deleteMethod(testMethod)
    for each in jClist:
        print("_____",each.getClass(),"_____")
        for each2 in each.getMethod():
            print(each2.getFull())



def test_DAM():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    field=[]
    for each in load:
        jClist.append(jClass(load=each))
    for each in jClist:
        print(each.getField())
        print(DAM(each.getField()))


# test_jClass()
test_addMethod()
# test_DAM()
# s=1
# a=2
# b=3
# list=[s,a,b]
#
# d=1
# list.remove(d)
# print(list)