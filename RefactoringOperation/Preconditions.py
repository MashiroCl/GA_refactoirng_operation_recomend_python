def inlineClassPreCondition(decodedBinarySequence,projectInfo):
    '''
    class1 and class2 is not the same class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class1"]==decodedBinarySequence["class2"]:
        return False
    return True

def moveMethodPreCondition(decodedBinarySequence,projectInfo):
    '''
    class1 contains method1 && class1 and class 2 is not the same class
    :param decodedBinarySequence:
    :param projectInfo:
    :return: if contains return false
    '''
    if decodedBinarySequence["class1method"] not in decodedBinarySequence["class1"]["method"].values:
        return False

    if decodedBinarySequence["class1"]==decodedBinarySequence["class2"]:
        return False

    return True

def moveFieldPreCondition(decodedBinarySequence,projectInfo):
    '''
    class1 contains field 1 &&cclass1 and class 2 is not the same class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class1field"] not in decodedBinarySequence["class1"]["field"].values:
        return False

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
    if decodedBinarySequence["class1method"] not in decodedBinarySequence["class1"]["method"].values:
        return False
    if decodedBinarySequence["class1"] not in decodedBinarySequence["class2"]["classInfo"].getSuperClass():
        return False

    return True

def pushDownFieldPreCondition(decodedBinarySequence,projectInfo):
    '''
    class1 contains field1 and class1 is class2's parent class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class1field"] not in decodedBinarySequence["class1"]["field"].values:
        return False
    if decodedBinarySequence["class1"] not in decodedBinarySequence["class2"]["classInfo"].getSuperClass():
        return False

    return True

def pullUpMethodPreCondition(decodedBinarySequence,projectInfo):
    '''
    class2 contains method2 && class1 is class2's parent class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class2method"] not in decodedBinarySequence["class2"]["method"].values:
        return False
    if decodedBinarySequence["class1"] not in decodedBinarySequence["class2"]["classInfo"].getSuperClass():
        return False

    return True

def pullUpFieldPreCondition(decodedBinarySequence,projectInfo):
    '''
    class2 contains field2 && class1 is class2's parent class
    :param decodedBinarySequence:
    :param projectInfo:
    :return:
    '''
    if decodedBinarySequence["class2field"] not in decodedBinarySequence["class2"]["field"].values:
        return False
    if decodedBinarySequence["class1"] not in decodedBinarySequence["class2"]["classInfo"].getSuperClass():
        return False

    return True