from .EncodingDict import EncodingDict
from .ROTypeDict import ROTypeDict
class BinaryEncoding():
    def __init__(self):
        self.chromosomeLen=0
        self.classLen = 0
        self.fieldLen = 0
        self.methodLen = 0
        self.encodingDict = EncodingDict()
        self.ROTypeDict = ROTypeDict()
        self.ROtypeLen = self.ROTypeDict.ROTypeLen
    def encoding(self,projectInfo)->str:
        '''
        Encode a list of jClass entities into binary sequences which represent refactoring operations
        :param projectInfo: list of jClass entities
        :return: chromosome length after encoding
        '''
        'Element: ROtype length:3'

        'calculate length of longest '
        jFieldLenMax = -1
        jMethodLenMax = -1
        for eachClass in projectInfo:
            jFieldLenTemp = len(eachClass.getField())
            jMethodLenTemp = len(eachClass.getMethod())
            if(jFieldLenTemp>jFieldLenMax):
                    jFieldLenMax = jFieldLenTemp
            if(jMethodLenTemp>jMethodLenMax):
                    jMethodLenMax =  jMethodLenTemp
        'calculate binary sequence length'
        '-1 because encode from 0 not 1'
        jFieldLenMax = len(bin(jFieldLenMax-1).split("0b")[1])
        jMethodLenMax = len(bin(jMethodLenMax-1).split("0b")[1])
        jClassEntitiesLen = len(bin(len(projectInfo)-1).split("0b")[1])

        self.classLen=jClassEntitiesLen
        self.methodLen=jMethodLenMax
        self.fieldLen=jFieldLenMax

        countJClass = 0
        for eachClass in projectInfo:
            jClass2 = self.toBinarySequence(countJClass,jClassEntitiesLen)
            countJClass+=1
            self.encodingDict.addClass(jClass2,eachClass)

            countJField = 0
            for eachField in eachClass.getField():
                jField2 = self.toBinarySequence(countJField,jFieldLenMax)
                countJField+=1
                self.encodingDict.addField(jClass2,jField2,eachField)

            countJMethod = 0
            for eachMethod in eachClass.getMethod():
                jMethod2 = self.toBinarySequence(countJMethod,jMethodLenMax)
                countJMethod+=1
                self.encodingDict.addMethod(jClass2,jMethod2,eachMethod)

        self.chromosomeLen = self.ROtypeLen + self.classLen*2 + self.fieldLen*2 + self.methodLen*2
        return self.chromosomeLen

    def decoding(self):
        pass

    def toBinarySequence(self,value,length):
        '''
        Convert an int number value into a binary sequence with a length of length
        :param value: value being converted
        :param length: binary sequence
        :return: a string of binary sequence
        '''
        body = bin(value).split("0b")[1]
        head = (length - len(body)) * "0"
        result = head + body
        return result
