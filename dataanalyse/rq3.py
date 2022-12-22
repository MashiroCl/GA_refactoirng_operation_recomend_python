from translation.translate import get_reviewers, get_genes, decode_gene, encode_abs, trans_decoded_gene
from search_technique.SearchTechnique import SearchTechnique
from dataanalyse.rq2 import prepare_path
from dataanalyse.rq1 import aggregate_top_k_from_outputs, get_objective_value_list

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
        ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths)
        # print(-row[2]*len(ref_sequence))
        for each in ref_sequence:
            # repository dagger
            if {'swankjesse', 'cgruber', 'cgruber', 'swankjesse'} == set(each["reviewers"]) or \
                set(each['reviewers']) == {'swankjesse'} or set(each['reviewers']) == {'cgruber'}:
                print(each["collaboration_score"])
            # res.append(each["reviewers"])
    return res

def deduce_files(aggregated_strs, repo_name, output_num, algo):
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
        ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths)

        for each in ref_sequence:
            # print(each["reviewers"])
            res.append(each["class1path"])
            res.append(each["class2path"])
    return res

def aggregated2str(l: 'List[List[List[float]]]'):
    res = []
    for each_output in l:
        output = []
        for value in each_output:
            output.append([" ".join(str(each) for each in value)])
        res.append(output)
    return res


def vulnerable(l: 'List[str]') -> bool:
    if len(l) == 2:
        # reviewers: A A / A B
        return True
    if len(l) == 3 and len(set(l)) < 3:
        # reviewers: A A B
        return True
    return False

def two_rev(l:'List[str]')->bool:
    if len(l) == 4 and len(set(l)) == 2:
        # reviewers: A A B B
        return True
    return False

def common_rev(l:'List[str]')->bool:
    if len(set(l)) < len(l) and len(set(l))!= 1:
        # print(l)
        return True
    return False

def AABC(l:'List[str]')->bool:
    if len(l)==4 and len(set(l))== 3:
        # print(l)
        return True
    return False


if __name__ == "__main__":
    repos = ['HikariCP', 'dagger', 'ActionBarSherlock', 'AndroidAsync', 'mockito', 'auto', 'quasar']
    # repos = ['mockito']
    f1 = "FUN.Nsga3RE"
    f2 = "FUN.Nsga3NRE"
    f3 = "FUN.NsgaiiRE"
    f4 = "FUN.NsgaiiNRE"
    k = 5
    algo = ['Nsga3RE', 'Nsga3NRE', 'NsgaiiRE', 'NsgaiiNRE']
    for repo in repos:
        reviewers_re = []
        reviewers_nre = []
        re = aggregate_top_k_from_outputs(repo, f3, k)
        nre = aggregate_top_k_from_outputs(repo, f4, k)
        for i in range(1, 6):
            reviewers_re += deduce_reviewers(re, repo, i, algo[2])
        for i in range(1, 6):
            reviewers_nre += deduce_reviewers(nre, repo, i, algo[3])

        # #vulnerable
        # print("In NRE: ", sum([1 if vulnerable(each) else 0 for each in reviewers_nre]))
        # print(len(reviewers_nre))
        # print("In RE: ", sum([1 if vulnerable(each) else 0 for each in reviewers_re]))
        # print(len(reviewers_re))
        # not_vul_nre = 1- sum([1 if vulnerable(each) else 0 for each in reviewers_nre]) / len(reviewers_nre)
        # not_vul_re = 1- sum([1 if vulnerable(each) else 0 for each in reviewers_re]) / len(reviewers_re)
        # print(f"In {repo} NRE: ", not_vul_nre, len(reviewers_nre))
        # print(f"In {repo} RE: ", not_vul_re, len(reviewers_re))
        # print(f"In {repo}", not_vul_re>not_vul_nre)

        # #two_rev
        # print(f"In {repo} NRE: ", sum([1 if two_rev(each) else 0 for each in reviewers_nre]) / len(reviewers_nre))
        # print(f"In {repo} RE: ", sum([1 if two_rev(each) else 0 for each in reviewers_re]) / len(reviewers_re))

        # #common_rev
        # print(f"In {repo} NRE: ", sum([1 if common_rev(each) else 0 for each in reviewers_nre]) / len(reviewers_nre))
        # print(f"In {repo} RE: ", sum([1 if common_rev(each) else 0 for each in reviewers_re]) / len(reviewers_re))


        aabc_nre = sum([1 if AABC(each) else 0 for each in reviewers_nre]) / len(reviewers_nre)
        aabc_re = sum([1 if AABC(each) else 0 for each in reviewers_re]) / len(reviewers_re)
        # print(f"In {repo} NRE: ", aabc_nre, len(reviewers_nre))
        # print(f"In {repo} RE: ", aabc_re, len(reviewers_re))
        print(f"In {repo}  {aabc_re>aabc_nre}  {aabc_re} {aabc_nre}" )