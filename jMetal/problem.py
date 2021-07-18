from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution
from RefactoringOperation import Solution, MoveMethod
from Qmood import Qmood
import random

#a binary array representing whethever the ith element of one RO is selected or not?
class FindOperations(BinaryProblem):
    def __init__(self,Qmood:float,s:Solution,jClist:list):
        super(FindOperations,self).__init__()
        'solution which contains method dictionary and class dictionary'
        self.s=s
        self.jClist=jClist
        self.Qmood=Qmood
        'Length of each refactoring operation'
        self.number_of_bits=self.s.len
        '7 objectives: Qmood, code ownership'
        #todo firstly only Qmood
        self.number_of_objectives=6
        'Length of refactoring operation sequence (This should be difference according to the  scale of the rpository)'
        # self.number_of_variables=3
        self.number_of_variables=1
        self.number_of_constraints=0

        'Qmood: maximize    code ownership: maximize'
        #todo Qmood should be 6 metrics or not?
        # Firstly use it as 6 consider the code ownership
        self.obj_directions=[self.MAXIMIZE,self.MAXIMIZE,self.MAXIMIZE,self.MAXIMIZE,self.MAXIMIZE,self.MAXIMIZE]
        self.obj_labels=['Effectiveness','Extendibility','Flexibility','Functionality','Resusability','Understandability']

        'encoding'
        self.s.binaryEncoding(self.jClist)

    def boolTo01(self,l):
        s=[]
        for each in l:
            if each == False:
                s.append(0)
            elif each == True:
                s.append(1)
        return s

    def executeSolutions(self,solutions):
        #todo number of variables will be changed
        for each in solutions:
            #todo execute RO, considering different type of RO
            oneSolution="".join(str(x) for x in (self.boolTo01(each)))

            #todo other type of refactoring operations
            #if one Solution is MoveMethod:
            print("oneSolution",oneSolution)
            result=self.s.binaryDecoding(oneSolution)
            mm=MoveMethod(result[0],result[1],result[2])
            mm.execute()



    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        '''
        :param solution:
        :return:
        '''
        'Execute refactoring operations'
        print("Execute solutions")
        print(solution)
        self.executeSolutions(solution.variables)

        'Calculate qmood on the whole projects'
        qmood=Qmood()
        #todo it should be the average value of all classes
        qmood.calculateQmood(self.jClist)
        effectiveness=qmood.getEffectiveness()
        extendibility=qmood.getExtendibility()
        flexibility=qmood.getFlexibility()
        functionality=qmood.getFunctionality()
        resusability=qmood.getResusability()
        understandability=qmood.getUnderstandability()

        solution.objectives[0] = -1.0 * effectiveness
        solution.objectives[1] = -1.0 * extendibility
        solution.objectives[2] = -1.0 * flexibility
        solution.objectives[3] = -1.0 * functionality
        solution.objectives[4] = -1.0 * resusability
        solution.objectives[5] = -1.0 * understandability


        'Calculate code ownership'
        #todo how to calculate, in which form
        ownership=0


        # solution.objectives[6]=-1.0*ownership
        return solution

    def create_solution(self) -> BinarySolution:
        print("create solution")
        new_solution=BinarySolution(number_of_variables=self.number_of_variables,
                                    number_of_objectives=self.number_of_objectives)
        #todo invalid value should be considered in the random part

        new_solution.variables[0] = \
            [True if random.randint(0, 1) == 0 else False for _ in range(self.number_of_bits)]

        print(new_solution)
        return new_solution
    def get_name(self) -> str:
      return 'Find Operations'