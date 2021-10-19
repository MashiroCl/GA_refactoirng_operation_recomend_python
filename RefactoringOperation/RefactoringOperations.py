from .Preconditions import *
def inlineClass(decodedBinarySequence,projectInfo):
    '''
    move all fields and methods from class1 to class2 and remove class1
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    'check decoded binary sequence has null element'
    if None in decodedBinarySequence.values():
        return
    'check precondition'
    if not inlineClassPreCondition(decodedBinarySequence,projectInfo):
        return

    'move method'
    for eachMethod in decodedBinarySequence["class1"]["classInfo"].getMethod():
        moveAMethod(decodedBinarySequence["class1"]["classInfo"],
                    decodedBinarySequence["class2"]["classInfo"],
                    eachMethod)

    for eachField in decodedBinarySequence["class1"]["classInfo"].getField():
        moveAField(decodedBinarySequence["class1"]["classInfo"],
                    decodedBinarySequence["class2"]["classInfo"],
                   eachField)

    #todo remove class1 in projectInfo
    projectInfo.remove(decodedBinarySequence["class1"])

def moveMethod(decodedBinarySequence,projectInfo):
    '''
    move method1 from class1 to class2
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    'check decoded binary sequence has null element'
    if None in decodedBinarySequence.values():
        return
    'check precondition'
    if not moveMethodPreCondition(decodedBinarySequence,projectInfo):
        return

    'move method from class1 to class2'
    moveAMethod(decodedBinarySequence["class1"]["classInfo"],
                decodedBinarySequence["class2"]["classInfo"],
                decodedBinarySequence["class1method"])

def moveField(decodedBinarySequence,projectInfo):
    '''
    move field1 from class1 to class2
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    'check decoded binary sequence has null element'
    if None in decodedBinarySequence.values():
        return
    'check precondition'
    if not moveFieldPreCondition(decodedBinarySequence, projectInfo):
        return
    moveAField(decodedBinarySequence["class1"]["classInfo"],
                decodedBinarySequence["class2"]["classInfo"],
                decodedBinarySequence["class1field"])

def pushDownField(decodedBinarySequence,projectInfo):
    '''
    push field from parent class class1 to child class class2
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    'check decoded binary sequence has null element'
    if None in decodedBinarySequence.values():
        return
    'check precondition'
    if not pushDownFieldPreCondition(decodedBinarySequence, projectInfo):
        return
    moveAField(decodedBinarySequence["class1"]["classInfo"],
                decodedBinarySequence["class2"]["classInfo"],
                decodedBinarySequence["class1field"])

def pushDownMethod(decodedBinarySequence,projectInfo):
    '''
    push method from parent class to child class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    'check decoded binary sequence has null element'
    if None in decodedBinarySequence.values():
        return
    'check precondition'
    if not pushDownMethodPreCondition(decodedBinarySequence, projectInfo):
        return
    moveAMethod(decodedBinarySequence["class1"]["classInfo"],
                decodedBinarySequence["class2"]["classInfo"],
                decodedBinarySequence["class1method"])

def pullUpField(decodedBinarySequence,projectInfo):
    '''
    pull field up from child class class2 to parent class class1
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    'check decoded binary sequence has null element'
    if None in decodedBinarySequence.values():
        return
    'check precondition'
    if not pullUpFieldPreCondition(decodedBinarySequence, projectInfo):
        return
    moveAField(decodedBinarySequence["class2"]["classInfo"],
                decodedBinarySequence["class1"]["classInfo"],
                decodedBinarySequence["class2field"])

def pullUpMethod(decodedBinarySequence,projectInfo):
    '''
    pull method up from child class class2 to parent class class1
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    'check decoded binary sequence has null element'
    if None in decodedBinarySequence.values():
        return
    'check precondition'
    if not pullUpMethodPreCondition(decodedBinarySequence, projectInfo):
        return
    moveAField(decodedBinarySequence["class2"]["classInfo"],
               decodedBinarySequence["class1"]["classInfo"],
               decodedBinarySequence["class2method"])

def doNothing(decodedBinarySequence,projectInfo):
    '''
    for future use
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    print("do Nothing, ",decodedBinarySequence,projectInfo)
    pass

def moveAMethod(sourceCLass,targetClass,method):
    '''
    move a method from sourceClass to targetClass
    :param sourceCLass:
    :param targetClass:
    :param method:
    :return:
    '''
    'check if target Class already contains method signatrue'
    signatureList = []
    for each in targetClass.getMethod():
        signatureList.append(each.getSignature())
    if method.getSignature() in signatureList:
        sourceCLass.removeMethod(method)
    else:
        targetClass.addMethod(method)
        sourceCLass.removeMethod(method)


def moveAField(sourceCLass,targetClass,field):
    '''
    move a field from sourceClass to targetClass
    :param sourceCLass:
    :param targetClass:
    :param field:
    :return:
    '''
    'check if targetClass already has field'
    if field in targetClass.getField():
        sourceCLass.removeField(field)
    else:
        sourceCLass.removeField(field)
        targetClass.addField(field)