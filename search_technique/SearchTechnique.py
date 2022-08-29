import sys

sys.path.append("../")
from jxplatform2.jClass import jClass
from search_technique.SearchROProblemRE import SearchROProblemRE
from search_technique.SearchROProblemNRE import SearchROProblemNRE
from search_technique.enviroment.Platform import *
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from utils import readJson


class SearchTechnique:
    def __init__(self):
        self.problem = None
        self.name = "search_technique"
        self.algorithm = None
        self.output_path = None
        self.repo_name = ""
        self.max_evaluations = ""
        self.platform = ""

    def select_platform(self, repo_name, platform) -> Platform:
        '''
        select to run on local "local"  or on server "titan"
        '''
        p = Platform()
        if platform == "local":
            p = LocalPlatform()
        if platform == "titan":
            p = TitanPlatform()
        p.set_repository(repo_name)
        return p

    def load_args(self):
        'Read Jxplatform2 extraction result'
        self.repo_name = sys.argv[1]
        self.max_evaluations = sys.argv[2]
        self.platform = sys.argv[3]
        return self.repo_name, self.max_evaluations, self.platform

    def exclude_test_class(self, exclude: bool, java_classes):
        """exclude test_class"""
        res = []
        if exclude:
            for each in java_classes:
                if not each.testClass:
                    res.append(each)
        else:
            for each in java_classes:
                res.append(each)
        return res

    def exclude_anonymous_class(self, exclude: bool, java_classes):
        """ exclude anonymous class"""
        res = []
        if exclude:
            for each in java_classes:
                if not each.anonymous_class:
                    res.append(each)
        else:
            for each in java_classes:
                res.append(each)
        return res

    def json_2_jClass(self, json_list):
        res = []
        for each in json_list:
            res.append(jClass(each))
        return res

    def load_repository(self, json_file: str, exclude_test: bool, exclude_anonymous: bool = False):
        # load repository class info
        load = readJson(json_file)
        java_classes = self.json_2_jClass(load)
        java_classes = self.exclude_test_class(exclude=exclude_test, java_classes=java_classes)
        java_classes = self.exclude_anonymous_class(exclude=exclude_anonymous, java_classes=java_classes)
        return java_classes

    def load(self):
        pass

    def search(self):
        pass

    def write_result(self):
        front = get_non_dominated_solutions(self.algorithm.get_result())

        # save to files
        print_function_values_to_file(front, self.output_path + self.repo_name + '/FUN.' + self.name)
        print_variables_to_file(front, self.output_path + self.repo_name + '/VAR.' + self.name)

        print('Algorithm (continuous problem): ' + self.algorithm.get_name())
        print('Problem: ' + self.problem.get_name())
        print('Computing time: ' + str(self.algorithm.total_computing_time))


class SearchTechniqueRE(SearchTechnique):
    def load(self):
        self.repo_name, self.max_evaluations, self.platform = self.load_args()
        selected_platform = self.select_platform(self.repo_name, self.platform)
        self.output_path = selected_platform.output_path

        abs_representation = self.load_repository(json_file=selected_platform.json_file_path,
                                                  exclude_test=True, exclude_anonymous=True)

        self.problem = SearchROProblemRE(abs_representation, selected_platform)
        return self


class SearchTechniqueNRE(SearchTechnique):
    def load(self):
        self.repo_name, self.max_evaluations, self.platform = self.load_args()
        selected_platform = self.select_platform(self.repo_name, self.platform)
        self.output_path = selected_platform.output_path

        abs_representation = self.load_repository(json_file=selected_platform.json_file_path,
                                                  exclude_test=True, exclude_anonymous=True)
        self.problem = SearchROProblemNRE(abs_representation, selected_platform)
        return self
