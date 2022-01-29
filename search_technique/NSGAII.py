from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import BitFlipMutation,SPXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from utils import readJson
from jxplatform2.jClass import jClass
from SearchROProblemBinary import SearchROProblemBinary
from jmetal.lab.visualization import Plot,InteractivePlot


'Read Jxplatform2 extraction result'
jsonFile = "/Users/leichen/Desktop/jedis.json"
repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/jedis"
load = readJson(jsonFile)
jClist = []
for each in load:
    jClist.append(jClass(load=each))

problem=SearchROProblemBinary(jClist,repoPath)


algorithm = NSGAII(
    problem=problem,
    population_size=100,
    offspring_population_size=80,
    mutation=BitFlipMutation(probability=1.0 / problem.number_of_variables),
    # mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
    # crossover=SBXCrossover(probability=1.0, distribution_index=20),
    crossover=SPXCrossover(probability=1.0),
    termination_criterion=StoppingByEvaluations(max_evaluations=10)
)

algorithm.run()

# front = get_non_dominated_solutions(algorithm.get_result())

front = problem.reference_front
for eachSolution in front:
    print(eachSolution.objectives)
plot_front = Plot(title='Pareto front approximation', axis_labels=['1', '2','3','4','5','6','7','8'])
plot_front.plot(front, label='NSGAII', filename=algorithm.get_name())

# plot_front = InteractivePlot(title='Pareto front approximation. Problem: ' + problem.get_name(), reference_front=problem.reference_front, axis_labels=problem.obj_labels)
# plot_front.plot(front, label=algorithm.label, filename="Interactive.eps")


# save to files
print_function_values_to_file(front, 'FUN.NSGAII.SubsetSum')
print_variables_to_file(front, 'VAR.NSGAII.SubsetSum')