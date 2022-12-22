'''
Santi Check:  How does our proposed technique perform on searching
refactorings compared to other existing heuristic algorithms?
'''

import os
from translation.extract_results import top_k
from translation.translate import trans_NRE_valkyrie
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, ranksums
from search_technique.SearchTechnique import SearchTechnique
from translation.translate import get_reviewers, get_genes, decode_gene, encode_abs, trans_decoded_gene
from cliffs_delta import cliffs_delta
import statistics

data_root_path = f"/Users/leichen/experiement_result/MORCoRE2/output/"
objectives = {0: "QG", 1: "SC", 2: "CS"}


def aggregate_top_k_from_outputs(repo_name, file, k):
    # res.shape = 5*k*3
    res = []
    for output_num in range(1, 6):
        content_path = os.path.join(data_root_path, repo_name, "output" + str(output_num), file)
        res.append(top_k(content_path, k=k))
    return res


def get_objective_value_list(data, objective, positive=True):
    data_o = []
    for each_output_file in data:
        for objective_values in each_output_file:
            if not positive:
                data_o.append(objective_values[objective])
            else:
                data_o.append(-1 * objective_values[objective])
    return data_o


def get_fun4algors(repo_name, objective, k, re="RE"):
    algorithms = ["Nsga3", "Nsgaii", "RandomSearch"]
    data = {}
    for algo in algorithms:
        objective_values = aggregate_top_k_from_outputs(repo_name, "FUN." + algo + re, k)
        data[algo] = get_objective_value_list(objective_values, objective)
    return data


def compare_algor_box_plot(repo_name, objective, k):
    data = get_fun4algors(repo_name, objective, k)
    fig, ax = plt.subplots()
    # ax.boxplot(data.values())
    ax.violinplot(data.values())
    ax.set_xticklabels(data.keys())
    ax.title.set_text(f"{objectives[objective]} of {repo_name}")
    plt.savefig(f"/Users/leichen/experiement_result/MORCoRE2/RQ1/{objectives[objective]} of {repo_name}.pdf")
    plt.show()


def compare_algor_avg(repo_name, objective, k):
    data = get_fun4algors(repo_name, objective, k)
    if (sum(data["Nsga3"]) / len(data["Nsga3"])) < (sum(data["Nsgaii"]) / len(data["Nsgaii"])):
        print(f"{repo_name} {objective}")


def calc_p_value(data1, data2):
    return ranksums(data1, data2).pvalue


def calc_t_test_p_value(data1, data2):
    return ttest_ind(data1, data2).pvalue


def calc_avg_value(data):
    return sum(data) / len(data)


def table_avg_diff(repo_name, k=5):
    def avg_diff_ratio(data1, data2):
        avg1 = calc_avg_value(data1)
        avg2 = calc_avg_value(data2)
        return (avg1 - avg2) / avg2 * 100

    objectives = []
    for objective in range(3):
        objective_x = []
        repo_1objective_value = get_fun4algors(repo_name, objective, k)
        iiivsii = avg_diff_ratio(repo_1objective_value['Nsga3'], repo_1objective_value['Nsgaii'])
        iiivsr = avg_diff_ratio(repo_1objective_value['Nsga3'], repo_1objective_value['RandomSearch'])
        iivsr = avg_diff_ratio(repo_1objective_value['Nsgaii'], repo_1objective_value['RandomSearch'])
        objective_x.append(iiivsr)
        objective_x.append(iivsr)
        objective_x.append(iiivsii)
        objectives.append(objective_x)
    return objectives


def table_p_value_eff_size_row(repo_name, mode="p-value", k=5):
    objectives = []
    for objective in range(3):
        objective_x = []
        repo_1objective_value = get_fun4algors(repo_name, objective, k)
        if mode == "p-value":
            iivsiii = calc_p_value(repo_1objective_value['Nsgaii'], repo_1objective_value['Nsga3'])
            iiivsr = calc_p_value(repo_1objective_value['Nsga3'], repo_1objective_value['RandomSearch'])
            iivsr = calc_p_value(repo_1objective_value['Nsgaii'], repo_1objective_value['RandomSearch'])
        else:
            iivsiii = calc_effect_size(repo_1objective_value['Nsgaii'], repo_1objective_value['Nsga3'])
            iiivsr = calc_effect_size(repo_1objective_value['Nsga3'], repo_1objective_value['RandomSearch'])
            iivsr = calc_effect_size(repo_1objective_value['Nsgaii'], repo_1objective_value['RandomSearch'])
        objective_x.append(iivsr)
        objective_x.append(iiivsr)
        objective_x.append(iivsiii)
        objectives.append(objective_x)
    return objectives


