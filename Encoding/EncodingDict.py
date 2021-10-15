class EncodingDict():
    '''
    class contains binary encoding for a java project
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

    def getEncodingDict(self):
        return self.encodingDict