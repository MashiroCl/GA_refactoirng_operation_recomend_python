from RefactoringOperation.RefactoringOperationEnum import RefactoringOperationEnum
from RefactoringOperation.RefactoringOperations import *

def dispatch(index:int):
    return {
        RefactoringOperationEnum.INCLINECLASS.value: inlineClass,
        RefactoringOperationEnum.MOVEMETHOD.value: moveMethod,
        RefactoringOperationEnum.MOVEFIELD.value: moveField,
        RefactoringOperationEnum.PUSHDOWNMETHOD.value:pushDownMethod,
        RefactoringOperationEnum.PUSHDOWNFIELD.value:pushDownField,
        RefactoringOperationEnum.PULLUPMETHOD.value:pullUpMethod,
        RefactoringOperationEnum.PULLUPFIELD.value:pullUpField,
        RefactoringOperationEnum.NULL.value:doNothing
    }.get(index)