def table_delta_avg(repo_name, mode="avg_delta", k=5):
    def avg_delta(data1, data2):
        avg1 = calc_avg_value(data1)
        avg2 = calc_avg_value(data2)
        return avg1 - avg2

    def avg_delta_percentage(data1, data2):
        avg1 = calc_avg_value(data1)
        avg2 = calc_avg_value(data2)
        return (avg1 - avg2) / avg2 * 100

    objectives = []
    for objective in range(3):
        objective_x = []
        repo_1objective_value = get_fun4algors(repo_name, objective, k)
        if mode == "avg_delta":
            iivsiii = avg_delta(repo_1objective_value['Nsgaii'], repo_1objective_value['Nsga3'])
            iiivsr = avg_delta(repo_1objective_value['Nsga3'], repo_1objective_value['RandomSearch'])
            iivsr = avg_delta(repo_1objective_value['Nsgaii'], repo_1objective_value['RandomSearch'])
        else:
            iivsiii = avg_delta_percentage(repo_1objective_value['Nsgaii'], repo_1objective_value['Nsga3'])
            iiivsr = avg_delta_percentage(repo_1objective_value['Nsga3'], repo_1objective_value['RandomSearch'])
            iivsr = avg_delta_percentage(repo_1objective_value['Nsgaii'], repo_1objective_value['RandomSearch'])
        objective_x.append(iivsr)
        objective_x.append(iiivsr)
        objective_x.append(iivsiii)
        objectives.append(objective_x)
    return objectives


def table_delta_median(repo_name, mode="median_delta", k=5):
    def median_delta(data1, data2):
        median1 = statistics.median(data1)
        median2 = statistics.median(data2)
        return median1 - median2

    def relative(data1, data2):
        median1 = statistics.median(data1)
        median2 = statistics.median(data2)
        return (median1 - median2) / median2 * 100

    objectives = []
    for objective in range(3):
        objective_x = []
        repo_1objective_value = get_fun4algors(repo_name, objective, k)
        if mode == "median_delta":
            iivsiii = median_delta(repo_1objective_value['Nsgaii'], repo_1objective_value['Nsga3'])
            iiivsr = median_delta(repo_1objective_value['Nsga3'], repo_1objective_value['RandomSearch'])
            iivsr = median_delta(repo_1objective_value['Nsgaii'], repo_1objective_value['RandomSearch'])
        else:
            iivsiii = relative(repo_1objective_value['Nsgaii'], repo_1objective_value['Nsga3'])
            iiivsr = relative(repo_1objective_value['Nsga3'], repo_1objective_value['RandomSearch'])
            iivsr = relative(repo_1objective_value['Nsgaii'], repo_1objective_value['RandomSearch'])
        objective_x.append(iivsr)
        objective_x.append(iiivsr)
        objective_x.append(iivsiii)
        objectives.append(objective_x)
    return objectives


def color_background(p_value_row, avg_delta_row):
    p_value_record = [[False for _ in range(3)] for _ in range(3)]
    for algo in range(3):
        for objective, v in enumerate(p_value_row):
            if float(p_value_row[objective][algo]) < 0.05 and float(avg_delta_row[objective][algo]) > 0:
                p_value_record[objective][algo] = True
    return p_value_record


