def dataset_table_row(name, repo_dict):
    repo=repo_dict[name]
    res = repo["name"] + " & " + str(repo["classes"]) + " & " \
          + str(repo["commits"]) + " & " + str(repo["prs"]) +" & " + str(repo["iterations"])+ r"\\ \hline"
    return res


def repo_dict():
    repo_dict = {}
    repo_dict["HikariCP"] = {"name": "HikariCP", "classes":65, "commits":2826, "prs":381, 'iterations':20000}
    repo_dict["dagger"] = {"name": "dagger", "classes": 77, "commits": 703, "prs": 293, 'iterations':22000}
    repo_dict["auto"] = {"name": "auto", "classes": 225, "commits": 1519, "prs": 932, 'iterations':25000}
    repo_dict["UltimateRecyclerView"] = {"name": "UltimateRecyclerView", "classes": 239, "commits": 764, "prs": 109, 'iterations':45000}
    repo_dict["AndroidAsync"] = {"name": "AndroidAsync", "classes": 262, "commits": 1095, "prs": 142, 'iterations':46000}
    repo_dict["ActionBarSherlock"] = {"name": "ActionBarSherlock", "classes": 314, "commits": 1480, "prs": 253, 'iterations':48000}
    repo_dict["mockito"] = {"name": "mockito", "classes": 513, "commits": 5822, "prs": 1412, 'iterations':80000}
    repo_dict["guice"] = {"name": "guice", "classes": 570, "commits": 2024, "prs": 509, 'iterations':82000}
    repo_dict["quasar"] = {"name": "quasar", "classes": 611, "commits": 2494, "prs": 67, 'iterations':89000}
    repo_dict["fresco"] = {"name": "fresco", "classes": 841, "commits": 3413, "prs": 410, 'iterations':110000}
    return repo_dict


if __name__ == "__main__":
    rd = repo_dict()
    for repo in repo_dict().keys():
        res = dataset_table_row(repo, rd)
        print(res)

