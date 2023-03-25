import argparse, os, datetime
from expertise.ownership import get_repo_ownership_t, extract_owners, get_repo_ownership_t_without_similar_files
from collaboration.collaboration import get_pr_history
from jxplatform2.Jxplatform2 import extract_abs, extract_call_graph
from utils.directory import mkdir
from expertise.build_table import build_expertise_table, load_expertise_table
from workload.workload import cal_workload, get_workload_dict, store_workload, load_workload
from search_technique.Nsga3RE import Nsga3RE
from search_technique.Nsga3NRE import Nsga3NRE
from search_technique.NsgaiiRE import NsgaiiRE
from search_technique.NsgaiiNRE import NsgaiiNRE
from search_technique.spea2re import SPEA2RE
from search_technique.spea2nre import SPEA2NRE
from search_technique.ibeare import IBEARE
from search_technique.ibeanre import IBEANRE
from search_technique.mocellre import MOCellRE
from search_technique.mocellnre import MOCellNRE
from search_technique.RandomSearchRE import RandomSearchRE


def command_line():
    parser = argparse.ArgumentParser(
        description="MORCoRE: Multi-objective refactoring recommendation considering review effort")
    parser.add_argument("-e", "--expertise", help="extract expertise for <repository_path> and output in <csv_path>")
    parser.add_argument("-i", "--input", help="<repository_path>")
    parser.add_argument("-o", "--output", help="<csv_path>")
    parser.add_argument("-c", "--collaboration",
                        help="extract collaboration history for <repository_path> and output in <csv_path>")

    return parser.parse_args()


def command_extract():
    parser = argparse.ArgumentParser(description="Extract info for MORCoRE")
    parser.add_argument("-r", help="repo path")
    parser.add_argument("-u", help="repo url")
    parser.add_argument("-n", help="repo name")
    parser.add_argument("-i", help="maximum evaluations")
    parser.add_argument("-p", help="platform")
    parser.add_argument("-m", help="mode")
    parser.add_argument("-d", help="output num", default=1)
    return parser.parse_args()


def functions(args):
    if args.e is not None:
        get_repo_ownership_t(args.i, args.o)
    elif args.e is not None:
        get_pr_history(args.i)
        get_repo_ownership_t(args.i, args.o)


def extract_expertise(repo_p, output_directory):
    ownership_p = output_directory + "ownerships.csv"
    owners_p = output_directory + "owners.csv"
    # extract ownerships consider similar files
    # get_repo_ownership_t(repo_p, ownership_p)
    get_repo_ownership_t_without_similar_files(repo_p, ownership_p)
    # extract owners
    with open(owners_p, "w") as f:
        extract_owners(ownership_p, f)


def extract_collaboration(repo_url, output_directory):
    pullrequest_p = output_directory + "pullrequest.csv"
    # extract pull requests
    get_pr_history(repo_url, pullrequest_p)


def extract_repo_model(jxplatform, repo_p, output_directory):
    abs_p = output_directory + "abs.json"
    call_p = output_directory + "call.json"
    # extract abstract representation
    extract_abs(jxplatform, repo_p, abs_p)
    # extract call graph
    extract_call_graph(jxplatform, repo_p, call_p)


def extract_workload_expertise(repo_path, repo_url, csv_p, end_point, period):
    build_expertise_table(repo_path, csv_p + "expertise_table.csv")
    expertise_table = load_expertise_table(csv_p + "expertise_table.csv")
    reviewers = expertise_table['Unnamed: 0'].tolist()
    workload = cal_workload(repo_url, end_point, period)
    store_workload(workload, csv_p + "temporary_workload.json")
    # Manually unifying the names
    input(f"Please unify the names in workload table {csv_p + 'temporary_workload.json'}, after unification, press enter")
    d = get_workload_dict(load_workload(csv_p + "temporary_workload.json"), reviewers)
    store_workload(d, csv_p + "workload_table.json")

