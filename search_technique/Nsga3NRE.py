# import sys
# sys.path.append("../")
from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII, UniformReferenceDirectionFactory
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import WriteFrontToFileObserver, BasicObserver
from search_technique.SearchTechnique import SearchTechniqueNRE


class Nsga3NRE(SearchTechniqueNRE):
    def __init__(self):
        super(Nsga3NRE, self).__init__()
        self.name = "Nsga3NRE"

    def search(self):
        self.algorithm = NSGAIII(
            problem=self.problem,
            population_size=100,
            reference_directions=UniformReferenceDirectionFactory(2, n_points=91),
            mutation=IntegerPolynomialMutation(probability=0.5),
            crossover=IntegerSBXCrossover(probability=0.9),
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        # self.algorithm.observable.register(observer=WriteFrontToFileObserver(
        #     output_directory=self.output_path + self.repo_name + "/front/" + self.name + "/"))
        self.algorithm.run()
        return self


if __name__ == "__main__":
    nsga3NRE = Nsga3NRE()
    nsga3NRE.load().search().write_result()
