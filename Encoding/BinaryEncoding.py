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

    def decoding(self,encodedSequences):
        '''
        decode sequences of encoded binary sequence to jCLass,jField,jMethod
        :param encodedSequences:
        :return: refactoring operation type and its parameters
        '''
        encodedResults=[]
        for encodedSequence in encodedSequences:
            encodedSequence = self.bool2Binary(encodedSequence)
            count = 0
            count+=self.ROtypeLen
            ROType2 = encodedSequence[0:count]
            class12 = encodedSequence[count:count+self.classLen]
            count+=self.classLen
            class1field2 = encodedSequence[count:count+self.fieldLen]
            count+=self.fieldLen
            class1method2 = encodedSequence[count:count+self.methodLen]
            count+=self.methodLen
            class22 = encodedSequence[count:count+self.classLen]
            count+=self.classLen
            class2field2 = encodedSequence[count:count+self.fieldLen]
            count+=self.fieldLen
            class2method2 = encodedSequence[count:count+self.methodLen]
            count+=self.methodLen

            ROType = self.ROTypeDict.findROType(ROType2)
            class1 = self.encodingDict.findClass(class12)
            class1field = self.encodingDict.findField(class12,class1field2)
            class1method = self.encodingDict.findMethod(class12,class1method2)
            class2 = self.encodingDict.findClass(class22)
            class2field = self.encodingDict.findField(class22,class2field2)
            class2method = self.encodingDict.findMethod(class22,class2method2)

            resDict = {}
            resDict["ROType"]=ROType
            resDict["class1"]=class1
            resDict["class1field"]=class1field
            resDict["class1method"]=class1method
            resDict["class2"]=class2
            resDict["class2field"]=class2field
            resDict["class2method"]=class2method
            encodedResults.append(resDict)

            print("decoding ", encodedSequence)


        return encodedResults


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

    def bool2Binary(self,boolList):
        'convert bool list into a zero-one binary string'
        res = ""
        for each in boolList:
            if each:
                res=res+"1"
            if not each:
                res= res+"0"
        return res