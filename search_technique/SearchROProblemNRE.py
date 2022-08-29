import copy
from jmetal.core.solution import IntegerSolution
from encoding.IntegerEncoding import IntegerEncoding
from qmood.metricCalculation import init_inline_class_info
from qmood.Qmood import Qmood
from semantic.Vectorize import TF_IDF
from search_technique.enviroment import Platform
from search_technique.SearchROProblem import SearchROProblem, extract_user_defined_classes, \
    extract_class_with_one_child, extract_class_with_one_child_zero_parent_list

class SearchROProblemNRE(SearchROProblem):
    """
    Integer encoding problem which
    """
    def __init__(self, abs_representation, platform: Platform):
        '''
        set basic parameters and encode current project
        :param abs_representation: project being processed, should be a list of jClass
        should be an entity of class Repository
        '''
        super(SearchROProblemNRE, self).__init__(abs_representation, platform)
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
        self.tf_idf = TF_IDF()
        self.classes_nameSequence_dict = self.extract_names_sequences()
        self.callGraph=platform.load_call_graph()

        self.user_defined_classes = extract_user_defined_classes(self.abs_representation)
        self.class_with_one_child_list = extract_class_with_one_child(self.abs_representation)
        self.class_with_one_child_zero_parent_list = extract_class_with_one_child_zero_parent_list(self.abs_representation)
        self.inline_class_info = init_inline_class_info()
        self.initial_objectives = Qmood(self.abs_representation).calculateQmood(self.abs_representation,
                                                                                self.user_defined_classes,
                                                                                self.inline_class_info)



    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        abs_representation = copy.deepcopy(self.abs_representation)
        self.integer_encoding.encoding(abs_representation)

        'Decode and execute'
        decodedIntegerSequences = self.integer_encoding.decoding(solution.variables)

        "Execute corresponding refactoring operations"
        executed = self.exec_RO(decodedIntegerSequences, abs_representation)

        "Filter out RO that hasn't passed preconditions"
        decodedIntegerSequences = self.filter(executed=executed, decoded_sequences=decodedIntegerSequences)

        "Check whether Inline Class will change NOH, ANA, DSC"
        inline_class_info = self.fill_inline_class_info(self.inline_class_info,
                                                        decodedIntegerSequences,
                                                       self.class_with_one_child_list,
                                                        self.class_with_one_child_zero_parent_list)

        'calculate Quality Gain after executed refactoring operatins'
        quality_gain = self.calc_quality_gain(abs_representation, self.user_defined_classes, inline_class_info)

        'calculate QMOOD  after executed refactoring operations'
        solution.objectives[0] = -1 * quality_gain

        'calculate semantic coherence and call relation on refactoring operations applied classes'
        semantic_coherence = self.calc_sematic_coherence(decodedIntegerSequences)

        'calculate call relation'
        call_relation = self.callGraph.calc_call_relation(decodedIntegerSequences)
        solution.objectives[1] = -0.2 * semantic_coherence - 0.8*call_relation

        return solution

    def get_name(self) -> str:
        return "Search Refactoring Operation Problem without Review Effort"