import copy
import random
from typing import List
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from encoding.IntegerEncoding import IntegerEncoding
from qmood.Qmood import Qmood
from refactoring_operation.RefactoringOperationDispatcher import dispatch
from semantic.NameExtractor import NameExtractor
from semantic.Vectorize import TF_IDF
from search_technique.enviroment import Platform


class SearchROProblemNRE(IntegerProblem):
    """
    Integer encoding problem which
    """
    def __init__(self, abs_representation, platform: Platform):
        '''
        set basic parameters and encode current project
        :param abs_representation: project being processed, should be a list of jClass
        should be an entity of class Repository
        '''
        super(SearchROProblemNRE, self).__init__()
        "2 objectives: QMOOD-> Quality Gain + semantic coherence"
        self.number_of_objectives = 2
        "4 variables decide a refactoring operation"
        self.number_of_variables = 4
        # todo: Research on what are contraints for
        "No contraints"
        self.number_of_constraints = 0
        "number of chromosome"
        self.number_of_refactorings = 20

        'Qmood: maximize    code ownership: maximize'
        self.obj_directions=[self.MAXIMIZE,
                             self.MAXIMIZE,
                             self.MAXIMIZE]

        self.obj_labels=['Quality Gain','Relatioinship Score']
        self.abs_representation = abs_representation
        self.repo_path = platform.repo_path
        self.integer_encoding = IntegerEncoding()
        self.integer_encoding.encoding(self.abs_representation)
        self.lower_bound=[1, 1, 1, 1] *self.number_of_refactorings
        self.upper_bound= [self.integer_encoding.ROTypeNum,
                           self.integer_encoding.classNum,
                           self.integer_encoding.classNum,
                           self.integer_encoding.N] * self.number_of_refactorings
        self.initial_objectives = Qmood().calculateQmood(self.abs_representation)
        self.tf_idf = TF_IDF()
        self.classes_nameSequence_dict = self.extract_names_sequences()
        self.callGraph=platform.load_call_graph()

    def extract_names_sequences(self):
        name_extractor = NameExtractor()
        names_dict = name_extractor.extract(projectInfo=self.abs_representation)
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
            res += cosine_smiliarity
        if len(decoded_sequences) != 0:
            res = res/len(decoded_sequences)
        return res

    def exec_RO(self, decoded_sequences, projectInfo):
        '''
        perform refactoring operations in decoded_sequences on projectInfo
        return a list recording which refactorings has passed the preconditions and be executed
        '''
        executed = list()
        for each in decoded_sequences:
            executed.append(dispatch(each["ROType"].value)(each, projectInfo))
        return executed

    def calc_quality_gain(self, projectInfo):
        qmood_metrics_list = ["Effectiveness", "Extendibility", "Flexibility", "Functionality", "Resusability",
                              "Understandability"]

        qmood_metrics_value = Qmood().calculateQmood(projectInfo)
        return sum([(qmood_metrics_value[metric] - self.initial_objectives[metric]) for metric in qmood_metrics_list])


    def filter(self, executed:list, decoded_sequences:List[dict])->List[dict]:
        res = list()
        for i, value in enumerate(executed):
            if value:
                res.append(decoded_sequences[i])
        return res

    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        projectInfo = copy.deepcopy(self.abs_representation)
        self.integer_encoding.encoding(projectInfo)

        'Decode and execute'
        decodedIntegerSequences = self.integer_encoding.decoding(solution.variables)

        "Execute corresponding refactoring operations"
        executed = self.exec_RO(decodedIntegerSequences, projectInfo)

        "Filter out RO that hasn't passed preconditions"
        decodedIntegerSequences = self.filter(executed=executed, decoded_sequences=decodedIntegerSequences)


        'calculate Quality Gain after executed refactoring operatins'
        quality_gain = self.calc_quality_gain(projectInfo)

        'calculate QMOOD  after executed refactoring operations'
        solution.objectives[0] = -1 * quality_gain

        'calculate semantic coherence and call relation on refactoring operations applied classes'
        semantic_coherence = self.calc_sematic_coherence(decodedIntegerSequences)

        'calculate call relation'
        call_relation = self.callGraph.calc_call_relation(decodedIntegerSequences)
        solution.objectives[1] = -0.2 * semantic_coherence - 0.8*call_relation

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
        return "Search Refactoring Operation Problem without Review Effort"