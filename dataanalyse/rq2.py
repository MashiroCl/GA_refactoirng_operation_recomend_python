'''
RQ2: Nsga3RE vs. Nsga3NRE
     NsgaiiRE  vs. NsgaiiNRE
'''

from dataanalyse.rq1 import aggregate_top_k_from_outputs, get_objective_value_list, \
    calc_p_value, calc_effect_size, calc_avg_value, get_fun4algors
from translation.translate import build_NRE_a,get_genes, decode_gene, encode_abs, trans_decoded_gene
from scipy.stats import ttest_ind
from translation.extract_results import top_k
import matplotlib.pyplot as plt
from search_technique.SearchTechnique import SearchTechnique
import statistics


def prepare_path(repo_name, output_root, file_f="FUN.NsgaiiNRE", file_v="VAR.NsgaiiNRE"):
    fun_p = output_root + file_f
    var_p = output_root + file_v
    infos = {
        "abs": f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/abs.json",
        "owner": f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/owners.csv",
        "pr": f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/pullrequest.csv"
    }
    return fun_p, var_p, infos


def prepare_NRE_a(repo_name, output_root):
    fun_p, var_p, infos = prepare_path(repo_name, output_root)
    build_NRE_a(fun_p, var_p, infos)


def siginificant_difference_fun(data1, data2, objective):
    data1_o = get_objective_value_list(data1, objective)
    data2_o = get_objective_value_list(data2, objective)

    # print(f"nre average score: {sum(data1_o) / len(data1_o)}")
    # print(f"re average score: {sum(data2_o) / len(data2_o)}")
    return ttest_ind(data1_o, data2_o).pvalue


def get_3_objs_values(data1):
    return [get_objective_value_list(data1, 0), \
            get_objective_value_list(data1, 1), \
            get_objective_value_list(data1, 2)]


def three_d_plot(data1, data2):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    print(sum(get_3_objs_values(data1)[2]) / len(get_3_objs_values(data1)[2]))
    print(sum(get_3_objs_values(data2)[2]) / len(get_3_objs_values(data2)[2]))
    ax.scatter(get_3_objs_values(data1)[0], get_3_objs_values(data1)[1], get_3_objs_values(data1)[2], color='red',
               marker='o')
    ax.scatter(get_3_objs_values(data2)[0], get_3_objs_values(data2)[1], get_3_objs_values(data2)[2], color='blue',
               marker='^')
    plt.show()


def re_better_than_nre(data1, data2, objective=2):
    data1_o = get_objective_value_list(data1, objective)
    data2_o = get_objective_value_list(data2, objective)

    return (sum(data1_o) / len(data1_o)) > (sum(data2_o) / len(data2_o))


def table_p_value_eff_size_row(repo, f_re, f_nre, mode="p-value", k=5):
    re = aggregate_top_k_from_outputs(repo, f_re, k)
    nre = aggregate_top_k_from_outputs(repo, f_nre, k)

    objs_values = []
    for obj in range(3):
        cs_re = get_objective_value_list(re, obj)
        cs_nre = get_objective_value_list(nre, obj)
        if mode == "p-value":
            RevsNre = calc_p_value(cs_re, cs_nre)
        else:
            RevsNre = calc_effect_size(cs_re, cs_nre)
        objs_values.append(RevsNre)
    return objs_values


def table_delta_avg_percentage_row(repo, f_re, f_nre, mode="avg_delta", k=5):
    def avg_delta(data1, data2):
        avg1 = calc_avg_value(data1)
        avg2 = calc_avg_value(data2)
        return avg1 - avg2

    def avg_delta_percentage(data1, data2):
        avg1 = calc_avg_value(data1)
        avg2 = calc_avg_value(data2)
        return (avg1 - avg2) / avg2 * 100

    re = aggregate_top_k_from_outputs(repo, f_re, k)
    nre = aggregate_top_k_from_outputs(repo, f_nre, k)
    objs_values = []
    for obj in range(3):
        cs_re = get_objective_value_list(re, obj)
        cs_nre = get_objective_value_list(nre, obj)

        if mode == "avg_delta":
            RevsNre = avg_delta(cs_re, cs_nre)
        else:
            RevsNre = avg_delta_percentage(cs_re, cs_nre)
        objs_values.append(RevsNre)

    return objs_values


