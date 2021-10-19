from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution
from Encoding.BinaryEncoding import BinaryEncoding
from RefactoringOperation.RefactoringOperationDispatcher import dispatch
from QMOOD.Qmood import Qmood
import random

class SearchROProblemBinary(BinaryProblem):
    def __init__(self,projectInfo):
        super(SearchROProblemBinary, self).__init__
        "7 objectives: QMOOD 6 metrics + code ownership"
        self.number_of_objectives=7
        "Only recommend one refactoring operation"
        self.number_of_variables=1
        #todo: Research on what are contraints for
        "No contraints"
        self.number_of_constraints=0

        'Qmood: maximize    code ownership: maximize'
        self.obj_directions=[self.MAXIMIZE,self.MAXIMIZE,self.MAXIMIZE,self.MAXIMIZE,self.MAXIMIZE,self.MAXIMIZE]
        self.obj_labels=['Effectiveness','Extendibility','Flexibility','Functionality','Resusability','Understandability']

        self.projectInfo = projectInfo
        binaryEncoding = BinaryEncoding()
        choromosomeLen=binaryEncoding.encoding(self.projectInfo)

        self.number_of_bits = choromosomeLen

    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        'Decode and execute'
        be = BinaryEncoding()
        decodedBinarySequences=be.decoding(solution.variables)
        "Execute corressponding refactoring operations"

        print("decodedBinarySequences is ",decodedBinarySequences)
        for each in decodedBinarySequences:
            dispatch(each["ROType"].value)(each, self.projectInfo)

        'calculate QMOOD  after executed refactoring operations'
        #todo: projectInfo.calculateQMood()
        qmood = Qmood()
        qmood.calculateQmood(self.projectInfo)
        effectiveness=qmood.getEffectiveness()
        extendibility=qmood.getExtendibility()
        flexibility=qmood.getFlexibility()
        functionality=qmood.getFunctionality()
        resusability=qmood.getResusability()
        understandability=qmood.getUnderstandability()

        solution.objectives[0] = -1.0 * effectiveness
        solution.objectives[1] = -1.0 * extendibility
        solution.objectives[2] = -1.0 * flexibility
        solution.objectives[3] = -1.0 * functionality
        solution.objectives[4] = -1.0 * resusability
        solution.objectives[5] = -1.0 * understandability

        'calculate ownership on refactoring operations applied files'
        #todo: projectInfo.calculateOwnership()

        return solution




    def create_solution(self) -> BinarySolution:
        newSolution = BinarySolution(number_of_objectives=self.number_of_objectives,
                                     number_of_variables=self.number_of_variables,
                                     number_of_constraints=self.number_of_constraints
                                     )
        newSolution.variables[0] = \
            [True if random.randint(0, 1) == 0 else False for _ in range(self.number_of_bits)]

        return newSolution

    def get_name(self) -> str:
        return "Search Refactoring Operation Problem"


