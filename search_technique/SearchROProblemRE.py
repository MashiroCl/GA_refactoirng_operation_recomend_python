import copy
from typing import List
from jmetal.core.solution import IntegerSolution
from code_ownership.CodeOwnership import CodeOwnership
from encoding.IntegerEncoding import IntegerEncoding
from qmood.metricCalculation import init_inline_class_info
from qmood.Qmood import Qmood
from semantic.Vectorize import TF_IDF
from search_technique.enviroment import Platform
from search_technique.SearchROProblem import SearchROProblem, extract_user_defined_classes, \
    extract_class_with_one_child, extract_class_with_one_child_zero_parent_list


class SearchROProblemRE(SearchROProblem):
    """
    Integer encoding problem which
    """
    'static variable, record the call graph'
    call_graph = None

    def __init__(self, abs_representation: List, platform: Platform):
        '''
        set basic parameters and encode current project
        :param abs_representation: project being processed, should be a list of jClass
        should be an entity of class Repository
        '''
        super(SearchROProblemRE, self).__init__(abs_representation, platform)
        "3 objectives: QMOOD-> Quality Gain + commiters relationship + semantic coherence"
        self.number_of_objectives = 3
        "4 variables decide a refactoring operation"
        self.number_of_variables = 4
        # todo: Research on what are constraints for
        "No contraints"
        self.number_of_constraints = 0
        "number of chromosome"
        self.number_of_refactorings = 20

        'Qmood: maximize    code ownership: maximize'
        self.obj_directions = [self.MAXIMIZE,
                               self.MAXIMIZE,
                               self.MAXIMIZE]

        self.obj_labels = ['Quality Gain', 'Relationship Score']
        self.abs_representation = abs_representation
        self.repo_path = platform.repo_path
        self.integerEncoding = IntegerEncoding()
        self.integerEncoding.encoding(self.abs_representation)
        self.lower_bound = [1, 1, 1, 1] * self.number_of_refactorings
        self.upper_bound = [self.integerEncoding.ROTypeNum,
                            self.integerEncoding.classNum,
                            self.integerEncoding.classNum,
                            self.integerEncoding.N] * self.number_of_refactorings
        self.developer_graph = platform.load_developer_graph()
        self.ownership_path = platform.ownership_path
        self.tf_idf = TF_IDF()
        self.classes_nameSequence_dict = self.extract_names_sequences()
        self.call_graph = platform.load_call_graph()

        self.user_defined_classes = extract_user_defined_classes(self.abs_representation)
        self.class_with_one_child_list = extract_class_with_one_child(self.abs_representation)
        self.class_with_one_child_zero_parent_list = extract_class_with_one_child_zero_parent_list(self.abs_representation)
        self.inline_class_info = init_inline_class_info()
        self.initial_objectives = Qmood(self.abs_representation).calculateQmood(self.abs_representation,
                                                                                self.user_defined_classes,
                                                                                self.inline_class_info)

    def calc_relationship(self, decoded_sequencs):
        return CodeOwnership(self.repo_path, self.ownership_path).findAuthorPairList(decoded_sequencs). \
            calculateRelationship(self.developer_graph)

    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        abs_representation = copy.deepcopy(self.abs_representation)

        self.integerEncoding.encoding(abs_representation)
        'Decode and execute'
        decodedIntegerSequences = self.integerEncoding.decoding(solution.variables)

        "Execute corresponding refactoring operations"
        executed = self.exec_RO(decodedIntegerSequences, abs_representation)

        "Filter out RO that hasn't passed preconditions"
        decodedIntegerSequences = self.filter(executed=executed, decoded_sequences=decodedIntegerSequences)

        "Check whether Inline Class will change NOH, ANA, DSC"
        inline_class_info = self.fill_inline_class_info(self.inline_class_info,
                                                        decodedIntegerSequences,
                                                       self.class_with_one_child_list,
                                                        self.class_with_one_child_zero_parent_list)

        quality_gain = self.calc_quality_gain(abs_representation, self.user_defined_classes, inline_class_info)

        'calculate QMOOD  after executed refactoring operations'
        solution.objectives[0] = -1 * quality_gain

        'calculate ownership on refactoring operations applied files'
        relationship = self.calc_relationship(decodedIntegerSequences)
        solution.objectives[1] = -1 * relationship

        'calculate semantic coherence and call relation on refactoring operations applied classes'
        semantic_coherence = self.calc_sematic_coherence(decodedIntegerSequences)

        'calculate call relation'
        call_relation = self.call_graph.calc_call_relation(decodedIntegerSequences)
        solution.objectives[2] = -0.2 * semantic_coherence - 0.8 * call_relation

        return solution

    def get_name(self) -> str:
        return "Search Refactoring Operation Problem with Review Effort"