def build_table_repo_row(repo, avg_delta_row, avg_delta_relative,
                         p_value_row, effect_size_row, book_tab=True):
    grey = "\cellcolor[gray]{0.8}"
    # grey2 = "\cellcolor[gray]{0.8}"
    res = "\multirow{4}{*}{" + repo + "} & p-value"

    p_value_record = color_background(p_value_row, avg_delta_row)

    for algo in range(3):
        for objective, v in enumerate(p_value_row):
            value = p_value_row[objective][algo]
            color = ""
            if p_value_record[objective][algo]:
                color = grey
            # elif algo == 2 and avg_delta_row[objective][algo]>=0:
            #     color = grey2
            if value < 0.05:
                if value >= 0.001:
                    res += f" &{color} {format(value, '.3f')}"
                else:
                    res += f" &{color} $<$0.001"
            else:
                res += f" & {color}" + str(format(value, '.3f'))

    # effect size
    res = res + r"\\ &effect size"
    for algo in range(3):
        for objective, v in enumerate(effect_size_row):
            value = effect_size_row[objective][algo]
            color = ""
            if p_value_record[objective][algo]:
                color = grey
            # elif algo == 2 and avg_delta_row[objective][algo]>=0:
            #     color = grey2
            res += f" & {color}" + value

    # avg delta
    res = res + r"\\ & $\AD$"
    for algo in range(3):
        for objective, v in enumerate(avg_delta_row):
            value = avg_delta_row[objective][algo]
            color = ""
            if p_value_record[objective][algo]:
                color = grey
            # elif algo == 2 and avg_delta_row[objective][algo]>=0:
            #     color = grey2
            res += f" & {color}" + str(format(value, '.4f'))

    # avg relative
    res = res + r"\\ & \(relative\)"
    for algo in range(3):
        for objective, v in enumerate(avg_delta_relative):
            value = avg_delta_relative[objective][algo]
            color = ""
            if p_value_record[objective][algo]:
                color = grey
            # elif algo == 2 and avg_delta_row[objective][algo]>=0:
            #     color = grey2
            if value > 0:
                value = f"{color}" + "(+" + str(format(value, '.1f')) + "$\%$)"
            else:
                value = f"{color} (" +str(format(value, '.1f')) + "$\%$)"
            res += " & " + value

    if book_tab:
        res = res + r"\\ \midrule"
    else:
        res = res + r"\\ \hline"
    return res


def count_owners(repo):
    path = f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo}/csv/owners.csv"
    with open(path) as f:
        data = f.readlines()
    owners = set()
    for row in data:
        owners.add(row.split(",")[1])
    return owners


def count_superowner_ownershipratio(repo):
    def cal_superowner_ratio(owner_owns: dict):
        res = dict()
        total = sum(owner_owns.values())
        for each in owner_owns.keys():
            if (owner_owns[each]) / total > 0.2:
                res[each] = owner_owns[each] / total
        return res

    owner_owns = {}
    path = f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo}/csv/owners.csv"
    with open(path) as f:
        data = f.readlines()
    for row in data:
        owner = row.split(",")[1]
        owner_owns[owner] = owner_owns.get(owner, 0) + 1
    return cal_superowner_ratio(owner_owns)


def calc_effect_size(data1, data2):
    d, res = cliffs_delta(data1, data2)
    return res


if __name__ == "__main__":
    repos = ['HikariCP', 'dagger', 'auto', 'UltimateRecyclerView', 'AndroidAsync',
             'ActionBarSherlock', 'mockito', 'guice', 'quasar', 'fresco']
    f1 = "FUN.Nsga3RE"
    f2 = "FUN.NsgaiiRE"
    f3 = "FUN.RandomSearchRE"
    k = 5

    'compare average among different algorithms'
    # for repo in repos:
    #     for obj in range(0, 3):
    #         compare_algor_avg(repo, obj, k)

    # repos = ['ActionBarSherlock']
    # 'calculate p_value between each two algorithms on each objective for a repository'
    avg_diff_rows = []
    for repo in repos:
        # avg_delta_row = table_delta_avg(repo,"avg_delta")
        # avg_delta_relative = table_delta_avg(repo,"avg_delta_percentage")
        median_delta_row = table_delta_median(repo, "median_delta")
        median_delta_relative = table_delta_median(repo, "median_delta_relative")
        p_value_row = table_p_value_eff_size_row(repo, "p-value")
        effect_size_row = table_p_value_eff_size_row(repo, "effect_size")
        # res = build_table_repo_row(repo,
        #                            avg_delta_row, avg_delta_relative,
        #                            p_value_row, effect_size_row,
        #                            book_tab=True)
        res = build_table_repo_row(repo,
                                   median_delta_row, median_delta_relative,
                                   p_value_row, effect_size_row,
                                   book_tab=True)
        print(res)
    #     # print(p_value_row)
    #     avg_diff_row = median_delta_relative
    #     avg_diff_rows.append(avg_diff_row)
    #     # print(avg_diff_row)

    # increment in avg_v
    # avg_v = 0
    # for i in range(len(avg_diff_rows)):
    #     avg_v+=avg_diff_rows[i][1][2]
    #     print(avg_diff_rows[i][1][2])
    # print(avg_v/len(avg_diff_rows))

    # repos = ['dagger','mockito','UltimateRecyclerView', 'guice','auto']
    # for repo in repos:
    # count owners
    #     # owners = count_owners(repo)
    #     # print(f"{repo}: {len(owners)}")
    #
    # count superowner ratio
    #     superowner_ownershipratio = count_superowner_ownershipratio(repo)
    #     print(f"{repo}: {superowner_ownershipratio}")
