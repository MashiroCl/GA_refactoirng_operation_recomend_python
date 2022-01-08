import enum


class RefactoringOperationEnum(enum.Enum):
    INLINECLASS = 1
    MOVEMETHOD = 2
    MOVEFIELD = 3
    PUSHDOWNMETHOD = 4
    PUSHDOWNFIELD = 5
    PULLUPMETHOD = 6
    PULLUPFIELD = 7
    NULL = 8
