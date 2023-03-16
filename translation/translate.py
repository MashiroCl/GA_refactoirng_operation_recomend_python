from copy import deepcopy
from search_technique.SearchTechnique import SearchTechnique
from refactoring_operation.RefactoringOperationDispatcher import dispatch
from refactoring_operation.RefactoringOperationEnum import RefactoringOperationEnum
from encoding.IntegerEncoding import IntegerEncoding
from qmood.Qmood import Qmood
from code_ownership.CodeOwnership import CodeOwnership
from code_ownership.DeveloperGraph import DeveloperGraph
from code_ownership.PullRequestService import PullRequestService
from semantic.NameExtractor import NameExtractor
from semantic.Vectorize import TF_IDF
from collaboration.collaboration import get_collaboration_score
from collaboration.graph import Graph
from copy import deepcopy
from translation.extract_results import top_k
from expertise.ownership import get_path_owner_dict
from scipy.stats import ttest_ind
from search_technique.SearchROProblem import SearchROProblem, extract_user_defined_classes, \
    extract_class_with_one_child, extract_class_with_one_child_zero_parent_list
from search_technique.SearchROProblemRE import SearchROProblemRE
from search_technique.enviroment.Platform import LocalPlatform
from qmood.metricCalculation import init_inline_class_info


def get_genes(target: str, fun_p: str, var_p: str) -> 'List[int]':
    def str2float(s: str):
        strs = s.strip().split(" ")
        return [float(each) for each in strs if len(each) > 0]

    if isinstance(target, list):
        target = " ".join([str(each) for each in target])
    target = str2float(target)
    with open(fun_p) as f:
        lines = f.readlines()
    fun = [str2float(each) for each in lines]
    target_index = -1
    for index, each in enumerate(fun):
        if target == each:
            target_index = index
            break
    with open(var_p) as f:
        lines = f.readlines()
    if target_index != -1:
        return [int(each) for each in lines[target_index].strip().split(" ")]
    else:
        print("No result found")
        return None


def get_reviewers(refactoring, owners_p):
    '''
    param f: owners.csv
    '''
    res = []
    with open(owners_p) as f:
        owner_rows = f.readlines()
    for owner_row in owner_rows:
        infos = owner_row.split(",")
        if infos[0] == refactoring["class1"].getFilePath().strip():
            res.append(infos[1])
        if infos[0] == refactoring["class2"].getFilePath().strip():
            res.append(infos[1])
        if len(res) == 4:
            break
    return res


def get_all_reviewers(refactoring, expertise_p):
    """
    get all developers who have ever contributed to the files being refactored by refactoring
    expertise_p: file path for the ownership2.csv
    """
    res = []
    with open(expertise_p) as f:
        expertise_rows = f.readlines()
    for expertise_row in expertise_rows:
        infos = expertise_row.split(",")
        if infos[0] == refactoring["class1"].getFilePath().strip():
            res.append(infos[1:])
        if infos[0] == refactoring["class2"].getFilePath().strip():
            res.append(infos[1:])
        if len(res) == 2:
            break
    return res

def calc_quality_gain(abs, initial_objectives, user_defined_classes, inline_class_info):
    qmood_metrics_list = ["Effectiveness", "Extendibility", "Flexibility", "Functionality", "Resusability",
                          "Understandability"]

    qmood_metrics_value = Qmood(abs).calculateQmood(abs, user_defined_classes, inline_class_info)
    return sum([(qmood_metrics_value[metric] - initial_objectives[metric]) for metric in qmood_metrics_list])


def calc_semantic_coherence(repo, abs, decoded_sequence):
    platform = LocalPlatform()
    platform.set_repository(repo)
    search_ro_problem_re = SearchROProblemRE(abs, platform)
    # search_ro_problem.abs_representation = abs
    # search_ro_problem.classes_nameSequence_dict = search_ro_problem.extract_names_sequences()
    semantic_coherence = search_ro_problem_re.calc_sematic_coherence(decoded_sequence)

    'calculate call relation'
    call_relation = search_ro_problem_re.call_graph.calc_call_relation(decoded_sequence)
    return 0.2 * semantic_coherence + 0.8 * call_relation


def calc_collaboration_score(pr_csv, reviewers):
    graph = Graph()
    graph.build_from_csv(pr_csv)
    score = 0
    temp_reviewers = deepcopy(reviewers)
    score += get_collaboration_score(graph, temp_reviewers)
    return score


def encode_abs(abs: 'List[jClass]'):
    encoder = IntegerEncoding()
    encoder.encoding(abs)
    return encoder


def decode_gene(genes, encoder):
    refactorings = encoder.decoding(genes)
    return refactorings


def get_user_defined_and_inline_classes(abs):
    user_defined_classes = extract_user_defined_classes(abs)
    inline_class_info = init_inline_class_info()
    return user_defined_classes, inline_class_info


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
                res_dict["reviewers"] = get_reviewers(refactoring, paths["owners"])
                # res_dict["semantic_coherence"] = calc_semantic_coherence(repo, abs, [refactoring])
                res_dict["qmood"] = calc_quality_gain(abs, initial_objectives, user_defined_classes, inline_class_info)
                # refactoring, call_graph_path, ownership_path, repo_name
                res_dict["collaboration_score"] = calc_collaboration_score(paths["pr"], res_dict["reviewers"])
                res.append(res_dict)
    return res


