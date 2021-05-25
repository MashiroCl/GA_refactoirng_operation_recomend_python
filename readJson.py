import json



def readJson(jsonFile):
    with open(jsonFile) as f:
        load=json.load(f)
    return load



if __name__=="__main__":
    jsonFileRTE = ""
    load=readJson(jsonFileRTE)
    print(load)

    for each in load:
        # print(each)
        print(each['className'])
        print(each['jField'])
        print(each['jMethod'])