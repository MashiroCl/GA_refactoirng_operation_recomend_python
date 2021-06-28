from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution
from Qmood import Qmood
import random
from jClass import jClass

#a binary array representing whethever the ith element of one RO is selected or not?
class FindOperations(BinaryProblem):
    def __init__(self,Qmood:float,RO:list,jCL:list):
        super(FindOperations,self).__init__()
        self.RO=RO

        'Length of each refactoring operation'
        self.number_of_bits=len(self.RO[0])
        '2 objectives: Qmood, code ownership'
        self.number_of_objectives=2
        'Total number of all possible refactoirng operations'
        self.number_of_variables=len(self.RO)
        self.number_of_constraints=0

        'Qmood: maximize    code ownership: maximize'
        #todo Qmood should be 6 metrics or not?
        self.obj_directions=[self.MAXIMIZE,self.MAXIMIZE]
        self.obj_labels=['Qmood','CodeOwnership']

    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        '''
        :param solution:
        :return:
        '''
        'Execute refactoring operations'
        executeRO()
        'Calculate qmood on the whole projects'
        qmood=Qmood()
        extendibility=qmood.getExtendibility()
        effectiveness=qmood.getEffectiveness()
        resusability=qmood.getResusability()
        understandability=qmood.getUnderstandability()
        flexibility=qmood.getFlexibility()
        functionality=qmood.getFunctionality()

        solution.objectives[0]=-1.0*qmoodValue

        'Calculate code ownership'
        #todo how to calculate, in which form
        ownership=0


        solution.objectives[1]=-1.0*ownership

    def create_solution(self) -> BinarySolution:
        new_solution=BinarySolution(number_of_variables=self.number_of_variables,
                                    number_of_objectives=self.number_of_objectives)
        #todo invalid value should be considered in the random part
        new_solution.variables[0]=\
        [True if random.randint(0, 1) == 0 else False for _ in range(self.number_of_bits)]

        return new_solution
