import json

class CallGraph:
    def __init__(self, repoPath:str):
        self.repo = repoPath
        with open(self.repo) as f:
            self.json = json.load(f)
        self.callgraph = dict()
        self._build_call_graph()

    def _build_call_graph(self):
        for each in self.json:
            self.callgraph[each["class"]] = {"fieldAccessIn":each["fieldAccessIn"],
                                             "fieldAccessOut":each["fieldAccessOut"],
                                             "methodCallIn": each["methodCallIn"],
                                             "methodCallOut":each["methodCallOut"]}
    @staticmethod
    def count_share(lista, listb):
        total = dict()
        share = 0
        for each in lista:
            total[each]= total.get(each,0)+1
        for each in listb:
            total[each]= total.get(each,0)+1
        for each in total:
            if each in lista and each in listb and total[each]>1:
                share += total[each]
        total_len = len(lista)+len(listb)
        if total_len==0:
            total_len=1
        return share/total_len

    def shared_call_out(self, class1, class2):
        '''
        calculae shared-method call out between class1 and class2

        '''
        mco1 = self.callgraph[class1]["methodCallOut"]
        mco2 = self.callgraph[class2]["methodCallOut"]
        return CallGraph.count_share(mco1, mco2)

    def shared_call_in(self, class1, class2):
        '''
        calculae shared-method call out between class1 and class2

        '''
        mco1 = self.callgraph[class1]["methodCallIn"]
        mco2 = self.callgraph[class2]["methodCallIn"]
        return CallGraph.count_share(mco1, mco2)

    def shared_field_in(self, class1, class2):
        '''
        calculae shared-method call out between class1 and class2

        '''
        mco1 = self.callgraph[class1]["fieldAccessIn"]
        mco2 = self.callgraph[class2]["fieldAccessIn"]
        return CallGraph.count_share(mco1, mco2)

    def shared_field_in(self, class1, class2):
        '''
        calculae shared-method call out between class1 and class2

        '''
        mco1 = self.callgraph[class1]["fieldAccessOut"]
        mco2 = self.callgraph[class2]["fieldAccessOut"]
        return CallGraph.count_share(mco1, mco2)