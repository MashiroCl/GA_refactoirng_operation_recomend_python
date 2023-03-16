'''
RQ2_2
Investigate the reviewer pattern in the results
'''

from dataanalyse.rq1 import aggregate_top_k_from_outputs
from dataanalyse.rq3 import deduce_reviewers, deduce_files
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from collaboration.collaboration import get_collaboration_score
from collaboration.graph import Graph
from copy import deepcopy
import ast
from collections import Counter

class Patterns:
    def __init__(self, name):
        self.name = name
        self.d = dict()
        self.avg = dict()
        self.cs = dict()
        self.cs_avg = dict()

    def add(self, l):
        pattern = reviewer_pattern(l)
        if pattern not in self.d.keys():
            self.d.setdefault(pattern, []).append(l)
        else:
            self.d[pattern].append(l)

    def calc_avg(self):
        avg = {}
        n = 0
        for each in self.d.keys():
            n += len(self.d[each])
        for each in self.d.keys():
            avg[each] = len(self.d[each]) / n
        self.avg = avg
        return avg

    def calc_collaboration_socre(self,comment_network):
        for each in self.d.keys():
            for reviewer_group in self.d[each]:
                self.cs[each] = self.cs.get(each,0)+ calc_collaboration_score(comment_network, reviewer_group)
        return self.cs

    def get_cs_avg(self):
        total = sum(self.cs.values())
        for each in self.cs.keys():
            self.cs_avg[each] = self.cs[each]/total
        return self.cs_avg

def patterns_count_2df(pl: 'List[Patterns]'):
    patterns = ['AA', 'AB', 'ABC', 'AAB', 'ABCD', 'AABC', 'AABB']
    l = []
    for p in pl:
        l.append([p.name] + [p.avg.get(each, 0) for each in patterns])
    return pd.DataFrame(l, columns=['repo'] + patterns)

def patterns_cs_avg_2df(pl):
    patterns = ['AA', 'AB', 'ABC', 'AAB', 'ABCD', 'AABC', 'AABB']
    l = []
    for p in pl:
        l.append([p.name] + [p.get_cs_avg().get(each, 0) for each in patterns])
    return pd.DataFrame(l, columns=['repo'] + patterns)

def reviewer_pattern(l: 'List[str]') -> 'List':
    # patterns: AB ABC ABCD AA AABB AAB AABC
    if len(l) == 2:
        if len(set(l)) == 1:
            return "AA"
        else:
            return "AB"
    elif len(l) == 3:
        if len(set(l)) == 3:
            return "ABC"
        elif len(set(l)) == 2:
            return "AAB"
    elif len(l) == 4:
        if len(set(l)) == 4:
            return "ABCD"
        elif len(set(l)) == 3:
            return "AABC"
        elif len(set(l)) == 2:
            return "AABB"
    return "unknown"


def stacked_bar(df):
    color = ['#8ECFC9', '#FFBE7A', '#FA7F6F', '#82B0D2', '#BEB8DC', '#E7DAD2', '#96C37D']
    # color = ['#F27970', '#BB9727', '#54B345', '#32B897', '#05B9E2','#8983BF','#C76DA2']
    title = 'Reviewer Patterns Ratio'
    ax = df.plot(x='repo', kind='barh',
                 stacked=True,
                 color=color,
                 figsize=(22, 15),
                 fontsize=25
                 )
    ax.legend(loc=1, fontsize=20)
    ax.set_title(title, pad=20, fontdict={'fontsize': 30})
    # plt.savefig(f"/Users/leichen/experiement_result/MORCoRE2/RQ2_2/reviewers_pattern_ratio.pdf")
    plt.show()


def re_solution_reviewer_ratio(reviewers_re):
    reviewers_d = {}
    for each in reviewers_re:
        for reviewer in set(each):
            reviewers_d[reviewer] = reviewers_d.get(reviewer, 0) + 1
    reviewers_ratio = {}
    for each in reviewers_d:
        reviewers_ratio[each] = reviewers_d[each] / len(reviewers_re)
    return reviewers_ratio


def re_solution_same_reviewer_list_ratio(reviewers_list):
    def get_reviewer_list():
        pass

    same_reviewer_list = {}
    for each in reviewers_list:
        each = sorted(each)
        same_reviewer_list[str(each)] = same_reviewer_list.get(str(each), 0) + 1
    same_reviewer_list_ratio = {}
    total = sum(same_reviewer_list.values())
    for each in same_reviewer_list:
        same_reviewer_list_ratio[each] = same_reviewer_list[each] / total
    return dict(sorted(same_reviewer_list_ratio.items(), key=lambda item: item[1], reverse=True))

