from typing import List
from expertise.repository import Repository
from expertise.javafile import File as JavaFile
import utils.csv as csv_utils
import csv
from datetime import date

JACCARD_THRESHOLD = 0.8
BASE_LINE = date(2008, 12, 24)
DEAD_LINE = date(2022, 12, 24)

LOCAL_FILE_PATH = "/Users/leichen/ResearchAssistant/InteractiveRebase/data"


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


def get_file_ownership_t(file: JavaFile, similar_files: List[JavaFile]) -> List[PersonalOwnership]:
    """
    calculate the ownerships for authors in a file considering the commit time factor
    param
        files: files having similar paths with the 1st parameter file
    """
    authors = set([commit.author_name for commit in file.get_commits_from_json()])
    return [get_rev_file_ownership(file, each_author, similar_files) for each_author in authors]


def get_rev_file_ownership(file: JavaFile, reviewer: str, similar_files: List[JavaFile]) -> PersonalOwnership:
    def time_factor(commit):
        return (commit.time - BASE_LINE) / (DEAD_LINE - BASE_LINE)

    ownership = 0
    for each in similar_files:
        for commit in each.get_commits_from_json():
            if commit.author_name == reviewer:
                ownership += time_factor(commit)
    return PersonalOwnership(file.path, reviewer, ownership)


def search_similar_files(file: JavaFile, files: List[JavaFile]):
    similar_files = []
    for each in files:
        if jaccard(file.path, each.path) >= JACCARD_THRESHOLD:
            similar_files.append(each)
    return similar_files


def jaccard(path1: str, path2: str):
    p1_set = set(path1.split("/"))
    p2_set = set(path2.split("/"))
    return len(p1_set.intersection(p2_set)) / len(p1_set.union(p2_set))


def trim_path(po: PersonalOwnership):
    if LOCAL_FILE_PATH in po.file_path:
        po.file_path = po.file_path.split(LOCAL_FILE_PATH)[1]
    return po


def get_repo_ownership(repo_path: str, output_path: str, mode: str = "a"):
    files = Repository(repo_path).get_files()
    with open(output_path, mode, encoding="utf-8") as f:
        for file in files:
            csv_utils.ownership2csv(get_file_ownership(file), f)


def get_repo_ownership_t(repo_path: str, output_path: str, mode: str = "a"):
    files = Repository(repo_path).get_files()
    # build git log json
    for file in files:
        file.commits2csv()
    with open(output_path, mode, encoding="utf-8") as f:
        for file in files:
            similar_files = search_similar_files(file, files)
            pos = get_file_ownership_t(file, similar_files)
            for po in pos:
                trim_path(po)
            csv_utils.ownership2csv(pos, f)


def extract_owners(csv_path: str, output_file: 'File'):
    '''
    find the owners in one java file and export them into another csv
    :param :
    :return:
    '''

    def extract_csv() -> List[List[str]]:
        with open(csv_path, "r") as f:
            data = f.readlines()
            lines = []
            for each in data:
                csv_row = []
                for column in each.split(","):
                    csv_row.append(column.strip())
                lines.append(csv_row)
        return lines

    def select_owners(candidates: List[List[str]]) -> List[PersonalOwnership]:
        '''
        select owners who has the highest/ 2nd highest ownership on the file.
        candidates: ownerships of contributors to the file (candidates[0][0]) in the format of CSV_HEAD
        '''
        candidates.sort(key=lambda x: float(x[2]), reverse=True)
        if len(candidates) < 2:
            return [PersonalOwnership(candidates[0][0], candidates[0][1], candidates[0][2])]
        # todo: discuss need of threshold
        # elif float(candidates[0][2]) - float(candidates[1][2]) < OWNERSHIP_THRESHOLD:
        return [PersonalOwnership(candidates[0][0], candidates[0][1], candidates[0][2]),
                PersonalOwnership(candidates[1][0], candidates[1][1], candidates[1][2])]

    csv_lines = extract_csv()
    owners = []
    row = 1
    while row < len(csv_lines):
        if row < len(csv_lines):
            cur_file_path = csv_lines[row][0]
            candidates = []
            while row < len(csv_lines) and cur_file_path == csv_lines[row][0]:
                candidates.append(csv_lines[row])
                row += 1
            owners += select_owners(candidates)
    csv_utils.ownership2csv(owners, output_file)


def get_path_owner_dict(owners_path: str):
    '''
    key: file_path, value: owner/owners
    '''
    res = dict()
    with open(owners_path) as f:
        reader = csv.reader(f)
        for row in reader:
            res.setdefault(row[0], list()).append(row[1])
    return res

