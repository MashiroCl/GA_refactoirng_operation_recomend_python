import unittest
from call_graph.CallGraph import CallGraph

class CallGraphTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CallGraphTest, self).__init__( *args, **kwargs)


    def test_CallGraph(self):
        repo = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCoRE/csv/call.json"
        callgraph = CallGraph(repo, "mbassador")
        # print(callgraph.callgraph)
        print(callgraph.callgraph["src/main/java/net/engio/mbassy/bus/config/IBusConfiguration.java"]["fieldAccessIn"])


    def test_count_share_normal(self):
        lista=[2,3]
        listb=[2,2,6]
        actual = CallGraph.count_share(lista,listb)
        self.assertEqual(actual, 3/5)

    def test_count_share_all_same(self):
        lista=[2]
        listb=[2,2,2]
        actual = CallGraph.count_share(lista,listb)
        self.assertEqual(actual, 1)

    def test_count_share_all_difference(self):
        lista=[2, 2]
        listb=[3, 4, 5]
        actual = CallGraph.count_share(lista,listb)
        self.assertEqual(actual, 0)

    def test_shared_call_out(self):
        repo = "/Users/leichen/Desktop/Student/call.json"
        callgraph = CallGraph(repo, "Student")
        print(callgraph.callgraph)
        class1 = "Teacher.java"
        class2 = "SchoolDay.java"
        actual = callgraph.shared_call_out(class1, class2)
        self.assertEqual(1,actual)

    def test_shared_call_in(self):
        repo = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/call.json"
        callgraph = CallGraph(repo, "mbassador")
        class1 = "src/main/java/net/engio/mbassy/bus/config/IBusConfiguration.java"
        class2 = "src/main/java/net/engio/mbassy/bus/BusRuntime.java"
        actual = callgraph.shared_call_in(class1, class2)
        self.assertEqual(0.1891891891891892,actual)

    def test_check(self):
        repo = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/call.json"
        callgraph = CallGraph(repo, "mbassador")
        for each in callgraph.callgraph:
            print(each)
            print(callgraph.callgraph[each])


    def test_shared_call_out_key_not_exist(self):
        repo = "/Users/leichen/Desktop/Student/call.json"
        callgraph = CallGraph(repo, "Student")
        print(callgraph.callgraph)
        class1 = "NotExist.java"
        class2 = "SchoolDay.java"
        actual = callgraph.shared_call_out(class1, class2)
        self.assertEqual(0,actual)

    def test_shared_call_in_all_different(self):
        repo = "/Users/leichen/Desktop/Student/call.json"
        callgraph = CallGraph(repo, "Student")
        print(callgraph.callgraph)
        class1 = "People.java"
        class2 = "Student.java"
        actual = callgraph.shared_call_in(class1, class2)
        self.assertEqual(0,actual)


    def test_call_relation(self):
        repo = "/Users/leichen/Desktop/Student/call.json"
        callgraph = CallGraph(repo, "Student")
        class1 = "Teacher.java"
        class2 = "SchoolDay.java"
        actual = callgraph.call_relation(class1, class2)
        self.assertEqual(0.4, actual)


    def test_test(self):
        candidates = [[3,2,0],[2,2,1],[1,2,2]]
        candidates.sort(key=lambda x: x[2])
        print(candidates)
