from typing import List
from expertise.repository import Repository
from expertise.commit import Commit
from expertise.javafile import File as JavaFile


class PersonalOwnership:
    def __init__(self, file_path, author, ownership):
        self.file_path = file_path
        self.author = author
        self.ownership = ownership

    def __str__(self):
        return f"path:{self.file_path}, author:{self.author}, ownership:{self.ownership}"

    def tolist(self):
        return [self.file_path,self.author,self.ownership]


def get_file_ownership(file: JavaFile)->List[PersonalOwnership]:
    commits = file.get_commits()
    n = len(commits)
    ownership = []
    author_com_num_dict = dict()
    for commit in commits:
        author_com_num_dict[commit.author_name] = author_com_num_dict.get(commit.author_name, 0) + 1
    for author in author_com_num_dict.keys():
        ownership.append(PersonalOwnership(file.path, author, author_com_num_dict[author] / n))
    return ownership
