from RefactoringOperation.RefactoringOperationEnum import RefactoringOperationEnum
from RefactoringOperation.RefactoringOperations import moveMethod,inlineClass

def dispatch(index:int):
    return {
        RefactoringOperationEnum.MOVEMETHOD.value: moveMethod,
        RefactoringOperationEnum.INCLINECLASS.value: inlineClass,
    }.get(index)


