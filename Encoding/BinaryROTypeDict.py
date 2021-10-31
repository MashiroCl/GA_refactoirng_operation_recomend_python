from RefactoringOperation.RefactoringOperationEnum import RefactoringOperationEnum
class ROTypeDict():
    def __init__(self):
        self.ROTypeDict = {}
        self.ROTypeLen = len(bin(len(RefactoringOperationEnum)-1).split("0b")[1])
        count=0
        for each in RefactoringOperationEnum:
            self.ROTypeDict[self.toBinarySequence(count,self.ROTypeLen)]=each
            count=count+1

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

    def findROType(self,value):
        try:
            res = self.ROTypeDict[value]
        except KeyError:
            res = None
        return res