class Encoding():
    def __init__(self):
        pass
    def binaryEncoding(self,length:int,no:int)->str:
        binaryLen=len(bin(length).split("0b")[1])-2
        body = bin(no).split("0b")[1]
        head = (binaryLen - len(body)) * "0"
        result=head+body
        return result

    def binaryDecoding(self,str,list:list):
        '''
        :param str: binary sequence
        :param list:  each value in list represent length of one element such as class, method
        :return: list of binary sequence represent each element
        '''
        result=[]
        temp=0
        for each in list:
            result.append(str[temp:temp+each])
            temp=temp+each
        return result

if __name__=="__main__":
    # a=[1,2,3,4,5,6,7]
    # e=Encoding()
    # bE=e.binaryEncoding(a)
    # dict=dict()
    # for i in range(len(a)):
    #     dict[bE[i]]=a[i]
    # print(dict)

    string="123456789"
    l=[2,3,4]
    e=Encoding()
    print(e.binaryDecoding(string,l))