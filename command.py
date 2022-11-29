import argparse, os
from expertise.ownership import get_repo_ownership_t, extract_owners
from collaboration.collaboration import get_pr_history
from jxplatform2.Jxplatform2 import extract_abs, extract_call_graph
from utils.directory import mkdir
from search_technique.Nsga3RE import Nsga3RE
from search_technique.Nsga3NRE import Nsga3NRE
from search_technique.NsgaiiRE import NsgaiiRE
from search_technique.NsgaiiNRE import NsgaiiNRE
from search_technique.RandomSearchRE import RandomSearchRE

def command_line():
    parser = argparse.ArgumentParser(description="MORCoRE: Multi-objective refactoring recommendation considering review effort")
    parser.add_argument("-e", "--expertise", help = "extract expertise for <repository_path> and output in <csv_path>")
    parser.add_argument("-i", "--input", help = "<repository_path>")
    parser.add_argument("-o", "--output", help = "<csv_path>")
    parser.add_argument("-c","--collaboration", help = "extract collaboration history for <repository_path> and output in <csv_path>")

    return parser.parse_args()


def command_extract():
    parser = argparse.ArgumentParser(description="Extract info for MORCoRE")
    parser.add_argument("-r", help="repo path")
    parser.add_argument("-u", help= "repo url")
    parser.add_argument("-n", help="repo name")
    parser.add_argument("-i", help= "maximum evaluations")
    parser.add_argument("-p", help="platform")
    parser.add_argument("-m", help= "mode")
    parser.add_argument("-d", help="output num")
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
    # extract ownerships
    get_repo_ownership_t(repo_p, ownership_p)
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

    print(f"Extracting expertise for {repo_p}")
    extract_expertise(repo_p, csv_p)
    print(f"Finished extracting expertise for {repo_p}")

    print(f"Extracting collaboration for {repo_p}")
    extract_collaboration(repo_url, csv_p)
    print(f"Finished extracting collaboration for {repo_p}")


def search(args):
    repo_name = args.n
    max_evaluations = args.i
    platform = args.p
    root_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt"

    for output_num in range(1,6):
        MORCoRE_output = os.path.join(root_path,repo_name,"MORCoRE")
        output_p = os.path.join(MORCoRE_output, f"output{output_num}/")
        mkdir(output_p)

    for output_num in range(1,6):
        nsga3RE = Nsga3RE()
        nsga3NRE = Nsga3NRE()
        nsgaiiRE = NsgaiiRE()
        nsgaiiNRE = NsgaiiNRE()
        randomSearchRE = RandomSearchRE()

        nsga3RE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(output_num).search().write_result()
        nsga3NRE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(output_num).search().write_result()
        nsgaiiRE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(output_num).search().write_result()
        nsgaiiNRE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(output_num).search().write_result()
        randomSearchRE.load_by_parameter(repo_name, max_evaluations, platform).change_output_path(output_num).search().write_result()

def search_titan(args):
    repo_name = args.n
    max_evaluations = args.i
    platform = args.p
    output_num = args.d
    root_path = "/home/chenlei/MORCoRE/dataset/"

    for num in range(1,6):
        MORCoRE_output = os.path.join(root_path, repo_name)
        output_p = os.path.join(MORCoRE_output, f"output{num}/")
        mkdir(output_p)

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


if __name__ == "__main__":
    args = command_extract()
    # extraction mode
    if args.m=='extract':
        extract(args)
    # search mode
    elif args.m =='search':
        search(args)
    elif args.m =='search_titan':
        search_titan(args)