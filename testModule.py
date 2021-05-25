from jClass import *
from readJson import readJson


def test_jClass():
    jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"
    load=readJson(jsonFileRTE)

    jClist=[]
    for each in load:
        jClist.append(jClass(load=each))

    print(jClist[0].getClass())
    print(jClist[0].getField())
    print(jClist[0].getMethod())

test_jClass()