import csv
from copy import deepcopy
from dataanalyse.rq2 import prepare_path
from search_technique.SearchTechnique import SearchTechnique
from translation.translate import encode_abs, get_genes, decode_gene, trans_decoded_gene

root_path = "/Users/leichen/experiement_result/MORCoRE2/output/"
CSV_HEAD = ["repository", "algorithm", "trial", "rank", "Qual", "Sem", "Collab"]
output_path = "/Users/leichen/experiement_result/MORCoRE2/solution_csv/"


def get_value_refs(repo, algo, output_num, _a=False):
    path = f"{root_path}{repo}/output{output_num}/FUN.{algo}"
    # whether is NRE_a
    if _a:
        path = path + "_a"
    values = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        row = []
        for each in line.strip().split(" "):
            row.append(-1 * float(each))
        values.append(row)
    values = sorted(values, key=lambda x: x[0], reverse=True)

    refs = []
    for each in values:
        if _a:
            each = " ".join([str(-1*v) for v in each][:2])
        else:
            each = " ".join([str(-1*v) for v in each])
        ref = deduce_refs(each, repo, output_num, algo)
        refs.append(ref)
    return values, refs


def build_row(repo, algo, trial, rank, values):
    return [repo, algo, trial, rank] + values


def deduce_refs(values, repo, output_num, algo):
    fun_p, var_p, infos = prepare_path(repo, root_path + repo + f"/output{output_num}/", f"FUN.{algo}",
                                       f"VAR.{algo}")
    st = SearchTechnique()
    abs = st.load_repository(json_file=infos["abs"], exclude_test=True, exclude_anonymous=True)
    abs_temp = deepcopy(abs)
    encoder = encode_abs(abs_temp)
    gene = get_genes(values, fun_p, var_p)
    refactorings = decode_gene(gene, encoder)
    paths = {}
    paths["owners"] = infos["owner"]
    paths["pr"] = infos["pr"]
    ref_sequence = trans_decoded_gene(refactorings, abs_temp, paths, repo)
    return ref_sequence


def get_csv_row(algorithms, _a=False):
    repos = ['HikariCP', 'dagger', 'auto', 'UltimateRecyclerView', 'AndroidAsync',
             'ActionBarSherlock', 'mockito', 'guice', 'quasar', 'fresco']
    # repos = ['HikariCP']
    rows = []
    for repo in repos:
        for algo in algorithms:
            for trial in range(1, 6):
                print(f"Processing {repo} {algo} {trial}...")
                values, refs = get_value_refs(repo, algo, trial, _a)
                for i, v in enumerate(values):
                    row = [repo, algo, trial, i + 1] + v
                    if refs[i]:
                        row = row + refs[i]
                    rows.append(row)
    return rows


def write_rq_csv(csv_name, rows):
    with open(output_path + csv_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEAD)
        writer.writerows(rows)


if __name__ == "__main__":
    # RQ1 results csv
    # algorithms = ["Nsga3RE", "NsgaiiRE", "RandomSearchRE"]
    # rows = get_csv_row(algorithms)
    # write_rq_csv("rq1_results.csv", rows)

    # RQ2 results csv
    algorithms = ["NsgaiiNRE", "Nsga3NRE"]
    rows = get_csv_row(algorithms, _a=True)
    write_rq_csv("rq2_results.csv", rows)

    # dataset csv
    # repos = ['HikariCP', 'dagger', 'auto', 'UltimateRecyclerView', 'AndroidAsync',
    #          'ActionBarSherlock', 'mockito', 'guice', 'quasar', 'fresco']
    # valkyrie_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/"
    #
    # for repo in repos:
    #     command = f'cd {valkyrie_path}{repo} && git log --format="%h" -n 1'
    #     print(command)
