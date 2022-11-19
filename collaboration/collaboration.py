from typing import List

from collaboration.graph import Graph
from collaboration.pullrequest import Pullrequest
import utils.githubapi as api
import utils.csv as csv

REPO_API = "https://api.github.com/repos/"
PULL_REQUEST = "/pulls?state=all&sort=updated&direction=desc&per_page=100&page="


def get_pr_history(repo: str, output: str = "./pullrequest.csv"):
    '''
    use the github api to obtain pullrequests for a repository and write into a csv
    url: url for the repository
    '''
    page_num = 1
    if "https://github.com/" in repo:
        repo = repo.split("https://github.com/")[1]
    with open(output, "a", encoding="utf-8") as f:
        while True:
            response = api.api_request(REPO_API + repo + PULL_REQUEST + str(page_num))
            page_num += 1
            # no pull requests gotten from api
            if len(response.text) <= 2:
                break
            for each in response.json():
                pr = Pullrequest(each)
                pr.get_comments()
                csv.pullrequest2csv([pr], f)


def get_collaboration_score(graph: Graph, collaborators: List[str]):
    if len(collaborators) == 1:
        superowner = collaborators[0]
        return graph.vertices[superowner][superowner]
    score = 0
    while len(collaborators):
        cur_co = collaborators[0]
        for i in range(1,len(collaborators)):
            if cur_co in graph.vertices.keys():
                score += graph.vertices[cur_co].get(collaborators[i],0)
        collaborators.pop(0)
    return score