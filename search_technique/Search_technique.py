import sys
sys.path.append("../")
from jxplatform2.jClass import jClass
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from utils import readJson


class Search_technique:
    def __init__(self):
        self.problem = None
        self.name = "search_technique"
        self.algorithm = None
        self.outputPath = None

    def load_args(self):
        'Read Jxplatform2 extraction result'
        self.repoName = sys.argv[1]
        self.max_evaluations = sys.argv[2]
        self.platform = sys.argv[3]
        return self.repoName, self.max_evaluations, self.platform

    def exclude_test_class(self, exclude: bool, javaClasses):
        """exclude test_class"""
        res = []
        if exclude:
            for each in javaClasses:
                if not each.testClass:
                    res.append(each)
        else:
            for each in javaClasses:
                res.append(each)
        return res

    def exclude_anonymous_class(self, exclude: bool, javaClasses):
        """ exclude anonymous class"""
        res = []
        if exclude:
            for each in javaClasses:
                if not each.anonymous_class:
                    res.append(each)
        else:
            for each in javaClasses:
                res.append(each)
        return res

    def json_2_jClass(self, jsonList):
        res = []
        for each in jsonList:
            res.append(jClass(each))
        return res

    def load_repository(self, jsonFile: str, exclude_test: bool, exclude_anonymous: bool = False):
        # load repository class info
        load = readJson(jsonFile)
        javaClasses = self.json_2_jClass(load)
        javaClasses = self.exclude_test_class(exclude=exclude_test, javaClasses=javaClasses)
        javaClasses = self.exclude_anonymous_class(exclude=exclude_anonymous, javaClasses=javaClasses)
        return javaClasses

    def load(self):
        pass

    def search(self):
        pass

    def write_result(self):
        front = get_non_dominated_solutions(self.algorithm.get_result())

        # save to files
        print_function_values_to_file(front, self.outputPath + self.repoName +'/FUN.'+self.name)
        print_variables_to_file(front, self.outputPath + self.repoName +'/VAR.'+self.name)

        print('Algorithm (continuous problem): ' + self.algorithm.get_name())
        print('Problem: ' + self.problem.get_name())
        print('Computing time: ' + str(self.algorithm.total_computing_time))