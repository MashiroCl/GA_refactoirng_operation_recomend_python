import csv
from typing import List
from datetime import date

LAMBDA = 0.8

exclude_name_list = {"dependabot[bot]"}


def status_coefficient(status):
    if status == "merged":
        return 1
    if status == "open" or status == "closed":
        return 0.5


class Graph:
    '''
    {dev1: {dev2: 1.0, dev3: 2.0}, dev2{dev1: 1.0} ...}
    '''

    def __init__(self):
        self.vertices = dict()
        self.baseline = date(2008, 12, 24)
        self.deadline = date(2022, 12, 24)

    def build_from_csv(self, pr_csv: str):
        def create_dict(s: str):
            if s not in self.vertices.keys():
                self.vertices[s] = dict()

        self_collaboration_score = 0
        with open(pr_csv) as f:
            reader = csv.reader(f)
            # each pull request
            for row in reader:
                proposer = row[2]
                if proposer in exclude_name_list:
                    continue
                comments = row[3:]  # [comment1,comment1_time,comment2,comment2_time]
                create_dict(proposer)
                # each commenter and comment with proposer
                for i in range(0, len(comments), 2):
                    commenter = comments[i]
                    # skip if the proposer and commenter is the same or commenter should be excluded
                    if proposer == commenter or commenter in exclude_name_list:
                        continue
                    create_dict(commenter)
                    edge_weight = self.calc_edge(i, comments)
                    # consider pull request status
                    edge_weight = edge_weight * status_coefficient(row[1].strip())
                    self.update(proposer, commenter, edge_weight)
                    self_collaboration_score = max(self.vertices[proposer][commenter], self_collaboration_score)
            # set the collaboration score for each proposer and him/herself as the maximum collaboration score which
            # ever exists in the repository
            for proposer in self.vertices.keys():
                self.vertices[proposer][proposer] = self_collaboration_score
        return self.vertices

    def calc_edge(self, index: int, comments: List[str]):
        def to_date(t: str):  # turn 2020-12-24 to date(2020,12,24) to calculate days number
            t = t.split("-")
            return date(int(t[0]), int(t[1]), int(t[2]))

        time_factor = (to_date(comments[index + 1]) - self.baseline) / (self.deadline - self.baseline)
        return LAMBDA ** index * time_factor

    def update(self, proposer: str, commenter: str, edge_weight: float):
        pd = self.vertices[proposer]
        cd = self.vertices[commenter]
        pd[commenter] = pd.get(commenter, 0) + edge_weight
        cd[proposer] = cd.get(proposer, 0) + edge_weight
