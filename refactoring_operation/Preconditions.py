def inlineClassPreCondition(decodedBinarySequence, projectInfo):
    '''
    class1 and class2 is not the same class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class1"]==decodedBinarySequence["class2"] or\
            decodedBinarySequence["class1"] not in projectInfo:
        return False
    return True

def moveMethodPreCondition(decodedBinarySequence,projectInfo):
    '''
    class1 contains method1 && class1 and class 2 is not the same class
    :param decodedBinarySequence:
    :param projectInfo:
    :return: if contains return false
    '''
    'method1 is contained by class1'
    if decodedBinarySequence["class1method"] not in decodedBinarySequence["class1"].getMethod():
        return False
    'class1 and class2 is not the same class'
    if decodedBinarySequence["class1"]==decodedBinarySequence["class2"]:
        return False

    return True

def moveFieldPreCondition(decodedBinarySequence,projectInfo):
    '''
    class1 contains field 1 &&class1 and class 2 is not the same class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    'check class1 contains field1'
    if decodedBinarySequence["class1field"] not in decodedBinarySequence["class1"].getField():
        return False
    'check class1 and class2 is not the same class'
    if decodedBinarySequence["class1"]==decodedBinarySequence["class2"]:
        return False

    return True


def pushDownMethodPreCondition(decodedBinarySequence,projectInfo):
    '''
    class1 contains method1 and class1 is class2's parent class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class1method"] not in decodedBinarySequence["class1"].getMethod():
        return False
    if decodedBinarySequence["class1"] not in decodedBinarySequence["class2"].getSuperClass():
        return False

    return True

def pushDownFieldPreCondition(decodedBinarySequence,projectInfo):
    '''
    class1 contains field1 and class1 is class2's parent class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class1field"] not in decodedBinarySequence["class1"].getField():
        return False
    if decodedBinarySequence["class1"] not in decodedBinarySequence["class2"].getSuperClass():
        return False

    return True

def pullUpMethodPreCondition(decodedBinarySequence,projectInfo):
    '''
    class2 contains method2 && class1 is class2's parent class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class2method"] not in decodedBinarySequence["class2"].getMethod():
        return False
    if decodedBinarySequence["class1"] not in decodedBinarySequence["class2"].getSuperClass():
        return False

    return True

def pullUpFieldPreCondition(decodedBinarySequence,projectInfo):
    '''
    class2 contains field2 && class1 is class2's parent class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class2field"] not in decodedBinarySequence["class2"].getField():
        return False
    if decodedBinarySequence["class1"] not in decodedBinarySequence["class2"].getSuperClass():
        return False

    return True