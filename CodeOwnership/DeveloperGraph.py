from PullRequestService import PullRequest
from typing import List
from datetime import date

class Developer():
    def __init__(self,name):
        self.name = name
        self.relationships = dict()

    def __hash__(self):
        return self.name


class DeveloperGraph():
    def __init__(self,pull_request_list:List[PullRequest]):
        self.pull_request_list = pull_request_list
        self.LAMBDA = 0.8
        self.CLOSED = 0.5
        self.MERGED = 1
        'a vertive is one Developer'
        self.vertices=dict()
        'manually set baseline & deadline'
        self.baseline = "2011-12-24"
        self.deadline = "2022-12-24"

    def generate_vertices(self):
        for each in self.pull_request_list:
            if each.proposer not in self.vertices.keys():
                self.vertices[each.proposer] = dict()
            for developer in each.commentators:
                if developer not in self.vertices.keys():
                    self.vertices[developer] = dict()
        return self

    def update(self,value:float,vertice1,vertice2):
        if vertice1!=vertice2:
            self.vertices[vertice1][vertice2] = self.vertices[vertice1].get(vertice2, 0) + value
            self.vertices[vertice2][vertice1] = self.vertices[vertice2].get(vertice1, 0) + value

    def build(self):
        for each_pull_request in self.pull_request_list:
            for i in range(len(each_pull_request.commentators)):
                'calcualte edge value'
                if(each_pull_request.proposer == each_pull_request.commentators[i]):
                    pass
                value = self.calculate_edges(i,each_pull_request)
                'update both developer edge value'
                self.update(value,each_pull_request.proposer,each_pull_request.commentators[i])
        'for relationship between authour and him/herself, set the highest value that appears in self.vertices'
        maximum =0
        for each in self.vertices:
            maximum = max(max(self.vertices[each].values()),maximum)
        for each in self.vertices:
            self.vertices[each][each] = maximum

        return self


    def calculate_edges(self,comment_index:int,pull_request:PullRequest):
        time = float((self.transfer_time_format(pull_request.proposed_time) - self.transfer_time_format(self.baseline)).days)/ \
                float((self.transfer_time_format(self.deadline)-self.transfer_time_format(self.baseline)).days)
        return time*pow(self.LAMBDA,comment_index-1)* (self.CLOSED if pull_request.state=="closed" else self.MERGED)

    def transfer_time_format(self,time):
        'input time format is "20xx-xx-xx" and it will be transfered into date()'
        return date(int(time.split("-")[0]), int(time.split("-")[1]), int(time.split("-")[2]))