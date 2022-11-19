from javamodel.jVariable import jVariable
from javamodel.jMethod import jMethod
from typing import List, Dict


# in each Field,
def DAM(jClass):
    field = jClass.getField()
    # print(field)
    variableList = []
    for each in field:
        variableList.append(jVariable(each))
    molecular = 0
    denominator = len(field)
    if denominator == 0:
        denominator = 1
    else:
        for each in variableList:
            if each.getModifier() == "2":
                molecular = molecular + 1
    return molecular / denominator


def getFPType(jClass) -> List[List]:
    cPType = []
    cFType = []
    for eachMethod in jClass.getMethod():
        for each2 in eachMethod.getParameterType():
            'Exclude generic signature,only package+class name remains'
            if '<' in each2:
                each2 = each2.split("<")[0]
            cPType.append(each2)
    cField = jClass.getField()
    for eachCField in cField:
        temp = jVariable(eachCField).getType()
        if '<' in temp:
            temp = temp.split("<")[0]
        cFType.append(temp)
    return cPType, cFType


def DCC(jClass, user_defined_classes):
    DCC = 0
    'cPType:Type of parameters of current class'
    'cPType:Type of field of current class'
    cPType, cFType = getFPType(jClass)
    for t in cPType:
        if t in user_defined_classes:
            DCC += 1
    for t in cFType:
        if t in user_defined_classes:
            DCC += 1
    return DCC


# ignore <clinit>
def ignore2(method):
    ign = 0
    return ign


def isStatic(jm):
    type = jm.getModifier()
    # static== 8 (1000)   15 (1111)
    # between 8 and 15 it should contains static
    static = 0
    if (int(type) >= 8 and int(type) <= 15):
        static = 1
    return static


def getArgsTypes(jm):
    result = set()
    if (ignore2(jm)):
        return result
    # Whether the method is static
    if not (isStatic(jm)):
        result.add("this")
    # Detect the parmeter typs of method
    pType = jm.getParameterType()
    for each in pType:
        result.add(each)

    return result


def CAM(jc):
    types = set()
    methods = jc.getMethod()
    numerator = 0
    denominator = 0
    # collect data about method arguments
    for each in methods:
        types = types.union(getArgsTypes(each))
    # count the metric
    for each in methods:
        if not ignore2(each):
            numerator = numerator + len(getArgsTypes(each))
            denominator = denominator + len(types)
    if (denominator == 0):
        denominator = 1
        numerator = 1
    CAM = numerator / denominator
    return CAM


# Number of user defined class variables in field
def MOA(jClass, user_defined_classes):
    MOA = 0
    field = jClass.getField()
    for each in field:
        variable = jVariable(each)
        if variable.getType() in user_defined_classes:
            # print(variable.getName()+variable.getType()+" ")
            MOA = MOA + 1
    return MOA


# ignore <init> and <clinit>
def ignore(mlist):
    ign = 0
    return ign


def getNumOfMethods(jc):
    # When the java.lang.Object is the parent
    # we do not analyze the parent's methods
    if "Object" in jc.getClassName():
        return 0
    else:
        mlist = jc.getMethod()
        return len(mlist) - ignore(mlist)


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
    pNumOfMeth = 0
    parents = jc.getSuperClass()
    for each in parents:
        pNumOfMeth = pNumOfMeth + getNumOfPCMethods(each)
    cNumofMeth = getNumOfMethods(jc)

    if (cNumofMeth + pNumOfMeth == 0):
        result = 1
    else:
        result = pNumOfMeth / (cNumofMeth + pNumOfMeth)
    # print(jc.getClassName())
    return result


# modifier,name, return type of method is a fingerPrint
def getFingerPrint(jm):
    fingerPrint = jm.getModifier() + "@" + jm.getName() + "@" + jm.getReturnType()
    # fingerPrint=1
    return fingerPrint


# number of polymorphic
def NOP(jc):
    # check each superclass
    # check each method
    # if superMethod has the same modifier,name,
    NOP = 0
    parentClasses = jc.getSuperClass()
    cMethodList = jc.getMethod()
    # get fingerprint of the current class
    cMethodListFingerPrint = []
    for each in cMethodList:
        cMethodListFingerPrint.append(getFingerPrint(each))

    for pClass in parentClasses:
        # get fingerprint of the parent class
        pMethodListFingerPrint = []
        pMethodList = []
        for each in pClass[1]:
            pMethodList.append(jMethod(each))
        for pEachMethod in pMethodList:
            pMethodListFingerPrint.append(getFingerPrint(pEachMethod))
        # Compare method finger print of parent class and current class
        for eachCMFP in cMethodListFingerPrint:
            if eachCMFP in pMethodListFingerPrint:
                NOP = NOP + 1
                break

    return NOP


def CIS(jClass):
    CISNum = 0
    methodList = jClass.getMethod()
    for each in methodList:
        if each.getModifier() == "1":
            CISNum = CISNum + 1
    return CISNum


def NOM(jClass):
    methodNum = len(jClass.getMethod())
    return methodNum


def DSC(length:int, inline_class_info: Dict[str, int]):
    '''
    Count of the total number of classes in design
    :param jClassList:
    :return: total number of classes in design
    '''
    return length+inline_class_info.get("DSC",0)


def count_hierarchies(java_classes):
    count = 0
    for each in java_classes:
        if len(each.getSuperClass()) == 0 and len(each.getChildren()) > 0:
            count = count + 1
    return count


def NOH(hierarchies: int, inline_class_info: Dict[str, int]):
    '''
    Count of the number of class hierarchies in the design
    If one class has only child classes without parent class (Class Object excleded, library class excluded -> only developer self-defined classes considered) is considered to be a root
	NOH = number of root
	As the Class Object has been filtered in the json file obtained from JXplatform2
	Other java.lang/java.util classes are temporaly not considered
    :return:
    '''
    return hierarchies + inline_class_info.get("NOH",0)


def count_classes_with_child_class(java_classes):
    return [each_class for each_class in java_classes if len(each_class.getChildren()) > 0]


def ANA(classes_with_child_class: int, inline_class_info: Dict[str, int], length: int):
    '''
    Average number of classes from which a class inherits information
    :return:
    '''
    return (classes_with_child_class + inline_class_info.get("ANA",0)) / length


def init_inline_class_info():
    '''
    initialize a map recording the information bring by refactoring operation Inline Class.
    The information can be used to calculate design-level metrics NOH, DSC, ANA
    '''
    inline_class_info = dict()
    inline_class_info["NOH"] = 0
    inline_class_info["DSC"] = 0
    inline_class_info["ANA"] = 0
    return inline_class_info



'''
_official methods are low-effective but calculate metric use the official definition
'''
def ANA_official(jClassList):
    '''
    Average number of classes from which a class inherits information
    :return:
    '''
    classWithChildClasses = [eachClass for eachClass in jClassList if len(eachClass.getChildren()) > 0]
    return len(classWithChildClasses) / len(jClassList)


def NOH_official(java_classes):
    '''
    Count of the number of class hierarchies in the design
    If one class has only child classes without parent class (Class Object excleded, library class excluded -> only developer self-defined classes considered) is considered to be a root
    NOH = number of root
    As the Class Object has been filtered in the json file obtained from JXplatform2
    Other java.lang/java.util classes are temporaly not considered
    :return:
    '''
    return count_hierarchies(java_classes)


def DSC_official(jClassList):
    '''
    Count of the total number of classes in design
    :param jClassList:
    :return: total number of classes in design
    '''
    return len(jClassList)