def solution_reviewer_list_cs_contribution(reviewers_list, comment_network):
    rl_frequency = {}
    for each in reviewers_list:
        each = sorted(each)
        rl_frequency[str(each)] = rl_frequency.get(str(each), 0) + 1
    rl_cs_contribution={}
    for each in rl_frequency:
        rl_cs_contribution[each] = calc_collaboration_score(comment_network,ast.literal_eval(each))*rl_frequency[each]
    # calculate average
    total = sum(rl_cs_contribution.values())
    for each in rl_cs_contribution:
        rl_cs_contribution[each] = rl_cs_contribution[each]/total
    return dict(sorted(rl_cs_contribution.items(), key=lambda item: item[1], reverse=True))


def re_solution_same_file_ratio(re_rs, re_ns):
    files_rs = []
    files_ns = []
    files_rs += deduce_files(re_rs, repo, output_num, algo[2])
    files_ns += deduce_files(re_ns, repo, output_num, algo[4])
    rs_dict = {}
    ns_dict = {}
    for each in files_rs:
        rs_dict[each] = rs_dict.get(each, 0) + 1
    for each in files_ns:
        ns_dict[each] = ns_dict.get(each, 0) + 1
    same_files = []
    for each in rs_dict.keys():
        if each in ns_dict.keys():
            same_files.append(each)
    print(sum(rs_dict[each] for each in same_files) / sum(rs_dict.values()))
    print(sum(ns_dict[each] for each in same_files) / sum(ns_dict.values()))


def get_vulnerability_ratio(patterns):
    return patterns.avg.get("AA", 0) + patterns.avg.get("AB", 0) + patterns.avg.get("AAB", 0)


def build_comment_network(repo):
    pr_csv = f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo}/csv/pullrequest.csv"
    graph = Graph()
    graph.build_from_csv(pr_csv)
    return graph


def calc_collaboration_score(comment_network, reviewers):
    score = 0
    temp_reviewers = deepcopy(reviewers)
    score += get_collaboration_score(comment_network, temp_reviewers)
    return score


