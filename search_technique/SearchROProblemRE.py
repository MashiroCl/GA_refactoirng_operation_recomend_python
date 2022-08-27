import copy
from typing import List
from jmetal.core.solution import IntegerSolution
from code_ownership.CodeOwnership import CodeOwnership
from encoding.IntegerEncoding import IntegerEncoding
from qmood.Qmood import Qmood
from semantic.Vectorize import TF_IDF
from search_technique.enviroment import Platform
from search_technique.SearchROProblem import SearchROProblem
from multiprocessing import Process


class SearchROProblemRE(SearchROProblem):
    """
    Integer encoding problem which
    """

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
        # todo: Research on what are contraints for
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
        self.initial_objectives = Qmood().calculateQmood(self.abs_representation)
        self.developer_graph = platform.load_developer_graph()
        self.ownership_path = platform.ownership_path
        self.tf_idf = TF_IDF()
        self.classes_nameSequence_dict = self.extract_names_sequences()
        self.callGraph = platform.load_call_graph()

    def calc_relationship(self, decoded_sequencs):
        return CodeOwnership(self.repo_path, self.ownership_path).findAuthorPairList(decoded_sequencs). \
            calculateRelationship(self.developer_graph)


    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        import time

        projectInfo = copy.deepcopy(self.abs_representation)

        self.integerEncoding.encoding(projectInfo)
        'Decode and execute'
        decodedIntegerSequences = self.integerEncoding.decoding(solution.variables)

        "Execute corresponding refactoring operations"
        executed = self.exec_RO(decodedIntegerSequences, projectInfo)

        "Filter out RO that hasn't passed preconditions"
        decodedIntegerSequences = self.filter(executed=executed, decoded_sequences=decodedIntegerSequences)

        # start = time.time()

        # multi_process_pool = Pool(4)
        # 'calculate Quality Gain after executed refactoring operations'
        # quality_gain_getter = multi_process_pool.apply_async(self.calc_quality_gain,(projectInfo,))
        # relationship_getter = multi_process_pool.apply_async(self.calc_relationship,(decodedIntegerSequences,))
        # semantic_getter = multi_process_pool.apply_async(self.calc_sematic_coherence,(decodedIntegerSequences,))
        # call_getter = multi_process_pool.apply_async(self.callGraph.calc_call_relation, (decodedIntegerSequences,))
        # multi_process_pool.close()
        # multi_process_pool.join()

        quality_gain = self.calc_quality_gain(projectInfo)
        # process = [Process(target=self.calc_quality_gain, args=(projectInfo,)),
        #            Process(target= self.calc_relationship,args = (decodedIntegerSequences,)),
        #            Process(target=self.calc_sematic_coherence, args=(decodedIntegerSequences,)),
        #            Process(target=self.callGraph.calc_call_relation, args=(decodedIntegerSequences,))]
        # [p.start() for p in process]
        # [p.join() for p in process]
        'calculate QMOOD  after executed refactoring operations'
        solution.objectives[0] = -1 * quality_gain

        'calculate ownership on refactoring operations applied files'
        relationship = self.calc_relationship(decodedIntegerSequences)
        solution.objectives[1] = -1 * relationship

        'calculate semantic coherence and call relation on refactoring operations applied classes'
        semantic_coherence = self.calc_sematic_coherence(decodedIntegerSequences)

        'calculate call relation'
        call_relation = self.callGraph.calc_call_relation(decodedIntegerSequences)
        solution.objectives[2] = -0.2 * semantic_coherence - 0.8 * call_relation

        # end = time.time()
        # print(f"{end - start}, calc 3 objectives time")

        return solution

    def get_name(self) -> str:
        return "Search Refactoring Operation Problem with Review Effort"
