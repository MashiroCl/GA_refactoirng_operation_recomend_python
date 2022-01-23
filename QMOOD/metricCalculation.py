from Jxplatform2.jVariable import jVariable
from Jxplatform2.jMethod import jMethod

# in each Field,
def DAM(jClass):
    field=jClass.getField()
    # print(field)
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
        denominator = 1
        numerator = 1
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


def MFA(jc):
    '''
    For a class A, whose parents named as Ca, MFA=(#methods of Ca/#methods of Ca+#methods of A)
    Only developer defined class is considered beacuse Jxplatform2 cannot extract info from library class
    :param jc:
    :return:
    '''
    pNumOfMeth=0
    parents=jc.getSuperClass()
    for each in parents:
        pNumOfMeth=pNumOfMeth+getNumOfPCMethods(each)
    cNumofMeth=getNumOfMethods(jc)

    if(cNumofMeth+pNumOfMeth==0):
        result=1
    else:
        result=pNumOfMeth/(cNumofMeth+pNumOfMeth)
    # print(jc.getClassName())
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

def DSC(jClassList):
    '''
    Count of the total number of classes in design
    :param jClassList:
    :return: total number of classes in design
    '''
    return len(jClassList)


def NOH(jClassList):
    '''
    Count of the number of class hierarchies in the design
    If one class has only child classes without parent class (Class Object excleded, library class excluded -> only developer self-defined classes considered) is considered to be a root
	NOH = number of root
	As the Class Object has been filtered in the json file obtained from JXplatform2
	Other java.lang/java.util classes are temporaly not considered
    :return:
    '''
    count = 0
    for each in jClassList:
        if len(each.getSuperClass())==0 and len(each.getChildren())>0:
            count = count +1
    return count

def ANA(jClassList):
    '''
    Average number of classes from which a class inherits information
    :return:
    '''
    classWithChildClasses = [eachClass for eachClass in jClassList if len(eachClass.getChildren())>0]
    return len(classWithChildClasses)/len(jClassList)
