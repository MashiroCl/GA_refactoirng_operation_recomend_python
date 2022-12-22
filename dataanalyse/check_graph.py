from collaboration.collaboration import get_collaboration_score
from collaboration.graph import Graph
from rq2_2 import build_comment_network



def collaboration_count(pullrequest_csv_p):
    with open(pullrequest_csv_p) as f:
        data = f.readlines()
    count = 0
    # print(data[0])
    for each in data:
        if "tyronen" in each:
            count+=1
    print(count)


def collaboration_contained_count(pullrequest_csv_p, reviewerws):
    with open(pullrequest_csv_p) as f:
        data = f.readlines()
        count = 0
        for each in data:
            if all([reviewer in each for reviewer in reviewerws]):
                print(each)
                count +=1
        print(count)


if __name__ == "__main__":
    repo = "HikariCP"
    # comment_network = build_comment_network(repo)
    # print(comment_network.vertices.get('blsem',0))

    # collaboration_count("/Users/leichen/experiement_result/MORCoRE2/infos/fresco/csv/pullrequest.csv")
    pullrequest_csv_p = f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo}/csv/pullrequest.csv"
    collaboration_contained_count(pullrequest_csv_p, ["brettwooldridge","gsmet"])
    # collaboration_contained_count(pullrequest_csv_p, ["brettwooldridge"])