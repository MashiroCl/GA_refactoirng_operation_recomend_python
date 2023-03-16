from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.algorithm.multiobjective.mocell import MOCell
from jmetal.util.archive import CrowdingDistanceArchive
from jmetal.util.neighborhood import C9
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import BasicObserver
from search_technique.SearchTechnique import SearchTechniqueNRE


class MOCellNRE(SearchTechniqueNRE):
    def __init__(self):
        super(MOCellNRE, self).__init__()
        self.name = "MOCellNRE"

    def search(self):
        self.algorithm = MOCell(
            problem=self.problem,
            population_size=100,
            neighborhood=C9(10, 10),
            archive=CrowdingDistanceArchive(100),
            mutation=IntegerPolynomialMutation(probability=0.5),
            crossover=IntegerSBXCrossover(probability=0.9),
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.run()
        return self