def table_delta_median_percentage_row(repo, f_re, f_nre, mode="avg_delta", k=5):
    def median_delta(data1, data2):
        median1 = statistics.median(data1)
        median2 = statistics.median(data2)
        return median1 - median2

    def relative(data1, data2):
        median1 = statistics.median(data1)
        median2 = statistics.median(data2)
        return (median1 - median2) / median2 * 100

    re = aggregate_top_k_from_outputs(repo, f_re, k)
    nre = aggregate_top_k_from_outputs(repo, f_nre, k)
    objs_values = []
    for obj in range(3):
        cs_re = get_objective_value_list(re, obj)
        cs_nre = get_objective_value_list(nre, obj)

        if mode == "median_delta":
            RevsNre = median_delta(cs_re, cs_nre)
        else:
            RevsNre = relative(cs_re, cs_nre)
        objs_values.append(RevsNre)

    return objs_values

def build_table_repo_row(repo, avg_delta_row, avg_delta_relative,
                                   p_value_row, effect_size_row, book_tab=True):
    res = repo

    color_record = color_background(p_value_row, avg_delta_row)
    grey = "\cellcolor[gray]{0.8}"

    # p-value & effect size
    for objective in range(3):
        color = ""
        if color_record[objective]:
            color = grey
        value = p_value_row[objective]
        if value < 0.05:
            if value >= 0.001:
                res += f" &{color} {format(value, '.3f')}"
            else:
                res += f" &{color} $<$0.001"
        else:
            res += " & " + str(format(value, '.3f'))
        res+=f" &{color} " + effect_size_row[objective]

    # avg delta & avg delta percentage
        res += f" &{color} " + str(format(avg_delta_row[objective], '.5f'))
        value = avg_delta_relative[objective]
        if value > 0:
            value = f"{color}(+" + str(format(value, '.2f')) +"\%)"
        else:
            value = "("+str(format(value, '.2f')) +"\%)"
        res += f" &{color} " + value

    if book_tab:
        res = res + r"\\ \midrule"
    else:
        res = res + r"\\ \hline"
    return res


def deduce_refactorings(aggregated_strs, repo_name, output_num, algo):
    data_root_path = f"/Users/leichen/experiement_result/MORCoRE2/output/"
    fun_p, var_p, infos = prepare_path(repo_name, data_root_path + repo_name + f"/output{output_num}/", f"FUN.{algo}",
                                       f"VAR.{algo}")
    st = SearchTechnique()
    abs = st.load_repository(json_file=infos["abs"], exclude_test=True, exclude_anonymous=True)

    res = []
    from copy import deepcopy
    for row in aggregated_strs[output_num - 1]:
        abs_temp = deepcopy(abs)
        encoder = encode_abs(abs_temp)
        gene = get_genes(row, fun_p, var_p)
        refactorings = decode_gene(gene, encoder)
        paths = {}
        paths["owners"] = infos["owner"]
        paths["pr"] = infos["pr"]
        ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths,repo_name)
        # print(-row[2]*len(ref_sequence))
        # for each in ref_sequence:
        #     if each["semantic_coherence"]<0.1:
        #         print(each)
        res.append(ref_sequence)
    return res


def color_background(p_value_row, median_delta_row):
    p_value_record = [False for _ in range(3)]
    for objective, v in enumerate(p_value_row):
        if float(p_value_row[objective]) < 0.05 and float(median_delta_row[objective]) > 0:
            p_value_record[objective] = True
    return p_value_record


