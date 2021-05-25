class jClass:
    load=None
    classInfo=None
    fieldList=[]
    methodList=[]

    def __init__(self,load):
        self.load = load
        self.classInfo = load['className']
        for each in load['jField']:
            self.fieldList.append(each)
        for each in load['jMethod']:
            self.methodList.append(each)


    def getClass(self):
        return self.classInfo

    def getField(self):
        return self.fieldList
    def getMethod(self):
        return self.methodList
