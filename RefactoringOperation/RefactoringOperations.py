from .Preconditions import *
def inlineClass(decodedSequence,projectInfo):
    '''
    move all fields and methods from class1 to class2 and remove class1
    :param decodedSequence:
    :param projectInfo:
    :return:
    '''

    'check precondition'
    if not inlineClassPreCondition(decodedSequence,projectInfo):
        return

    'move method'
    for eachMethod in decodedSequence["class1"].getMethod():
        moveAMethod(decodedSequence["class1"],
                    decodedSequence["class2"],
                    eachMethod)

    for eachField in decodedSequence["class1"].getField():
        moveAField(decodedSequence["class1"],
                    decodedSequence["class2"],
                   eachField)
    # print(decodedSequence)
    # projectInfo.remove(decodedSequence["class1"])


def moveMethod(decodedSequence,projectInfo):
    '''
    move method1 from class1 to class2
    :param decodedSequence:
    :param projectInfo:
    :return:
    '''

    'check precondition'
    if not moveMethodPreCondition(decodedSequence,projectInfo):
        return

    'move method from class1 to class2'
    moveAMethod(decodedSequence["class1"],
                decodedSequence["class2"],
                decodedSequence["class1method"])


def moveField(decodedSequence,projectInfo):
    '''
    move field1 from class1 to class2
    :param decodedSequence:
    :param projectInfo:
    :return:
    '''

    'check precondition'
    if not moveFieldPreCondition(decodedSequence, projectInfo):
        return
    moveAField(decodedSequence["class1"],
                decodedSequence["class2"],
                decodedSequence["class1field"])


def pushDownField(decodedSequence,projectInfo):
    '''
    push field from parent class class1 to child class class2
    :param decodedSequence:
    :param projectInfo:
    :return:
    '''

    'check precondition'
    if not pushDownFieldPreCondition(decodedSequence, projectInfo):
        return
    moveAField(decodedSequence["class1"],
                decodedSequence["class2"],
                decodedSequence["class1field"])


def pushDownMethod(decodedSequence,projectInfo):
    '''
    push method from parent class to child class
    :param decodedSequence:
    :param projectInfo:
    :return:
    '''

    'check precondition'
    if not pushDownMethodPreCondition(decodedSequence, projectInfo):
        return
    moveAMethod(decodedSequence["class1"],
                decodedSequence["class2"],
                decodedSequence["class1method"])


def pullUpField(decodedSequence,projectInfo):
    '''
    pull field up from child class class2 to parent class class1
    :param decodedSequence:
    :param projectInfo:
    :return:
    '''

    'check precondition'
    if not pullUpFieldPreCondition(decodedSequence, projectInfo):
        return
    moveAField(decodedSequence["class2"],
                decodedSequence["class1"],
                decodedSequence["class2field"])


def pullUpMethod(decodedSequence,projectInfo):
    '''
    pull method up from child class class2 to parent class class1
    :param decodedSequence:
    :param projectInfo:
    :return:
    '''

    'check precondition'
    if not pullUpMethodPreCondition(decodedSequence, projectInfo):
        return
    moveAField(decodedSequence["class2"],
               decodedSequence["class1"],
               decodedSequence["class2method"])


def doNothing(decodedSequence,projectInfo):
    '''
    for future use
    :param decodedSequence:
    :param projectInfo:
    :return:
    '''
    # print("do Nothing, ",decodedSequence)
    pass

def moveAMethod(sourceCLass,targetClass,method):
    '''
    move a method from sourceClass to targetClass
    :param sourceCLass:
    :param targetClass:
    :param method:
    :return:
    '''
    # print("move a method")

    'check if target Class already contains method signatrue'
    signatureList = []
    for each in targetClass.getMethod():
        signatureList.append(each.getSignature())
    if method.getSignature() in signatureList:
        sourceCLass.removeMethod(method)
    else:
        # print("------------------------------------------------------------")
        # print(sourceCLass.getMethod())
        # print(targetClass.getMethod())
        targetClass.addMethod(method)
        sourceCLass.removeMethod(method)
        # print(sourceCLass.getMethod())
        # print(targetClass.getMethod())
        # print("------------------------------------------------------------")


def moveAField(sourceCLass,targetClass,field):
    '''
    move a field from sourceClass to targetClass
    :param sourceCLass:
    :param targetClass:
    :param field:
    :return:
    '''

    # print("move a field")

    'check if targetClass already has field'
    if field in targetClass.getField():
        sourceCLass.removeField(field)
    else:
        sourceCLass.removeField(field)
        targetClass.addField(field)