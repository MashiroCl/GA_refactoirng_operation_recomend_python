from typing import List
from expertise.repository import Repository
from expertise.javafile import File as JavaFile
import utils.csv as csv


class PersonalOwnership:
    def __init__(self, file_path, author, ownership):
        self.file_path = file_path
        self.author = author
        self.ownership = ownership

    def __str__(self):
        return f"path:{self.file_path}, author:{self.author}, ownership:{self.ownership}"

    def tolist(self):
        return [self.file_path, self.author, self.ownership]


def get_file_ownership(file: JavaFile) -> List[PersonalOwnership]:
    commits = file.get_commits()
    n = len(commits)
    ownership = []
    author_com_num_dict = dict()
    for commit in commits:
        author_com_num_dict[commit.author_name] = author_com_num_dict.get(commit.author_name, 0) + 1
    for author in author_com_num_dict.keys():
        ownership.append(PersonalOwnership(file.path, author, author_com_num_dict[author] / n))
    return ownership


def get_repo_ownership(repo_path: str, output_path: str, mode: str = "a"):
    files = Repository(repo_path).get_files()
    with open(output_path, mode, encoding="utf-8") as f:
        for file in files:
            csv.ownership2csv(get_file_ownership(file), f)
