import csv
import pathlib
from translation.translate import get_all_reviewers, get_user_defined_and_inline_classes, calc_quality_gain, \
    encode_abs, get_genes, decode_gene
from refactoring_operation.RefactoringOperationDispatcher import dispatch
from qmood.Qmood import Qmood
from copy import deepcopy
from search_technique.SearchTechnique import SearchTechnique
from dataanalyse.rq2_2 import build_comment_network, aggregate_top_k_from_outputs


def reformat_by_file_name(file_p):
    """
    reformat the csv file to:
    file_name, reviewer1, reviewer2, reviewer3 ...
    """
    d = dict()
    with open(file_p) as f:
        reader = csv.reader(f)
        for line in reader:
            file_name = line[0]
            d[file_name] = d.get(file_name, []) + ([each.strip() for each in line[1:-1]])
    with open(pathlib.Path(file_p).parent.joinpath("expertise.csv"), "w") as f:
        writer = csv.writer(f)
        for each in d.keys():
            writer.writerow([each] + d[each])


def prepare_path(repo_name, output_root, file_f="FUN.NsgaiiNRE", file_v="VAR.NsgaiiNRE"):
    fun_p = output_root + file_f
    var_p = output_root + file_v
    infos = {
        "abs": f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/abs.json",
        "owner": f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/expertise.csv",
        "pr": f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/pullrequest.csv"
    }
    return fun_p, var_p, infos


def trans_decoded_gene(refactorings, abs, paths, repo=""):
    res = []
    field_and_method = ['class1field', 'class1method', 'class2field', 'class2method']
    abs_temp = deepcopy(abs)
    user_defined_classes, inline_class_info = get_user_defined_and_inline_classes(abs)
    initial_objectives = Qmood(abs).calculateQmood(abs, user_defined_classes, inline_class_info)
    for refactoring in refactorings:
        # Filter refactorings didn't pass preconditions
        if dispatch(refactoring["ROType"].value)(refactoring, abs_temp):
            if not (refactoring['class1field'] is None and refactoring['class1method'] is None and
                    refactoring['class2field'] is None and refactoring['class2method'] is None):
                res_dict = dict()
                res_dict["ROType"] = refactoring['ROType']
                res_dict["class1info"] = refactoring['class1'].classInfo
                res_dict["class1path"] = refactoring['class1'].filePath
                res_dict["class2info"] = refactoring['class2'].classInfo
                res_dict["class2path"] = refactoring['class2'].filePath
                for i in field_and_method:
                    if not refactoring[i] is None:
                        res_dict["target"] = refactoring[i]
                res_dict["reviewers"] = get_all_reviewers(refactoring, paths["owners"])
                res_dict["qmood"] = calc_quality_gain(abs, initial_objectives, user_defined_classes, inline_class_info)
                res.append(res_dict)
    return res


data_root_path = f"/Users/leichen/experiement_result/MORCoRE2/output/"


def deduce_reviewers(aggregated_strs, repo_name, output_num, algo):
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
        ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths, repo_name)
        for each in ref_sequence:
            res.append(each["reviewers"])
    return res


if __name__ == "__main__":
    f1 = "FUN.Nsga3RE"
    f2 = "FUN.Nsga3NRE"
    f3 = "FUN.NsgaiiRE"
    f4 = "FUN.NsgaiiNRE"
    f5 = "FUN.RandomSearchRE"
    k = 5
    algo = ['Nsga3RE', 'Nsga3NRE', 'NsgaiiRE', 'NsgaiiNRE', 'RandomSearchRE']

    repos = ['HikariCP', 'dagger', 'auto', 'UltimateRecyclerView', 'AndroidAsync',
             'ActionBarSherlock', 'mockito', 'guice', 'quasar', 'fresco']
    # repos = ['HikariCP']
    for repo in repos:
        expertise_file = f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo}/csv/ownerships.csv"
        reformat_by_file_name(expertise_file)
        reviewers_re = []
        reviewers_rs_re = []
        reviewers_nre = []
        comment_network = build_comment_network(repo)
        re = aggregate_top_k_from_outputs(repo, f3, k)
        nre = aggregate_top_k_from_outputs(repo, f4, k)
        for output_num in range(2, 3):
            reviewers_nre += deduce_reviewers(nre, repo, output_num, algo[3])
            reviewers = []
            for each_ref in reviewers_nre:
                left = [each.strip() for each in each_ref[0]]
                right = [each.strip() for each in each_ref[1]]
                reviewers.append(set(left))
                reviewers.append(set(right))
            common_reviewers = reviewers[0]
            for i,each in enumerate(reviewers):
                common_reviewers = common_reviewers.intersection(each)
            print(f"repo: {repo}, common reviewers: {common_reviewers}")

