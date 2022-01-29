from refactoring_operation.RefactoringOperationEnum import RefactoringOperationEnum
from refactoring_operation.RefactoringOperations import *

def dispatch(index:int):
    return {
        RefactoringOperationEnum.INLINECLASS.value: inlineClass,
        RefactoringOperationEnum.MOVEMETHOD.value: moveMethod,
        RefactoringOperationEnum.MOVEFIELD.value: moveField,
        RefactoringOperationEnum.PUSHDOWNMETHOD.value:pushDownMethod,
        RefactoringOperationEnum.PUSHDOWNFIELD.value:pushDownField,
        RefactoringOperationEnum.PULLUPMETHOD.value:pullUpMethod,
        RefactoringOperationEnum.PULLUPFIELD.value:pullUpField,
        RefactoringOperationEnum.NULL.value:doNothing
    }.get(index)


