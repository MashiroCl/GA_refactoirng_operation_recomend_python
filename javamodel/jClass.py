from javamodel.jMethod import jMethod


class jClass:
    def __init__(self,load):
        self.load = load
        self.classInfo = self.load['className']
        self.fieldList=[]
        self.methodList=[]
        self.childrenList=self.load['childClasses']
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

        "If this class is a test class, then test.class is true"
        self.testClass = self.isTestClass()
        "If this class is an anonymous class, then anonymous_class is true"
        self.anonymous_class = self.isAnonymousClass()
        "use filepath and class name as signature of a class"
        self.className = self.classInfo.split("#")[1]
        self.key = self.filePath + "#" +self.className

    def getClass(self):
        return self.classInfo
    def getClassName(self):
        return self.className

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
    def getKey(self):
        return self.key

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

        if jMethod in self.methodList:
            return 1
        else:
            return 0
    def getPackage(self):
        return self.package

    def setFilePath(self,filePath:str):
        self.filePath=filePath

    def getRelativeFilePath(self):
        '''
        return file path after "src"
        '''
        return self.filePath.split("/src/")[1]

    def getFilePath(self)->str:
        return self.filePath

    def isTestClass(self):
        """
        /../test/../ or class Testxxx, then it must be a test class
        """
        if "test" in self.filePath or "Test" in self.filePath :
            return True
        # Why I use this as the criterion to distinguish test class before?
        # if self.classInfo.split("#")[0] == str(0):
        #     return True
        return False

    def isAnonymousClass(self):
        """
        no name in classInfo is anonymous inner class
        :return:
        """
        if not self.classInfo.split("#")[1]:
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
