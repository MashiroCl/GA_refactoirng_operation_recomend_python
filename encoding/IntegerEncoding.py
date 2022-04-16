from refactoring_operation.RefactoringOperationEnum import RefactoringOperationEnum
from encoding.Encoding import Encoding


class IntegerEncoding(Encoding):
    def __init__(self):
        self.chromosomeLen=4
        self.classNum = 0
        self.N=0
        self.classDict={}
        self.ROtypeEnum = RefactoringOperationEnum
        self.ROTypeNum = len(self.ROtypeEnum)
        self.ROTypeDict = {}
    def encoding(self,projectInfo):
        '''
        Encode a list of jClass entities into a Integer sequences length of 4 which represents
        ROType class1Info class2Info N
        N should be the max number of methodNum&fieldNum and N%methodNum / N%fieldNum represents the method/field being chosen
        :param projectInfo: list of jClass entities
        :return:
        '''

        'value of N'
        jFieldNumMax = 0
        jMethodNumMax = 0
        countClass = 1
        for eachClass in projectInfo:
            self.classDict[countClass]=eachClass
            countClass+=1
            jFieldNumMax = max(len(eachClass.getField()),jFieldNumMax)
            jMethodNumMax = max(len(eachClass.getMethod()),jMethodNumMax)

        self.classNum = countClass-1
        self.N = max(jFieldNumMax,jMethodNumMax)

        'ROTypeDict'
        for each in self.ROtypeEnum:
            self.ROTypeDict[each.value]=each

    def decoding(self,encodedSequences):
        '''
        decode sequences of encoded binary sequence to ROType, class1Info, class2Info N
        :param: encodedSequences
        :return: refactoring operation type and its parameters
        '''
        results=[]
        for i in range(int(len(encodedSequences) / self.chromosomeLen)):
            ROType = self.ROTypeDict[encodedSequences[self.chromosomeLen * i+0]]
            class1Info = self.classDict[encodedSequences[self.chromosomeLen * i+1]]
            class2Info = self.classDict[encodedSequences[self.chromosomeLen * i+2]]
            N = encodedSequences[self.chromosomeLen * i+3]
            results.append(self._assemble(ROType,class1Info,class2Info,N))
        return results

    def _assemble(self,ROType,class1Info,class2Info,n):
        resDict={}
        resDict["ROType"]=ROType
        resDict["class1"]=class1Info
        resDict["class2"]=class2Info
        resDict["class1field"]=None
        resDict["class1method"]=None
        resDict["class2field"]=None
        resDict["class2method"]=None
        element = self._getElementOfN(ROType,class1Info,class2Info,n)

        if(ROType == RefactoringOperationEnum.INLINECLASS):
            resDict["class1method"] = "place_holder"

        elif(ROType == RefactoringOperationEnum.MOVEMETHOD):
            resDict["class1method"]=element

        elif (ROType == RefactoringOperationEnum.MOVEFIELD):
            resDict["class1field"]=element

        elif (ROType == RefactoringOperationEnum.PUSHDOWNMETHOD):
            resDict["class1method"]=element

        elif (ROType == RefactoringOperationEnum.PUSHDOWNFIELD):
            resDict["class1field"]=element

        elif (ROType == RefactoringOperationEnum.PULLUPMETHOD):
            resDict["class2method"]=element

        elif (ROType == RefactoringOperationEnum.PULLUPFIELD):
            resDict["class2field"]=element

        elif (ROType == RefactoringOperationEnum.NULL):
            pass

        return resDict

    def _getElementOfN(self,ROType,class1Info,class2Info,n):
        '''
        Get the element N represents for
        :param n: N
        :return:
        '''
        if(ROType == RefactoringOperationEnum.INLINECLASS):
            pass
        elif(ROType == RefactoringOperationEnum.MOVEMETHOD):
            if len(class1Info.getMethod()) !=0:
                return class1Info.getMethod()[n % len(class1Info.getMethod())]

        elif (ROType == RefactoringOperationEnum.MOVEFIELD):
            if len(class1Info.getField()) != 0:
                return class1Info.getField()[n % len(class1Info.getField())]

        elif (ROType == RefactoringOperationEnum.PUSHDOWNMETHOD):
            if len(class1Info.getMethod()) != 0:
                return class1Info.getMethod()[n % len(class1Info.getMethod())]

        elif (ROType == RefactoringOperationEnum.PUSHDOWNFIELD):
            if len(class1Info.getField()) != 0:
                return class1Info.getField()[n % len(class1Info.getField())]

        elif (ROType == RefactoringOperationEnum.PULLUPMETHOD):
            if len(class2Info.getMethod()) != 0:
                return class2Info.getMethod()[n % len(class2Info.getMethod())]

        elif (ROType == RefactoringOperationEnum.PULLUPFIELD):
            if len(class2Info.getField()) != 0:
                return class2Info.getField()[n % len(class2Info.getField())]

        elif (ROType == RefactoringOperationEnum.NULL):
            return None

        return None