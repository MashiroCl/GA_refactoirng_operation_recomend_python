from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.algorithm.multiobjective.spea2 import SPEA2
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import WriteFrontToFileObserver, BasicObserver
from search_technique.SearchTechnique import SearchTechniqueRE


class SPEA2RE(SearchTechniqueRE):
    def __init__(self):
        super(SPEA2RE, self).__init__()
        self.name = "SPEA2RE"

    def search(self):
        self.algorithm = SPEA2(
            problem=self.problem,
            population_size=100,
            offspring_population_size=100,
            mutation=IntegerPolynomialMutation(probability=0.5),
            crossover=IntegerSBXCrossover(probability=0.9),
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.run()
        return self