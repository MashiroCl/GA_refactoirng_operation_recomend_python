'''
Experiment running environment
{
Local: MacBook,
Titan: server titan,
}
'''
from call_graph.CallGraph import CallGraph
from code_ownership.DeveloperGraph import DeveloperGraph
from code_ownership.PullRequestService import PullRequestService
from collaboration.graph import Graph
from expertise.build_table import load_expertise_table, WorkloadExpertise
from workload.workload import load_workload


class Platform:
    def __init__(self):
        self.name = "platform"
        self.repo_name = ""
        self.json_file_path = ""
        self.output_path = ""
        # developers collaboration
        # self.collaboration_csv_path = ""
        # self.ownership_path = ""
        self.repo_path = ""
        self.call_graph_path = ""

        # expertise_workload
        self.workload_table_path = ""
        self.expertise_table_path = ""

    def __str__(self):
        return f"name:{self.name}\n" \
               f"json file path:{self.json_file_path}\n" \
               f"output path:{self.output_path}\n" \
               f"workload_table path:{self.workload_table_path}\n" \
               f"expertise_table path:{self.expertise_table_path}\n" \
               f"repository path:{self.repo_path}\n" \
               f"call graph csv file path:{self.call_graph_path}"
        # f"relationship csv path:{self.collaboration_csv_path}\n" \
        # f"ownership csv file path:{self.ownership_path}\n" \

    def set_repository(self, repo_name):
        '''
        Set repository path in paths of platform
        '''
        self.repo_name = repo_name

    def load_call_graph(self) -> CallGraph:
        return CallGraph(self.call_graph_path, self.repo_name)

    # def old_load_developer_graph(self) -> DeveloperGraph:
    #     pullrequests = PullRequestService().loadPullRequest(self.collaboration_csv_path)
    #     return DeveloperGraph(pullrequests).generate_vertices().build()
    #
    # def load_developer_graph(self) -> Graph:
    #     g = Graph()
    #     csv_path = self.collaboration_csv_path
    #     g.build_from_csv(csv_path)
    #     return g

    def load_workload_expertise(self) -> WorkloadExpertise:
        return WorkloadExpertise(load_expertise_table(self.expertise_table_path),
                                 load_workload(self.workload_table_path))


class LocalPlatform(Platform):
    def __init__(self):
        super().__init__()
        self.name = "local"

    def set_repository(self, repo_name):
        self.repo_name = repo_name
        self.json_file_path = "/Users/leichen/experiement_result/MORCoRA/infos/" + repo_name + "/csv/abs.json"
        self.repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo_name
        self.output_path = "/Users/leichen/Desktop/output/"
        self.expertise_table_path = "/Users/leichen/experiement_result/MORCoRA/infos/" + repo_name + "/csv/expertise_table.csv"
        self.workload_table_path = "/Users/leichen/experiement_result/MORCoRA/infos/" + repo_name + "/csv/workload_table.json"
        # self.collaboration_csv_path = "/Users/leichen/experiement_result/MORCoRA/infos/" + repo_name + "/csv/pullrequest.csv"
        # self.ownership_path = "/Users/leichen/experiement_result/MORCoRA/infos/" + repo_name + "/csv/owners.csv"
        self.call_graph_path = "/Users/leichen/experiement_result/MORCoRA/infos/" + repo_name + "/csv/call.json"


class TitanPlatform(Platform):
    def __init__(self):
        super().__init__()
        self.name = "titan"

    def set_repository(self, repo_name):
        root = "/home/salab/chenlei/MORCoRA/dataset/"
        self.repo_name = repo_name
        self.json_file_path = root + repo_name + "/csv/abs.json"
        self.repo_path = root + repo_name
        self.output_path = root + repo_name + "/output/"
        self.expertise_table_path = root + repo_name + "/csv/expertise_table.csv"
        self.workload_table_path = root + repo_name + "/csv/workload_table.json"
        self.call_graph_path = root + repo_name + "/csv/call.json"


class ValkyriePlatform(Platform):
    def __init__(self):
        self.name = "valkyrie"

    def set_repository(self, repo_name):
        root = ""
        self.repo_name = repo_name
        self.json_file_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/csv/abs.json"
        self.repo_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name
        self.output_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/output/"
        self.expertise_table_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/csv/expertise_table.csv"
        self.workload_table_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/csv/workload_table.json"
        # self.collaboration_csv_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/csv/pullrequest.csv"
        # self.ownership_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/csv/owners.csv"
        self.call_graph_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/csv/call.json"


class ThorPlatform(Platform):
    def __init__(self):
        self.name = "thor"

    def set_repository(self, repo_name):
        root = "/home/salab/chenlei/project/MORCoRA/dataset/csv"
        self.repo_name = repo_name
        self.json_file_path = root + repo_name + "/csv/abs.json"
        self.repo_path = root + repo_name
        self.output_path = root + repo_name + "/output/"
        self.expertise_table_path = root + repo_name + "/csv/expertise_table.csv"
        self.workload_table_path = root + repo_name + "/csv/workload_table.json"
        self.call_graph_path = root + repo_name + "/csv/call.json"


class CustomizePlatform(Platform):
    def __init__(self):
        self.name = "customize"

    def set_repository(self, repo_name, root=""):
        with open("config.txt") as f:
            data = f.readlines()
            root = data[0].strip()
        if len(root) == 0:
            raise Exception("Target repository dataset path not set")
        self.repo_name = repo_name
        self.json_file_path = root + repo_name + "/MORCoRE/csv/abs.json"
        self.repo_path = root + repo_name
        self.output_path = root + repo_name + "/MORCoRE/output/"
        self.expertise_table_path = root + repo_name + "/MORCoRE/csv/expertise_table.csv"
        self.workload_table_path = root + repo_name + "/MORCoRE/csv/workload_table.json"
        # self.collaboration_csv_path = root + repo_name + "/MORCoRE/csv/pullrequest.csv"
        # self.ownership_path = root + repo_name + "/MORCoRE/csv/owners.csv"
        self.call_graph_path = root + repo_name + "/MORCoRE/csv/call.json"
