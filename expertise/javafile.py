import subprocess
import os
import json
from typing import List
from expertise.commit import Commit


PRETTY_FORMAT = "--pretty=format:\'{%n  \"commit\": \"%H\",%n \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }%n},\'"


class File:
    def __init__(self, repo_path:str, path: str):
        self.repo_path = repo_path
        self.path = path
        self.name = path.split("/")[-1].split(".")[0]

    # def get_commits(self)->List[Commit]:
    #     command = " ".join(["cd", self.repo_path, "&&", "git", "--no-pager","log", PRETTY_FORMAT, "--follow", self.path])
    #     commits_str = subprocess.getoutput(command)
    #     commits_json = json.loads("["+commits_str.replace("\\", " ")[:-1]+"]")
    #     return [Commit(each) for each in commits_json]

    def get_commits(self)->List[Commit]:
        command = " ".join(["cd", self.repo_path, "&&", "git", "--no-pager","log", PRETTY_FORMAT, "--follow", self.path])
        commits_str = subprocess.getoutput(command)
        commits_json = json.loads("["+commits_str.replace("\\", " ")[:-1]+"]")
        return [Commit(each) for each in commits_json]

    def get_commits_from_json(self):
        git_log_p = os.path.join(self.repo_path, "MORCoRE", self.name+".json")
        with open(git_log_p) as f:
            commits_json = json.loads("["+f.read().replace("\\", " ")[:-1]+"]")
        return [Commit(each) for each in commits_json]

    def commits2csv(self):
        git_log_directory = os.path.join(self.repo_path, "MORCoRE")
        if not os.path.exists(git_log_directory):
            os.mkdir(git_log_directory)
        command = " ".join(["cd", self.repo_path, "&&", "git", "--no-pager","log", PRETTY_FORMAT,
                            "--follow", self.path, ">", os.path.join(git_log_directory, self.name+".json")])
        # command = " ".join(["cd", self.repo_path, "&&", "git", "--no-pager","log", PRETTY_FORMAT, "--follow", self.path])
        commits_str = subprocess.getoutput(command)
        # with open(os.path.join(git_log_directory, self.name+".json"),"w") as f:
        #     json.dump(("["+commits_str.replace("\\", " ")[:-1]+"]"),f)

