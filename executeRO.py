#Use result of Jxplatform2 to simulate moving method
class ExecuteRO():
    def __init__(self):
        pass
    def moveMethod(self,jMethod,jClass1,jClass2):
        jClass1.removeMethod(jMethod)
        jClass2.addMethod(jMethod)