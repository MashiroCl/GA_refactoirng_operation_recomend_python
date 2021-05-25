from jClass import *
from readJson import readJson
from metricCalculation import DAM

def test_jClass():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))

    print(load[0])
    print(jClist[0].getClass())
    print(jClist[0].getField())
    print(jClist[0].getMethod())

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
test_DAM()