def extract(args):
    jxplatform = "jxplatform2/arExtractor.jar"

    repo_p = args.r
    repo_url = args.u

    MORCoRE_output = os.path.join(repo_p, "MORCoRE")
    csv_p = os.path.join(MORCoRE_output, "csv/")
    output_p = os.path.join(MORCoRE_output, "output/")
    mkdir(MORCoRE_output)
    mkdir(csv_p)
    mkdir(output_p)

    print(f"Extracting repository model for {repo_p}")
    extract_repo_model(jxplatform, repo_p, csv_p)
    print(f"Finished extracting repository model for {repo_p}")

    print(f"Extracting expertise_workload model for {repo_p}")
    end_point = datetime.datetime(2023, 3, 18)
    period = datetime.timedelta(days=7)
    extract_workload_expertise(repo_p, repo_url, csv_p, end_point, period)
    print(f"Finished extracting expertise_workload model for {repo_p}")

    # print(f"Extracting expertise for {repo_p}")
    # extract_expertise(repo_p, csv_p)
    # print(f"Finished extracting expertise for {repo_p}")

    # print(f"Extracting collaboration for {repo_p}")
    # extract_collaboration(repo_url, csv_p)
    # print(f"Finished extracting collaboration for {repo_p}")


def search(args):
    repo_name = args.n
    max_evaluations = args.i
    platform = args.p
    root_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt"

    for output_num in range(1, 6):
        MORCoRE_output = os.path.join(root_path, repo_name, "MORCoRE")
        output_p = os.path.join(MORCoRE_output, f"output{output_num}/")
        mkdir(output_p)

    for output_num in range(1, 6):
        nsga3RE = Nsga3RE()
        nsga3NRE = Nsga3NRE()
        nsgaiiRE = NsgaiiRE()
        nsgaiiNRE = NsgaiiNRE()
        randomSearchRE = RandomSearchRE()

        nsga3RE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(
            output_num).search().write_result()
        nsga3NRE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(
            output_num).search().write_result()
        nsgaiiRE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(
            output_num).search().write_result()
        nsgaiiNRE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(
            output_num).search().write_result()
        randomSearchRE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(
            output_num).search().write_result()


def search_with_output_num(args):
    repo_name = args.n
    max_evaluations = args.i
    platform = args.p
    output_num = args.d

    algorithms = [
                # Nsga3RE(),
                #   Nsga3NRE(),
                  NsgaiiRE(),
                  NsgaiiNRE(),
                  RandomSearchRE(),
                  SPEA2RE(),
                  # SPEA2NRE(),
                  IBEARE(),
                  # IBEANRE(),
                  MOCellRE(),
                  # MOCellNRE()
                  ]

    for algorithm in algorithms:
        algorithm.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(
            output_num).search().write_result()


def search_titan(args):
    root_path = "/home/chenlei/MORCoRA/dataset/"
    repo_name = args.n
    for num in range(1, 6):
        MORCoRE_output = os.path.join(root_path, repo_name)
        output_p = os.path.join(MORCoRE_output, f"output{num}/")
        mkdir(output_p)

    search_with_output_num(args)


def search_thor(args):
    root_path = "/home/salab/chenlei/project/MORCoRA/dataset/"
    repo_name = args.n
    for num in range(1, 6):
        MORCoRE_output = os.path.join(root_path, repo_name)
        output_p = os.path.join(MORCoRE_output, f"output{num}/")
        mkdir(output_p)

    search_with_output_num(args)


def search_customize(args):
    with open("config.txt") as f:
        data = f.readlines()
        root_path = data[0].strip()
    repo_name = args.n
    output_num = args.d + 1
    for num in range(1, output_num):
        MORCoRE_output = os.path.join(root_path, repo_name)
        output_p = os.path.join(MORCoRE_output, f"output{num}/")
        mkdir(output_p)

    search_with_output_num(args)


if __name__ == "__main__":
    args = command_extract()
    # extraction mode
    if args.m == 'extract':
        extract(args)
    # search mode
    elif args.m == 'search':
        search(args)
    elif args.m == 'search_titan':
        search_titan(args)
    elif args.m == 'search_thor':
        search_thor(args)
    elif args.m == 'search_customize':
        search_customize(args)