if __name__ == "__main__":
    # # build NRE_a
    output_root = "/Users/leichen/experiement_result/MORCoRE2/output/"
    # repos = ['HikariCP','dagger','ActionBarSherlock','AndroidAsync', 'mockito']
    # repos = ['auto']
    # repos = ['UltimateRecyclerView']
    # repos = ['guice']
    # repos = ['quasar']
    # repos = ['fresco']
    # repos = ['dagger']
    # repos = ['guice']
    # for repo in repos:
    #     for i in range(1, 6):
    #         prepare_NRE_a(repo, output_root + repo + "/output" + str(i)+"/")

    # siginificant_difference
    repos = ['HikariCP', 'dagger', 'ActionBarSherlock', 'AndroidAsync', 'mockito', 'auto', 'UltimateRecyclerView',
             'guice', 'quasar', 'fresco']
    algo = ['Nsga3RE', 'Nsga3NRE', 'NsgaiiRE', 'NsgaiiNRE']
    f1 = "FUN.Nsga3NRE_a"
    f2 = "FUN.Nsga3RE"
    f3 = "FUN.NsgaiiNRE_a"
    f4 = "FUN.NsgaiiRE"
    k = 5
    # repos = ['HikariCP']
    # for repo in repos:
    #     nres = []
        # nre3 = aggregate_top_k_from_outputs(repo, f1, k)
        # re3 = aggregate_top_k_from_outputs(repo, f2, k)
    #     p_value3 = siginificant_difference_fun(nre3, re3, 2)
    #     # print(f"{repo} {f2} {re_better_than_nre(re3, nre3)}")
    #     # print(f"{repo} {f2} {p_value3}")
    #     # if re_better_than_nre(re3, nre3) and p_value3 < 0.05:
    #     #     print(f"{repo} {f2} shows significant difference")
    #     nre2 = aggregate_top_k_from_outputs(repo, f3, k)
    #     re2 = aggregate_top_k_from_outputs(repo, f4, k)
    #     p_value2 = siginificant_difference_fun(nre2, re2, 2)
    #     # print(f"{repo} {f4} {re_better_than_nre(re2, nre2)}")
    #     # print(f"{repo} {f4} {p_value2}")
    #     # if re_better_than_nre(re2, nre2) and p_value2 < 0.05:
    #     #     print(f"{repo} {f4} shows significant difference")
    #     p_value4 = siginificant_difference_fun(nre3, re2, objective=2)
    #     if re_better_than_nre(re2, nre3) and p_value4 < 0.05:
    #         print(f"{repo} {f4} shows significant difference")

        # compare NSGAII- vs. NSGAII-
        # cs3,cs2 = 0,0
        # count3,count2 = 0,0
        # # print(nre3)
        # for i in range(5):
        #     for j in range(len(nre3[i])):
        #         count3+=1
        #         cs3 += nre3[i][j][2]
        #     for j in range(len(nre2[i])):
        #         count2+=1
        #         cs2 += nre2[i][j][2]
        # if -1*cs3/count3<-1*cs2/count2:
        #     print(repo)

        # translate solutions into refactorings to find high QG & high CS but low SC example
        # for i in range(1, 6):
        #     re2_qmood = deduce_refactorings(re2, repo, i, algo[2])
            # print(re2_qmood)

    # 3d plot
    # repos = ['HikariCP', 'dagger', 'ActionBarSherlock', 'AndroidAsync', 'mockito', 'auto', 'UltimateRecyclerView',
    #          'guice', 'quasar', 'fresco']
    # f1 = "FUN.Nsga3NRE_a"
    # f2 = "FUN.Nsga3RE"
    # f3 = "FUN.NsgaiiNRE_a"
    # f4 = "FUN.NsgaiiRE"
    # k = 5
    # repos = ['HikariCP', 'fresco']
    # for repo in repos:
    #     nre = aggregate_top_k_from_outputs(repo, f3, k)
    #     re = aggregate_top_k_from_outputs(repo, f4, k)
    #
    #     three_d_plot(re, nre)


    fre = "FUN.NsgaiiRE"
    fnre = "FUN.NsgaiiNRE_a"
    # # build rq2_booktab
    relatives = []
    for repo in repos:
        p_value_row = table_p_value_eff_size_row(repo,fre,fnre,"p-value")
        effect_size_row = table_p_value_eff_size_row(repo,fre,fnre,"effect_size")
    #     # avg_delta_row = table_delta_avg_percentage_row(repo,fre,fnre,"avg_delta")
    #     # avg_delta_relative = table_delta_avg_percentage_row(repo,fre,fnre,"avg_delta_relative")
        median_delta_row = table_delta_median_percentage_row(repo,fre,fnre,"median_delta")
        median_delta_relative = table_delta_avg_percentage_row(repo,fre,fnre,"median_delta_relative")
        # res = build_table_repo_row(repo, avg_delta_row, avg_delta_relative, p_value_row, effect_size_row)
        res = build_table_repo_row(repo, median_delta_row, median_delta_relative, p_value_row, effect_size_row)
        print(res)

    # average of avg delta percentage(relative) on all repos:
        relatives.append(median_delta_relative)
    for o in range(3):
        total = 0
        for i in range(len(relatives)):
            total += relatives[i][o]
        print(total/len(relatives))


