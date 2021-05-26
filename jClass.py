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
        if self.hasMethod(jMethod):
            print("Method already exist in the class")
        else:
            self.methodList.append(jMethod)

    def deleteMethod(self,jMethod):
        if self.hasMethod(jMethod):
            self.methodList.remove(jMethod)
        else:
            print("Method being moved doesn't exist in the class")


    def hasMethod(self,jMethod):
        if jMethod in self.methodList:
            return 1
        else:
            return 0