import json


class CallGraph:
    def __init__(self, repoPath: str):
        self.repo = repoPath
        with open(self.repo) as f:
            self.json = json.load(f)
        self.callgraph = dict()
        self._build_call_graph()

    def _build_call_graph(self):
        for each in self.json:
            self.callgraph[each["class"]] = {"fieldAccessIn": each["fieldAccessIn"],
                                             "fieldAccessOut": each["fieldAccessOut"],
                                             "methodCallIn": each["methodCallIn"],
                                             "methodCallOut": each["methodCallOut"]}

    @staticmethod
    def count_share(lista, listb):
        total = dict()
        share = 0
        if lista == None:
            lista = []
        if listb == None:
            listb = []
        for each in lista:
            total[each] = total.get(each, 0) + 1
        for each in listb:
            total[each] = total.get(each, 0) + 1
        for each in total:
            if each in lista and each in listb and total[each] > 1:
                share += total[each]
        total_len = len(lista) + len(listb)
        if total_len == 0:
            total_len = 1
        return share / total_len

    def obtain_callees(self, class1, type):
        callee_list = self.callgraph.get(class1, list())
        if len(callee_list)==0:
            return callee_list
        return callee_list[type]

    def shared_call_out(self, class1, class2):
        '''
        calculae shared-method call out between class1 and class2

        '''
        mco1 = self.obtain_callees(class1, "methodCallOut")
        mco2 = self.obtain_callees(class2, "methodCallOut")
        return CallGraph.count_share(mco1, mco2)

    def shared_call_in(self, class1, class2):
        '''
        calculae shared-method call out between class1 and class2

        '''
        mco1 = self.obtain_callees(class1, "methodCallIn")
        mco2 = self.obtain_callees(class2, "methodCallIn")
        return CallGraph.count_share(mco1, mco2)

    def shared_field_in(self, class1, class2):
        '''
        calculae shared-method call out between class1 and class2

        '''
        mco1 = self.obtain_callees(class1, "fieldAccessIn")
        mco2 = self.obtain_callees(class2, "fieldAccessIn")
        return CallGraph.count_share(mco1, mco2)

    def shared_field_out(self, class1, class2):
        '''
        calculae shared-method call out between class1 and class2

        '''
        mco1 = self.obtain_callees(class1, "fieldAccessOut")
        mco2 = self.obtain_callees(class2, "fieldAccessOut")
        return CallGraph.count_share(mco1, mco2)

    def call_relation(self, class1, class2):
        '''
        call_relation = 0.1* field_access_in+0.1* field_access_out+0.4*method_call_in+0.4*method_call_out
        '''
        return 0.1 * self.shared_field_in(class1, class2) \
               + 0.1 * self.shared_field_out(class1, class2) \
               + 0.4 * self.shared_call_out(class1, class2) \
               + 0.4 * self.shared_call_in(class1, class2)

    def calc_call_relation(self, decoded_sequences):
        res = 0
        for each in decoded_sequences:
            res += self.call_relation(each["class1"].getRelativeFilePath(), each["class1"].getRelativeFilePath())
        'normalize'
        if len(decoded_sequences)!=0:
            res = res/len(decoded_sequences)
        return res
