class jMethod():
    def __init__(self,method):
        self.method=method
        self.modifier=method.split("@")[0]
        self.name=method.split("@")[1]
        self.returnType=(method.split("@")[2]).split("#")[0]
        self.parameter=[]
        for each in method.split("#"):
            if "LOCAL: " in each:
                self.parameter.append(each.split("LOCAL: ")[1])

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
        type=[]
        for each in self.parameter:
            type.append(each.split("@")[0])
        return type

    def getFull(self):
        return self.method
