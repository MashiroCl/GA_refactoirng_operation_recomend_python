from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.algorithm.multiobjective.ibea import IBEA
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import BasicObserver
from search_technique.SearchTechnique import SearchTechniqueNRE


class IBEANRE(SearchTechniqueNRE):
    def __init__(self):
        super(IBEANRE, self).__init__()
        self.name = "IBEANRE"

    def search(self):
        self.algorithm = IBEA(
            problem=self.problem,
            kappa=1,
            population_size=100,
            offspring_population_size=100,
            mutation=IntegerPolynomialMutation(probability=0.5),
            crossover=IntegerSBXCrossover(probability=0.9),
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.run()
        return self