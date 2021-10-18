from .jMethod import jMethod
class jClass:
    def __init__(self,load):
        self.load = load
        self.classInfo = self.load['className']
        self.fieldList=[]
        self.methodList=[]
        self.childrenList=[]
        self.superClassList=[]
        self.package=self.load['javaPackage']
        for each in self.load['javaFields']:
            self.fieldList.append(each)
        for each in self.load['javaMethods']:
            self.methodList.append(jMethod(each))
        # for each in self.load['children']:
        #     self.childrenList.append(each)
        for each in self.load['superClasses']:
            self.superClassList.append(each)
        self.filePath=self.load['filePath']

        "If this class is a test class"
        self.testClass=self.isTestClass()


    def getClass(self):
        return self.classInfo
    def getClassName(self):
        return self.classInfo.split("#")[1]

    def getParameters(self):
        pass

    def getField(self):
        return self.fieldList
    def getMethod(self):
        return self.methodList

    def getChildren(self):
        return self.childrenList
    def getSuperClass(self):
        return self.superClassList

    def addMethod(self,jMethod):
        if self.hasMethod(jMethod):
            print("Method already exist in the class")
        else:
            self.methodList.append(jMethod)

    def removeMethod(self, jMethod):
        'Precondition: the source class has the method to be moved'
        if self.hasMethod(jMethod):
            self.methodList.remove(jMethod)
        else:
            print(jMethod," doesn't exist in the class")


    def hasMethod(self,jMethod):
        'Use '
        if jMethod in self.methodList:
            return 1
        else:
            return 0
    def getPackage(self):
        return self.package

    def setFilePath(self,filePath:str):
        self.filePath=filePath

    def getFilePath(self)->str:
        return self.filePath

    def isTestClass(self):
        if self.classInfo.split("#")[0] == str(0):
            return True
        return False

    def hasField(self,field):
        if field in self.fieldList:
            return True
        return False

    def addField(self,field):
        self.fieldList.append(field)

    def removeField(self,field):
        if field in self.fieldList:
            self.fieldList.remove(field)
        else:
            print(field," doesn't exist in the class")
