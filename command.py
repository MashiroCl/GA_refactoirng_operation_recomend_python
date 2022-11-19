import argparse
from expertise.ownership import get_repo_ownership_t, extract_owners
from collaboration.collaboration import get_pr_history
from jxplatform2.Jxplatform2 import extract_abs, extract_call_graph

def command_line():
    parser = argparse.ArgumentParser(description="MORCoRE: Multi-objective refactoring recommendation considering review effort")
    parser.add_argument("-e", "--expertise", help = "extract expertise for <repository_path> and output in <csv_path>")
    parser.add_argument("-i", "--input", help = "<repository_path>")
    parser.add_argument("-o", "--output", help = "<csv_path>")
    parser.add_argument("-c","--collaboration", help = "extract collaboration history for <repository_path> and output in <csv_path>")

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


def extract():
    repo_p = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/javapoet"
    repo_url = "https://github.com/square/javapoet"
    output_directory = "/Users/leichen/Desktop/output/temp/"
    jxplatform = "/Users/leichen/Desktop/arExtractor.jar"

    print(f"Extracting repository model for {repo_p}")
    extract_repo_model(jxplatform, repo_p, output_directory)
    print(f"Finished extracting repository model for {repo_p}")

    print(f"Extracting expertise for {repo_p}")
    extract_expertise(repo_p, output_directory)
    print(f"Finished extracting expertise for {repo_p}")

    print(f"Extracting collaboration for {repo_p}")
    extract_collaboration(repo_url, output_directory)
    print(f"Finished extracting collaboration for {repo_p}")



if __name__ == "__main__":
    # args = command_line()
    # functions(args)
    extract()