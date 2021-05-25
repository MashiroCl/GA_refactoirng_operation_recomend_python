class jVariable:

    def __init__(self,sField):
        self.modifier = sField.split("#")[0]
        self.name = (sField.split("#")[1]).split("@")[0]
        self.type = (sField.split("#")[1]).split("@")[1]

    def getModifier(self):
        return self.modifier
    def getName(self):
        return self.name
    def getType(self):
        return self.type