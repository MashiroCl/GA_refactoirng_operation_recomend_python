from jClass import jClass
#Use result of Jxplatform2 to simulate moving method
def moveMethod(jMethod,jClass1,jClass2):
    jClass1.deleteMethod(jMethod)
    jClass2.addMethod(jMethod)


