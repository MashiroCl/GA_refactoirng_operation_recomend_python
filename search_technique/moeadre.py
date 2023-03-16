from jmetal.operator import PolynomialMutation, DifferentialEvolutionCrossover
from jmetal.util.aggregative_function import Tschebycheff
from jmetal.algorithm.multiobjective.moead import MOEAD
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import BasicObserver
from search_technique.SearchTechnique import SearchTechniqueRE


class MOEADRE(SearchTechniqueRE):
    def __init__(self):
        super(MOEADRE, self).__init__()
        self.name = "MOEADRE"

    def search(self):
        self.algorithm = MOEAD(
            problem=self.problem,
            population_size=300,
            crossover=DifferentialEvolutionCrossover(CR=1.0, F=0.5, K=0.5),
            mutation=PolynomialMutation(0.5),
            aggregative_function=Tschebycheff(dimension=self.problem.number_of_objectives),
            neighbor_size=20,
            neighbourhood_selection_probability=0.9,
            max_number_of_replaced_solutions=2,
            weight_files_path='search_technique/',
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )

        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.run()
        return self
