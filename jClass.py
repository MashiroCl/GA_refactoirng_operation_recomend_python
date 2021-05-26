from jMethod import jMethod

class jClass:
    def __init__(self,load):
        self.load = load
        self.classInfo = self.load['className']
        self.fieldList=[]
        self.methodList=[]
        for each in self.load['jField']:

            self.fieldList.append(each)
        for each in self.load['jMethod']:
            self.methodList.append(jMethod(each))

    def getClass(self):
        return self.classInfo

    def getField(self):
        return self.fieldList
    def getMethod(self):
        return self.methodList

    def addMethod(self,jMethod):
        # print(jMethod.getFull())
        self.methodList.append(jMethod)



    def deleteMethod(self,jMethod):
        # print(jMethod.getFull())
        # print(self.methodList)
        self.methodList.remove(jMethod)
