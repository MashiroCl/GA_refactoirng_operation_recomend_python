import unittest
from call_graph.CallGraph import CallGraph

class CallGraphTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CallGraphTest, self).__init__( *args, **kwargs)


    def test_CallGraph(self):
        repo = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/callgraph.json"
        callgraph = CallGraph(repo)
        # print(callgraph.callgraph)
        print(callgraph.callgraph["test/java/net/engio/mbassy/StrongConcurrentSetTest.java"]["fieldAccessIn"])


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
        repo = "/Users/leichen/Desktop/student.json"
        callgraph = CallGraph(repo)
        print(callgraph.callgraph)
        class1 = "Teacher.java"
        class2 = "SchoolDay.java"
        actual = callgraph.shared_call_out(class1, class2)
        self.assertEqual(1,actual)

    def test_check(self):
        repo = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/callgraph.json"
        callgraph = CallGraph(repo)
        print(callgraph.callgraph)

    def test_shared_call_out_key_not_exist(self):
        repo = "/Users/leichen/Desktop/student.json"
        callgraph = CallGraph(repo)
        print(callgraph.callgraph)
        class1 = "NotExist.java"
        class2 = "SchoolDay.java"
        actual = callgraph.shared_call_out(class1, class2)
        self.assertEqual(0,actual)

    def test_shared_call_in_all_different(self):
        repo = "/Users/leichen/Desktop/student.json"
        callgraph = CallGraph(repo)
        print(callgraph.callgraph)
        class1 = "People.java"
        class2 = "Student.java"
        actual = callgraph.shared_call_in(class1, class2)
        self.assertEqual(0,actual)


    def test_call_relation(self):
        repo = "/Users/leichen/Desktop/student.json"
        callgraph = CallGraph(repo)
        print(callgraph.callgraph)
        class1 = "Teacher.java"
        class2 = "SchoolDay.java"
        actual = callgraph.call_relation(class1, class2)
        self.assertEqual(0.4, actual)


    def test_test(self):
        a={1:{1:1, 2:2},2:{2:2, 3:3}}
        try:
            print(a.get(3,0).get(1,0))
        except:
            a= None