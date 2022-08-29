import random
from typing import List
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from qmood.Qmood import Qmood
from refactoring_operation.RefactoringOperationDispatcher import dispatch
from refactoring_operation.RefactoringOperationEnum import RefactoringOperationEnum
from semantic.NameExtractor import NameExtractor
from search_technique.enviroment import Platform


class SearchROProblem(IntegerProblem):
    """
    Integer encoding problem which
    """

    def __init__(self, abs_representation: List, platform: Platform):
        '''
        set basic parameters and encode current project
        :param abs_representation: project being processed, should be a list of jClass
        should be an entity of class Repository
        '''
        super(SearchROProblem, self).__init__()
        pass

    def extract_names_sequences(self):
        name_extractor = NameExtractor()
        names_dict = name_extractor.extract(abs_representation=self.abs_representation)
        sequence_dict = name_extractor.dict_names_to_dict_sequence(names_dict)
        return sequence_dict

    def vectorize_classes(self, classes):
        res = list()
        for each in classes:
            res.append(self.classes_nameSequence_dict[each.getKey()])
        return self.tf_idf.vectorize(res)

    def calc_cosine_similarity(self, doc_metric):
        return self.tf_idf.cosine_similarity(doc_metric)

    def calc_sematic_coherence(self, decoded_sequences):
        res = 0
        for each in decoded_sequences:
            X = self.vectorize_classes([each["class1"], each["class2"]])
            cosine_smiliarity = self.calc_cosine_similarity(X).tolist()[1]
            res += cosine_smiliarity
        if len(decoded_sequences) != 0:
            res = res / len(decoded_sequences)
        return res

    def exec_RO(self, decoded_sequences, abs_representation):
        '''
        perform refactoring operations in decoded_sequences on projectInfo
        return a list recording which refactorings has passed the preconditions and be executed
        '''
        executed = list()
        for each in decoded_sequences:
            executed.append(dispatch(each["ROType"].value)(each, abs_representation))
        return executed

    def calc_quality_gain(self, abs_representation, user_defined_classes, inline_class_info):
        qmood_metrics_list = ["Effectiveness", "Extendibility", "Flexibility", "Functionality", "Resusability",
                              "Understandability"]

        qmood_metrics_value = Qmood(abs_representation).calculateQmood(abs_representation, user_defined_classes, inline_class_info)
        return sum([(qmood_metrics_value[metric] - self.initial_objectives[metric]) for metric in qmood_metrics_list])

    def filter(self, executed: list, decoded_sequences: List[dict]) -> List[dict]:
        res = list()
        for i, value in enumerate(executed):
            if value:
                res.append(decoded_sequences[i])
        return res

    def fill_inline_class_info(self, inline_class_info, decoded_sequences,
                               class_with_one_child_list, class_with_one_child_zero_parent_list):
        for each in decoded_sequences:
            if each["ROType"] == RefactoringOperationEnum.INLINECLASS:
                inline_class_info["DSC"] = inline_class_info.get("DSC", 0) - 1
                if len(each["class1"].getSuperClass())>0:
                    'index 0 is modifier+#+classname e.g.1034#BaseListener '
                    if each["class1"].getSuperClass()[0] in class_with_one_child_list:
                        inline_class_info["ANA"] = inline_class_info.get("ANA", 0)-1
                    if each["class1"].getSuperClass()[0] in class_with_one_child_zero_parent_list:
                        inline_class_info["NOH"] = inline_class_info.get("ANA", 0)-1
        return inline_class_info

    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        pass

    def create_solution(self) -> IntegerSolution:
        newSolution = IntegerSolution(lower_bound=self.lower_bound,
                                      upper_bound=self.upper_bound,
                                      number_of_objectives=self.number_of_objectives,
                                      number_of_constraints=self.number_of_constraints)
        newSolution.variables = \
            [int(random.uniform(self.lower_bound[i] * 1.0, self.upper_bound[i] * 1.0))
             for i in range(self.number_of_variables * self.number_of_refactorings)]
        return newSolution

    def get_name(self) -> str:
        return "Search Refactoring Operation Problem"


def extract_user_defined_classes(java_classes):
    res = []
    for each in java_classes:
        res.append(each.getPackage() + "." + each.getClassName())
    return res


def extract_class_with_one_child(java_classes)->List:
    res = []
    for each in java_classes:
        if len(each.getChildren())==1:
            res.append(each.getClass())
    return res


def extract_class_with_one_child_zero_parent_list(java_classes)->List:
    res = []
    for each in java_classes:
        if len(each.getChildren())==1 and len(each.getSuperClass())==0:
            res.append(each.getClass())
    return res