if __name__ == "__main__":
    # repos = ['HikariCP', 'dagger', 'ActionBarSherlock', 'AndroidAsync', 'mockito', 'auto', 'UltimateRecyclerView',
    #                   'guice', 'quasar', 'fresco']
    # f1 = "FUN.Nsga3RE"
    # f2 = "FUN.Nsga3NRE"
    # f3 = "FUN.NsgaiiRE"
    # f4 = "FUN.NsgaiiNRE"
    # k = 5
    # algo = ['Nsga3RE', 'Nsga3NRE', 'NsgaiiRE', 'NsgaiiNRE']
    # for repo in repos:
    #     p = Patterns(repo)
    #     reviewers_re = []
    #     reviewers_nre = []
    #     re = aggregate_top_k_from_outputs(repo, f3, k)
    #     nre = aggregate_top_k_from_outputs(repo, f4, k)
    #     for i in range(1, 6):
    #         reviewers_re += deduce_reviewers(re, repo, i, algo[2])
    #     for i in range(1, 6):
    #         reviewers_nre += deduce_reviewers(nre, repo, i, algo[3])
    #     for each in reviewers_re:
    #         p.add(each)
    #     print(f"{repo}: {p.avg()}")

    ' stacked bar'
    repos = ['HikariCP', 'dagger', 'auto', 'UltimateRecyclerView', 'AndroidAsync',
             'ActionBarSherlock', 'mockito', 'guice', 'quasar', 'fresco']
    f1 = "FUN.Nsga3RE"
    f2 = "FUN.Nsga3NRE"
    f3 = "FUN.NsgaiiRE"
    f4 = "FUN.NsgaiiNRE"
    f5 = "FUN.RandomSearchRE"
    k = 5
    algo = ['Nsga3RE', 'Nsga3NRE', 'NsgaiiRE', 'NsgaiiNRE', 'RandomSearchRE']
    patternslist = []
    patternslist_nre = []
    repos = ['guice']
    for repo in repos:
        reviewers_re = []
        reviewers_rs_re = []
        reviewers_nre = []
        comment_network = build_comment_network(repo)
        re = aggregate_top_k_from_outputs(repo, f3, k)
        nre = aggregate_top_k_from_outputs(repo, f4, k)
        rs_re = aggregate_top_k_from_outputs(repo, f5, k)
        # for each in re:
        #     for each2 in each:
        #         print(-1*each2[2])
        for output_num in range(1, 6):
            reviewers_re += deduce_reviewers(re, repo, output_num, algo[2])
        for output_num in range(1, 6):
            reviewers_nre += deduce_reviewers(nre, repo, output_num, algo[3])
        # for output_num in range(1, 6):
        #     reviewers_rs_re += deduce_reviewers(rs_re, repo, output_num, algo[4])
        # print("reviewers_re:", reviewers_re)
        # print("*"*30)
        # print("reviewers_nre", reviewers_nre)
        c = Counter([j for sub in reviewers_nre for j in sub])
        print(c)





        # reviewers patterns
        # patterns = Patterns(repo)
        # for each in reviewers_re:
        #     patterns.add(each)
        # patterns.calc_avg()
        # patterns.calc_collaboration_socre(comment_network)
        # vulnerability
        # res = get_vulnerability_ratio(patterns)
        # print(f"NSGAII RE {repo} vulnerability {res}")

        # patterns_nre = Patterns(repo)
        # for each in reviewers_nre:
        #     patterns_nre.add(each)
        # patterns_nre.calc_avg()
        # patterns_nre.calc_collaboration_socre(comment_network)
        # res_nre = get_vulnerability_ratio(patterns_nre)
        # print(f"NSGAII NRE {repo} vulnerability {res_nre}")

        # print(patterns.avg.get("AAB"))
        # print(patterns.avg["AB"])

        # patternslist.append(patterns)
        # patternslist_nre.append(patterns_nre)
        # stacked bar
        # stacked_bar(patterns_count_2df(patternslist))
        # stacked_bar(patterns_count_2df(patternslist_nre))
    # stacked_bar(patterns_cs_avg_2df(patternslist))
    # stacked_bar(patterns_cs_avg_2df(patternslist_nre))

        # reviewers_ratio in solution NSGA-III vs. RandomSearch
        # ns_srr = re_solution_reviewer_ratio(reviewers_re)
        # rs_srr = re_solution_reviewer_ratio(reviewers_rs_re)
        # ns_srr = sorted(ns_srr.items(), key=lambda item: item[1], reverse=True)
        # rs_srr = sorted(rs_srr.items(), key=lambda item: item[1], reverse=True)
        # print(repo, f3, ns_srr)
        # print(repo, f5, rs_srr)

        # same_reviewer_list_ratio NSGA-III vs. RandomSearch
        # ns_smr = re_solution_same_reviewer_list_ratio(reviewers_re)
        # rs_smr = re_solution_same_reviewer_list_ratio(reviewers_rs_re)
        # print(ns_smr)
        # print(rs_smr)
        # # reviewrs list
        # print(repo, f3, ns_smr)
        # print(repo, f5, rs_smr)

        # same_reviewer_list_ratio re vs. nre
        # re_smr = re_solution_same_reviewer_list_ratio(reviewers_re)
        # nre_smr = re_solution_same_reviewer_list_ratio(reviewers_nre)
        # print(f"{repo} nre {len(nre_smr)}")
        # print(f"{repo} re {len(re_smr)}")

        # # reviewrs list cs contribution
        # import csv
        # srlcsc_re = solution_reviewer_list_cs_contribution(reviewers_re,comment_network)
        # srlcsc_nre = solution_reviewer_list_cs_contribution(reviewers_nre, comment_network)
        # with open("/Users/leichen/experiement_result/MORCoRE2/RQ2_2/reviewer_list_cs_contribution_re.csv", mode="a") as f:
        #     writer = csv.writer(f)
        #     writer.writerow([repo])
        #     writer.writerow(srlcsc_re.keys())
        #     writer.writerow(
        #         [calc_collaboration_score(comment_network, ast.literal_eval(each)) for each in srlcsc_re.keys()])
        #     writer.writerow(srlcsc_re.values())
        # with open("/Users/leichen/experiement_result/MORCoRE2/RQ2_2/reviewer_list_cs_contribution_nre.csv", mode="a") as f:
        #     writer = csv.writer(f)
        #     writer.writerow([repo])
        #     writer.writerow(srlcsc_nre)
        #     writer.writerow(
        #         [calc_collaboration_score(comment_network, ast.literal_eval(each)) for each in srlcsc_nre.keys()])
        #     writer.writerow(srlcsc_nre.values())
        # print(repo, f3, re_smr)
        # print(repo, f4, nre_smr)

        # same reviewers ratio
        # ns_same_num = 0
        # rs_same_num = 0
        # for each in ns_smr.keys():
        #     if each in rs_smr.keys():
        #         ns_same_num += ns_smr[each]
        # for each in rs_smr.keys():
        #     if each in ns_smr.keys():
        #         rs_same_num += rs_smr[each]
        # print(repo, f3, ns_same_num/sum(ns_smr.values()))
        # print(repo, f5, rs_same_num/sum(rs_smr.values()))

        # same file ratio
        # re_solution_same_file_ratio(re,rs_re)
