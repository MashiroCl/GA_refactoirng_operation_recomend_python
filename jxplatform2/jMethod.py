class jMethod:
    def __init__(self,method):
        self.method=method
        self.modifier=method.split("@")[0]
        self.name=method.split("@")[1]
        self.returnType=(method.split("@")[2]).split("#")[0]
        self.parameter=[]
        for each in method.split("#"):
            if "LOCAL: " in each:
                self.parameter.append(each.split("LOCAL: ")[1])

    def __repr__(self):
        return self.method

    def getModifier(self):
        return self.modifier
    def getName(self):
        return self.name
    def getReturnType(self):
        return self.returnType
    def getParameter(self):
        return self.parameter
    def getParameterName(self):
        name=[]
        for each in self.parameter:
            name.append(each.split("@")[0])
        return name
    def getParameterType(self):
        t=[]
        for each in self.parameter:
            t.append(each.split("@")[1])
        return t

    def getParameterPackage(self):
        packages = []
        for each in self.parameter:
            packages.append(each.split("@")[-1])
        return packages

    def getFull(self):
        return self.method

    def getSignature(self):
        return self.method
