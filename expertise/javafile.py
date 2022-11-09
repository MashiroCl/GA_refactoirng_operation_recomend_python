import subprocess
import json
from typing import List
from expertise.commit import Commit


class File:
    def __init__(self, repo_path:str, path: str):
        self.repo_path = repo_path
        self.path = path
        self.name = path.split("/")[-1]

    def get_commits(self)->List[Commit]:
        prettyFormat = "--pretty=format:\'{%n  \"commit\": \"%H\",%n \"author\": {%n    \"name\": \"%aN\",%n    \"email\": \"%aE\",%n    \"date\": \"%aD\"%n  },%n  \"commiter\": {%n    \"name\": \"%cN\",%n    \"email\": \"%cE\",%n    \"date\": \"%cD\"%n  }%n},\'"
        command = " ".join(["cd", self.repo_path, "&&", "git", "--no-pager","log", prettyFormat, "--follow", self.path])
        commits_str = subprocess.getoutput(command)
        commits_json = json.loads("["+commits_str.replace("\\", " ")[:-1]+"]")
        return [Commit(each) for each in commits_json]

