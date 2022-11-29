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


class Platform:
    def __init__(self):
        self.name = "platform"
        self.repo_name = ""
        self.json_file_path = ""
        self.output_path = ""
        # developers collaboration
        self.collaboration_csv_path = ""
        self.ownership_path = ""
        self.repo_path = ""
        self.call_graph_path = ""

    def __str__(self):
        return f"name:{self.name}\n" \
               f"json file path:{self.json_file_path}\n" \
               f"output path:{self.output_path}\n" \
               f"relationship csv path:{self.collaboration_csv_path}\n" \
               f"ownership csv file path:{self.ownership_path}\n" \
               f"repository path:{self.repo_path}\n" \
               f"call graph csv file path:{self.call_graph_path}"

    def set_repository(self, repo_name):
        '''
        Set repository path in paths of platform
        '''
        self.repo_name = repo_name

    def load_call_graph(self) -> CallGraph:
        return CallGraph(self.call_graph_path, self.repo_name)

    def old_load_developer_graph(self) -> DeveloperGraph:
        pullrequests = PullRequestService().loadPullRequest(self.collaboration_csv_path)
        return DeveloperGraph(pullrequests).generate_vertices().build()

    def load_developer_graph(self) -> Graph:
        g = Graph()
        csv_path = self.collaboration_csv_path
        g.build_from_csv(csv_path)
        return g


class LocalPlatform(Platform):
    def __init__(self):
        self.name = "local"

    def set_repository(self, repo_name):
        self.repo_name = repo_name
        self.json_file_path = "/Users/leichen/Desktop/StaticalAnalysis/" + repo_name + ".json"
        self.repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo_name
        self.output_path = "/Users/leichen/Desktop/output/"
        self.collaboration_csv_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo_name + "/MORCOoutput/csv/pullrequest.csv"
        self.ownership_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo_name + "/MORCOoutput/csv/owners.csv"
        self.call_graph_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo_name + "/MORCOoutput/csv/callgraph.json"


class TitanPlatform(Platform):
    def __init__(self):
        self.name = "titan"

    def set_repository(self, repo_name):
        # self.repo_name = repo_name
        # self.json_file_path = "/home/chenlei/MORCO/extractResult/" + repo_name + ".json"
        # self.repo_path = "/home/chenlei/MORCO/data/" + repo_name
        # self.output_path = "/home/chenlei/MORCO/output_temp/"
        # self.collaboration_csv_path = "/home/chenlei/MORCO/relationship/" + repo_name + "/pullrequest.csv"
        # self.ownership_path = "/home/chenlei/MORCO/relationship/" + repo_name + "/owners.csv"
        # self.call_graph_path = "/home/chenlei/MORCO/relationship/" + repo_name + "/callgraph.json"
        root = "/home/chenlei/MORCoRE/dataset/"
        self.repo_name = repo_name
        self.json_file_path = root + repo_name + "/csv/abs.json"
        self.repo_path = root + repo_name
        self.output_path = root + repo_name+"output/"
        self.collaboration_csv_path = root + repo_name + "/csv/pullrequest.csv"
        self.ownership_path = root + repo_name + "/csv/owners.csv"
        self.call_graph_path = root + repo_name + "/csv/call.json"




class ValkyriePlatform(Platform):
    def __init__(self):
        self.name = "valkyrie"

    def set_repository(self, repo_name):
        self.repo_name = repo_name
        self.json_file_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/csv/abs.json"
        self.repo_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name
        self.output_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/output/"
        self.collaboration_csv_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/csv/pullrequest.csv"
        self.ownership_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/csv/owners.csv"
        self.call_graph_path = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt/" + repo_name + "/MORCoRE/csv/call.json"


class ThorPlatform(Platform):
    def __init__(self):
        self.name = "thor"

    def set_repository(self, repo_name):
        self.repo_name = repo_name
        root = "/home/salab/chenlei/project/MORCoRE/dataset/"
        self.json_file_path = root + repo_name + "/csv/abs.json"
        self.repo_path = root + repo_name
        self.output_path = root + repo_name+"/"
        self.collaboration_csv_path = root + repo_name + "/csv/pullrequest.csv"
        self.ownership_path = root + repo_name + "/csv/owners.csv"
        self.call_graph_path = root + repo_name + "/csv/call.json"