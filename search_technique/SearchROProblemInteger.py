import copy
import random
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from code_ownership.CodeOwnership import CodeOwnership
from encoding.IntegerEncoding import IntegerEncoding
from qmood.Qmood import Qmood
from refactoring_operation.RefactoringOperationDispatcher import dispatch
from semantic.NameExtractor import NameExtractor
from semantic.Vectorize import TF_IDF



class SearchROProblemInteger(IntegerProblem):
    """
    Integer encoding problem which
    """
    def __init__(self, projectInfo, repoPath, developerGraph, ownershipPath):
        '''
        set basic parameters and encode current project
        :param projectInfo: project being processed, should be a list of jClass
        should be an entity of class Repository
        '''
        super(SearchROProblemInteger, self).__init__()
        "2 objectives: QMOOD-> Quality Gain + commiters relationship + semantic coherence"
        self.number_of_objectives = 3
        "4 variables decide a refactoring operation"
        self.number_of_variables = 4
        # todo: Research on what are contraints for
        "No contraints"
        self.number_of_constraints = 0
        "number of chromosome"
        self.number_of_refactorings = 10

        'Qmood: maximize    code ownership: maximize'
        self.obj_directions=[self.MAXIMIZE,
                             self.MAXIMIZE,
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
        self.tf_idf = TF_IDF()
        self.classes_nameSequence_dict = self.extract_names_sequences()

    def extract_names_sequences(self):
        name_extractor = NameExtractor()
        names_dict = name_extractor.extract(projectInfo=self.projectInfo)
        sequence_dict = name_extractor.dict_names_to_dict_sequence(names_dict)
        return sequence_dict

    def vectorize_classes(self, classes):
        res = list()
        for each in classes:
            res.append(self.classes_nameSequence_dict[each.getKey()][0])
        return self.tf_idf.vectorize(res)

    def calc_cosine_similarity(self, doc_metric):
        return self.tf_idf.cosine_similarity(doc_metric)

    def calc_sematic_coherence(self, decoded_sequences):
        res =0
        for each in decoded_sequences:
            X = self.vectorize_classes([each["class1"], each["class2"]])
            cosine_smiliarity = self.calc_cosine_similarity(X).tolist()[1]
            res +=cosine_smiliarity
        return res

    def exec_RO(self, decoded_sequences, projectInfo):
        for each in decoded_sequences:
            dispatch(each["ROType"].value)(each, projectInfo)

    def calc_quality_gain(self, projectInfo):
        qmood_metrics_list = ["Effectiveness", "Extendibility", "Flexibility", "Functionality", "Resusability",
                              "Understandability"]

        qmood_metrics_value = Qmood().calculateQmood(projectInfo)
        return sum([(qmood_metrics_value[metric] - self.initial_objectives[metric]) for metric in qmood_metrics_list])

    def calc_relationship(self, decoded_sequencs):
        return CodeOwnership(self.repoPath,self.ownershipPath).findAuthorPairList(decoded_sequencs).\
            calculateRelationship(self.developerGraph)



    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        projectInfo = copy.deepcopy(self.projectInfo)
        self.integerEncoding.encoding(projectInfo)

        'Decode and execute'
        decodedIntegerSequences = self.integerEncoding.decoding(solution.variables)

        "Execute corresponding refactoring operations"
        self.exec_RO(decodedIntegerSequences, projectInfo)

        'calculate Quality Gain after executed refactoring operatins'
        quality_gain = self.calc_quality_gain(projectInfo)

        'calculate QMOOD  after executed refactoring operations'
        solution.objectives[0] = -1 * quality_gain

        'calculate ownership on refactoring operations applied files'
        relationship = self.calc_relationship(decodedIntegerSequences)
        solution.objectives[1] = -1 * relationship

        'calculate semantic coherence on refactoring operations applied classes'
        semantic_coherence = self.calc_sematic_coherence(decodedIntegerSequences)
        solution.objectives[2] = -1 * semantic_coherence

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