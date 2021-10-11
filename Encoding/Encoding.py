class Encoding():
    def __init__(self):
        pass

    def getBinaryLengthByNumber(self,number:int)->int:
        '''
        get binary sequence length of number
        :param
        :return: binary sequence length
        '''
        return len(bin(number).split("0b")[1])


    def binaryEncodingFixedLength(self, length:int, number:int)->str:
        '''
        :param length: length of final binary sequence
        :param number: number being converted
        :return: binary encoded number string
        '''
        body = bin(number).split("0b")[1]
        head = (length - len(body)) * "0"
        result=head+body
        return result

    def divideBinarySequence(self, str, lengthList:list):
        '''
        :param str: binary sequence
        :param list:  each value in list represent length of one element such as class, method
        :return: list of binary sequence represent each element
        '''
        result=[]
        start=0
        for each in lengthList:
            result.append(str[start:start+each])
            start=start+each
        return result

if __name__ =="__main__":
    encoding = Encoding()
    res=encoding.binaryEncodingFixedLength(encoding.getBinaryLengthByNumber(8), 2)
    print(res)
    print(encoding.getBinaryLengthByNumber(8))