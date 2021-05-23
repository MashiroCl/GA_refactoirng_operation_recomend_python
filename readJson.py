import json

jsonFileRTE="/Users/leichen/Code/jxplatform2Json/RTE.json"

def readJson(jsonFile):
    with open(jsonFile) as f:
        load=json.load(f)
    return load


load=readJson(jsonFileRTE)
for each in load:
    print(each)
