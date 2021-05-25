class jClass:
    def __init__(self,load):
        self.load = load
        self.classInfo = self.load['className']
        self.fieldList=[]
        self.methodList=[]
        for each in self.load['jField']:

            self.fieldList.append(each)
        for each in self.load['jMethod']:
            self.methodList.append(each)

    def getClass(self):
        return self.classInfo

    def getField(self):
        return self.fieldList
    def getMethod(self):
        return self.methodList
