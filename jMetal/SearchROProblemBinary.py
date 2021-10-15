from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution
from Encoding.BinaryEncoding import BinaryEncoding
from RefactoringOperation.RefactoringOperationDispatcher import dispatch

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

        #todo
        self.projectInfo = projectInfo
        binaryEncoding = BinaryEncoding()
        choromosomeLen=binaryEncoding.encoding(self.projectInfo)

        self.number_of_bits = choromosomeLen

    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        pass
        #todo Decode
        decodedBinarySequences=BinaryEncoding.decoding(BinaryEncoding(),solution.variables)
        "Execute corressponding refactoring operations"
        for each in decodedBinarySequences:
            dispatch(each[0])(each,self.projectInfo)
        #todo: projectInfo.calculateQMood()
        #todo: projectInfo.calculateOwnership()
        #todo: solution.objectives[0][1]..




    def create_solution(self) -> BinarySolution:
        newSolution = BinarySolution(number_of_objectives=self.number_of_objectives,
                                     number_of_variables=self.number_of_variables,
                                     number_of_constraints=self.number_of_constraints
                                     )


    def get_name(self) -> str:
        return "Search Refactoring Operation Problem"


