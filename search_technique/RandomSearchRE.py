from jmetal.util.observer import BasicObserver, WriteFrontToFileObserver
from jmetal.util.termination_criterion import StoppingByEvaluations
from SearchTechnique import SearchTechniqueRE
from jmetal.algorithm.multiobjective import RandomSearch


class RandomSearchRE(SearchTechniqueRE):
    '''
    Simple random search with review effort
    Simple random search: call create_solution() to randomly create a new solution in each iteration,
                          if the new soulution is a non-dominated one, it will be recorded in FUN.xx
    '''
    def __init__(self):
        super(RandomSearchRE, self).__init__()
        self.name = "RandomSearchRE"

    def search(self):
        self.algorithm = RandomSearch(
            problem=self.problem,
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.observable.register(observer=WriteFrontToFileObserver(
            output_directory=self.output_path + self.repo_name + "/front/" + self.name + "/"))
        self.algorithm.run()
        return self

if __name__ =="__main__":
    randomSearchRE = RandomSearchRE()
    randomSearchRE.load().search().write_result()
