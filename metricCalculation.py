from jVariable import jVariable

# in each Field,
def DAM(jClass):
    field=jClass.getField()
    variableList=[]
    for each in field:
        variableList.append(jVariable(each))
    molecular=0
    denominator=len(field)
    if denominator==0:
        denominator=1
    else:
        for each in variableList:
            if each.getModifier()=="2":
                molecular=molecular+1
    DAM=molecular/denominator
    return DAM

def DCC():
    pass

def CAM():
    pass

#Number of user defined class variables in field
def MOA(jClassList,jClass):
    MOA=0
    classNameList=[]
    for eachC in jClassList:
        classNameList.append(eachC.getClassName())
    field=jClass.getField()
    for each in field:
        variable=jVariable(each)
        if variable.getType() in classNameList:
            print(variable.getName()+variable.getType()+" ")
            MOA=MOA+1
    return MOA


def MFA():
    pass

def NOP():
    pass

def CIS(jClass):
    CISNum=0
    methodList=jClass.getMethod()
    for each in methodList:
        if each.getModifier()=="1":
            CISNum=CISNum+1
    return CISNum

def NOM(jClass):
    methodNum=len(jClass.getMethod())
    return methodNum