def get_RE_collaboration_valkyrie(repo_name, algorithm):
    fun_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/FUN.{algorithm}RE"
    funs = top_k(fun_p, 5)
    return [each[2] for each in funs]


def trans_RE_valkyrie(repo_name, algorithm):
    st = SearchTechnique()
    json_file_path = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/csv/abs.json"
    abs = st.load_repository(json_file=json_file_path, exclude_test=True, exclude_anonymous=True)
    fun_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/FUN.{algorithm}RE"
    var_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/VAR.{algorithm}RE"
    owners_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/csv/owners.csv"
    funs = top_k(fun_p, 5)
    count = 0
    from copy import deepcopy
    res = []
    for fun in funs:
        abs_temp = deepcopy(abs)
        encoder = encode_abs(abs_temp)
        count += 1
        gene = get_genes(fun, fun_p, var_p)
        refactorings = decode_gene(gene, encoder)
        paths = dict()
        paths["owners"] = owners_p
        paths["pr"] = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/csv/pullrequest.csv"
        ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths)
        res.append(ref_sequence)
        # for each in ref_sequence:
        #     print(each["reviewers"])
        # print(sum(each["collaboration_score"] for each in ref_sequence)/len(ref_sequence))
    return res


def trans_NRE_valkyrie(repo_name, algorithm):
    st = SearchTechnique()
    json_file_path = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/csv/abs.json"
    abs = st.load_repository(json_file=json_file_path, exclude_test=True, exclude_anonymous=True)
    fun_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/FUN.{algorithm}NRE"
    var_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/VAR.{algorithm}NRE"
    owners_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/csv/owners.csv"
    funs = top_k(fun_p, 5)
    res = []
    for fun in funs:
        abs_temp = deepcopy(abs)
        encoder = encode_abs(abs_temp)
        gene = get_genes(fun, fun_p, var_p)
        refactorings = decode_gene(gene, encoder)
        paths = dict()
        paths["owners"] = owners_p
        paths["pr"] = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo_name}/csv/pullrequest.csv"
        ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths)
        res.append(ref_sequence)
        # for each in ref_sequence:
        #     print(each["reviewers"])
        # print(sum(each["collaboration_score"] for each in ref_sequence)/len(ref_sequence))
    return res


# calculate the review effort for FUN.xxNRE and store in FUN.xxNRE_a
def build_NRE_a(fun_p, var_p, info_p):
    def write_NRE_a(path, lines):
        with open(path, "w") as f:
            f.writelines(lines)

    st = SearchTechnique()
    abs = st.load_repository(json_file=info_p["abs"], exclude_test=True, exclude_anonymous=True)
    with open(fun_p) as f:
        data = f.readlines()
    res = []
    for row in data:
        abs_temp = deepcopy(abs)
        encoder = encode_abs(abs_temp)
        gene = get_genes(row, fun_p, var_p)
        refactorings = decode_gene(gene, encoder)
        paths = dict()
        paths["owners"] = info_p["owner"]
        paths["pr"] = info_p["pr"]
        ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths)
        collaboration_score = sum(ref["collaboration_score"] for ref in ref_sequence)
        if len(ref_sequence) != 0:
            collaboration_score = collaboration_score / len(ref_sequence)
        row = row.strip() + f" -{collaboration_score} \n"
        res.append(row)
    write_NRE_a(fun_p + "_a", res)
    print(f"build {fun_p}_a finished")


def deduce_reviewers(fun_p, var_p, info_p):
    st = SearchTechnique()
    abs = st.load_repository(json_file=info_p["abs"], exclude_test=True, exclude_anonymous=True)
    with open(fun_p) as f:
        data = f.readlines()
    res = []
    for row in data:
        abs_temp = deepcopy(abs)
        encoder = encode_abs(abs_temp)
        gene = get_genes(row, fun_p, var_p)
        refactorings = decode_gene(gene, encoder)
        paths = dict()
        paths["owners"] = info_p["owner"]
        paths["pr"] = info_p["pr"]
        ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths)
        res.append(ref_sequence["reviewer"])
    return res


if __name__ == "__main__":
    # root = "/Users/leichen/experiement_result/MORCoRE2/1st_test_output/*"
    # import glob
    # res = glob.glob(root)
    # print([each.split("/")[-1] for each in res])
    repos = ['UltimateRecyclerView', 'ActiveAndroid', 'auto', 'HikariCP',
             'dagger', 'fresco', 'quasar', 'guice', 'ActionBarSherlock',
             'AndroidAsync', 'mockito']
    repo = "ActiveAndroid"

    for repo in repos:
        for algorithm in ["Nsga3", "Nsgaii"]:
            re = get_RE_collaboration_valkyrie(repo, algorithm)
            re = [-1 * each for each in re]
            nre = trans_NRE_valkyrie(repo, algorithm)
            nre_l = []
            for ref_seq in nre:
                nre_l.append(sum(ref["collaboration_score"] for ref in ref_seq) / len(ref_seq))
                # print(sum(ref["collaboration_score"] for ref in ref_seq)/len(ref_seq))
            pvalue = ttest_ind(re, nre_l).pvalue
            if pvalue < 0.05:
                print(f"{repo} with {algorithm} is Significant difference")
