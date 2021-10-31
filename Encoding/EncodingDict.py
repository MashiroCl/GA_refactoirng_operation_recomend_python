class EncodingDict():
    '''
    class contains encoding result for a java project
    '''
    def __init__(self):
        self.encodingDict = {"class":{}}
    def addClass(self,value,classInfo):
        self.encodingDict["class"][value]={"classInfo":classInfo,
                                           "field":{},
                                           "method":{}}
    def addField(self,classValue,fieldValue,fieldInfo):
        self.encodingDict["class"][classValue]["field"][fieldValue]=fieldInfo

    def addMethod(self,classValue,methodValue,methodInfo):
        self.encodingDict["class"][classValue]["method"][methodValue]=methodInfo

    #todo check null when executing
    def findClass(self,value):
        try:
            res = self.encodingDict["class"][value]
        except KeyError:
            res = None
        return res

    def findField(self,classValue,fieldValue):
        try:
            res = self.encodingDict["class"][classValue]["field"][fieldValue]
        except KeyError:
            res = None
        return res

    def findMethod(self,classValue,methodValue):
        try:
            res = self.encodingDict["class"][classValue]["method"][methodValue]
        except KeyError:
            res = None
        return res

    def getEncodingDict(self):
        return self.encodingDict