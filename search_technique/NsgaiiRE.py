import sys
sys.path.append("../")
from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import WriteFrontToFileObserver, BasicObserver
from search_technique.SearchTechnique import SearchTechniqueRE


class NsgaiiRE(SearchTechniqueRE):
    def __init__(self):
        super(NsgaiiRE, self).__init__()
        self.name = "NsgaiiRE"

    def search(self):
        self.algorithm = NSGAII(
            problem=self.problem,
            population_size=100,
            offspring_population_size=100,
            mutation=IntegerPolynomialMutation(probability=0.5),
            crossover=IntegerSBXCrossover(probability=1),
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.observable.register(observer=WriteFrontToFileObserver(
            output_directory=self.output_path + self.repo_name + "/front/" + self.name + "/"))
        self.algorithm.run()
        return self


if __name__ == "__main__":
    nsgaiiRE = NsgaiiRE()
    nsgaiiRE.load().search().write_result()
