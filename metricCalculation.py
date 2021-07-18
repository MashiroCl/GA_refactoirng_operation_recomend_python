from jVariable import jVariable
from jMethod import jMethod
from jClass import jClass

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


def getFPType(jClass):
    cPType=[]
    cFType=[]
    for eachMethod in jClass.getMethod():
        for each2 in eachMethod.getParameterType():
            cPType.append(each2.split(".")[-1])
    cField=jClass.getField()
    for eachCField in cField:
        cFType.append(jVariable(eachCField).getType().split(".")[-1])
    return cPType,cFType

def isIn(l1,l2):
    lTemp=[]
    for each in l1:
        if each in l2:
            lTemp.append(each)
    return lTemp

def DCC(jClass,jClassList):
    DCC=0
    'cPType:Type of parameters of current class'
    'cPType:Type of field of current class'
    cPType,cFType=getFPType(jClass)
    cDict={}
    cList=[]
    for each2 in jClassList:
        if each2==jClass:
            pass
        elif each2.getClassName() in cPType:
            cList.append(each2.getClassName())
        elif each2.getClassName() in cFType:
            cList.append(each2.getClassName())
    DCC=DCC+len(cList)
    if len(cList)!=0:
        cDict[jClass.getClassName()]=cList

    # for each in jClassList:
    #     # if each.getClassName() == "ClassMetricsTest":
    #     #     cPType1, cFType1 = getFPType(each)
    #     #     print(cPType1, cFType1)
    #     cPType,cFType=getFPType(each)
    #     cDict={}
    #     cList=[]
    #     for each2 in jClassList:
    #         if each2==each:
    #             pass
    #         elif each2.getClassName() in cPType:
    #             cList.append(each2.getClassName())
    #         elif each2.getClassName() in cFType:
    #             cList.append(each2.getClassName())
    #         # PType,FType=getFPType(each2)
    #         # lP=isIn(cPType,PType)
    #         # lF=isIn(cFType,FType)
    #         # # print("lP ",lP)
    #         # # print("lF", lF)
    #         # for lPEach in lP:
    #         #     cDict[lPEach]=each2.getClassName()
    #         # for lFEach in lF:
    #         #     cDict[lFEach]=each2.getClassName()
    #     DCC=DCC+len(cList)
    #     if len(cList)!=0:
    #         cDict[each.getClassName()]=cList


    return DCC

#ignore <clinit>
def ignore2(method):
    ign=0
    return ign
def isStatic(jm):
    type=jm.getModifier();
    #static== 8 (1000)   15 (1111)
    #between 8 and 15 it should contains static
    static=0
    if(int(type)>=8 and int(type)<=15):
        static=1
    return static

def getArgsTypes(jm):
    result=set()
    if(ignore2(jm)):
        return result
    #Whether the method is static
    if not (isStatic(jm)):
        result.add("this")
    #Detect the parmeter typs of method
    pType=jm.getParameterType()
    for each in pType:
        result.add(each)

    return result

def CAM(jc):
    CAM=0
    types=set()
    methods=jc.getMethod()
    numerator=0
    denominator=0
    #collect data about method arguments
    for each in methods:
        types=types.union(getArgsTypes(each))
    #count the metric
    for each in methods:
        if not ignore2(each):
            numerator=numerator+len(getArgsTypes(each))
            denominator=denominator+len(types)
    if(denominator==0):
        denominator=1
    CAM=numerator/denominator
    return CAM

#Number of user defined class variables in field
def MOA(jClass,jClassList):
    MOA=0
    classNameList=[]
    for eachC in jClassList:
        classNameList.append(eachC.getPackage()+"."+eachC.getClassName())
    field=jClass.getField()
    for each in field:
        variable=jVariable(each)
        if variable.getType() in classNameList:
            # print(variable.getName()+variable.getType()+" ")
            MOA=MOA+1
    return MOA

#ignore <init> and <clinit>
def ignore(mlist):
    ign=0
    return ign
def getNumOfMethods(jc):
    #When the java.lang.Object is the parent
    #we do not analyze the parent's methods
    if "Object" in jc.getClassName():
        return 0
    else:
        mlist=jc.getMethod()
        return len(mlist)-ignore(mlist)

def getNumOfPCMethods(jc):
    className = jc[0]
    methodL = jc[1]
    # print(className)
    # print("methodL is ", methodL)
    return len(methodL) - ignore(methodL)

#todo modify MFA
def MFA(jc):
    pNumOfMeth=0
    parents=jc.getSuperClass()
    for each in parents:
        pNumOfMeth=pNumOfMeth+getNumOfPCMethods(each)
    cNumofMeth=getNumOfMethods(jc)

    if(cNumofMeth+pNumOfMeth==0):
        result=0
    else:
        result=pNumOfMeth/(cNumofMeth+pNumOfMeth)

    return result

#modifier,name, return type of method is a fingerPrint
def getFingerPrint(jm):
    fingerPrint=jm.getModifier()+"@"+jm.getName()+"@"+jm.getReturnType()
    # fingerPrint=1
    return fingerPrint

#number of polymorphic
def NOP(jc):
    # check each superclass
      #check each method
         #if superMethod has the same modifier,name,
    NOP=0
    parentClasses=jc.getSuperClass()
    cMethodList=jc.getMethod()
    #get fingerprint of the current class
    cMethodListFingerPrint=[]
    for each in cMethodList:
        cMethodListFingerPrint.append(getFingerPrint(each))

    for pClass in parentClasses:
        # get fingerprint of the parent class
        pMethodListFingerPrint = []
        pMethodList=[]
        for each in pClass[1]:
            pMethodList.append(jMethod(each))
        for pEachMethod in pMethodList:
            pMethodListFingerPrint.append(getFingerPrint(pEachMethod))
        #Compare method finger print of parent class and current class
        for eachCMFP in cMethodListFingerPrint:
            if eachCMFP in pMethodListFingerPrint:
                NOP=NOP+1
                break

    return NOP
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

def DSC():
    return 0
def NOH():
    return 0
def ANA():
    return 0
