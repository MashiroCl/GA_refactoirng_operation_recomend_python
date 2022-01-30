from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
import random
from code_ownership.CodeOwnership import CodeOwnership

from encoding.IntegerEncoding import IntegerEncoding
from refactoring_operation.RefactoringOperationDispatcher import dispatch
from qmood.Qmood import Qmood
import copy

class SearchROProblemInteger(IntegerProblem):
    def __init__(self, projectInfo, repoPath, developerGraph, ownershipPath):
        '''
        set basic parameters and encode current project
        :param projectInfo: project being processed, should be a list of jClass
        :param repository: repository of project being processed, used to do code ownership related manipulation,
        should be an entity of class Repository
        '''
        super(SearchROProblemInteger,self).__init__()
        "8 objectives: QMOOD 6 metrics + highest ownership+# of commiters"
        self.number_of_objectives = 2
        "4 variables decide a refactoring operation"
        self.number_of_variables = 4
        # todo: Research on what are contraints for
        "No contraints"
        self.number_of_constraints = 0
        "number of chromosome"
        self.number_of_refactorings = 10

        'Qmood: maximize    code ownership: maximize'
        self.obj_directions=[self.MAXIMIZE,
                             self.MAXIMIZE]

        self.obj_labels=['Quality Gain','Relatioinship Score']
        self.projectInfo = projectInfo
        self.repoPath = repoPath
        self.integerEncoding = IntegerEncoding()
        self.integerEncoding.encoding(self.projectInfo)
        self.lower_bound=[1, 1, 1, 1] *self.number_of_refactorings
        self.upper_bound=[self.integerEncoding.ROTypeNum,
                          self.integerEncoding.classNum,
                          self.integerEncoding.classNum,
                          self.integerEncoding.N]*self.number_of_refactorings
        self.initial_objectives = Qmood().calculateQmood(self.projectInfo)
        self.developerGraph = developerGraph
        self.ownershipPath = ownershipPath

    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        projectInfo = copy.deepcopy(self.projectInfo)
        self.integerEncoding.encoding(projectInfo)

        'Decode and execute'
        decodedIntegerSequences = self.integerEncoding.decoding(solution.variables)
        "Execute corressponding refactoring operations"


        for each in decodedIntegerSequences:
            dispatch(each["ROType"].value)(each, projectInfo)

        'calculate QMOOD  after executed refactoring operations'
        qmood_metrics_value = Qmood().calculateQmood(projectInfo)

        minus = -1
        qmood_metrics_list = ["Effectiveness", "Extendibility", "Flexibility", "Functionality", "Resusability",
                              "Understandability"]

        code_quality = minus * sum([(qmood_metrics_value[metric] - self.initial_objectives[metric]) for metric in qmood_metrics_list])

        solution.objectives[0] = code_quality

        'calculate ownership on refactoring operations applied files'
        relationship = CodeOwnership(self.ownershipPath).findAuthorPairList(decodedIntegerSequences).calculateRelationship(self.developerGraph)
        solution.objectives[1] = minus * relationship
        return solution

    def create_solution(self) -> IntegerSolution:
        newSolution = IntegerSolution(lower_bound=self.lower_bound,
                                      upper_bound=self.upper_bound,
                                      number_of_objectives=self.number_of_objectives,
                                      number_of_constraints=self.number_of_constraints)
        newSolution.variables = \
            [int(random.uniform(self.lower_bound[i] * 1.0, self.upper_bound[i] * 1.0))
             for i in range(self.number_of_variables*self.number_of_refactorings)]
        return newSolution

    def get_name(self) -> str:
        return "Search Refactoring Operation Problem"