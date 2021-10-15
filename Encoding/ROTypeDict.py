from RefactoringOperation.RefactoringOperationEnum import RefactoringOperationEnum
class ROTypeDict():
    def __init__(self):
        self.ROTypeDict = {}
        self.ROTypeLen = len(bin(len(RefactoringOperationEnum)).split("0b")[1])
        for each in RefactoringOperationEnum:
            self.ROTypeDict[self.toBinarySequence(each.value-1,self.ROTypeLen)]=each

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