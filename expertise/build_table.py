import dataclasses
from typing import List
from expertise.repository import Repository
from expertise.ownership import PersonalOwnership, get_file_expertise_t
import utils.directory as directory
import utils.gitlog as gitlog
import pandas as pd
from workload.workload import filter_by_workload, build_author_pair


def extract_personal_ownerships(repo_path: str) -> List[PersonalOwnership]:
    """
    extract expertise for each contributor in each file
    """
    files = Repository(repo_path).get_files()
    latest_date = gitlog.get_latest_commit_time(repo_path)
    # build git log json
    for file in files:
        file.commits2csv()
    personal_ownerships = []
    for file in files:
        personal_ownership_per_file = get_file_expertise_t(file, latest_date)
        for po in personal_ownership_per_file:
            po.file_path = directory.trim_path(po.file_path)
        personal_ownerships += personal_ownership_per_file
    return personal_ownerships


def extract_authors(personal_ownerships: List[PersonalOwnership]) -> List[str]:
    """
    extract set of authors contained in the PersonalOwnership list
    """
    authors = set()
    for po in personal_ownerships:
        authors.add(po.author)
    return list(authors)


def build_hashmap(personal_ownerships: List[PersonalOwnership]):
    """
    build dict {filepath: {author1:expertise1, author2:expertise2}}
    """
    res = dict()
    # single reviewer
    for each in personal_ownerships:
        res.setdefault(each.file_path, {}).setdefault(each.author, each.ownership)
    # reviewer pairs
    for file_path in res.keys():
        reviewers_with_expertise = res[file_path].keys()
        reviewers_with_expertise = sorted(reviewers_with_expertise)
        for i in range(len(reviewers_with_expertise)):
            for j in range(i + 1, len(reviewers_with_expertise)):
                reviewer_pair = build_author_pair(reviewers_with_expertise[i],
                                                  reviewers_with_expertise[j])
                reviewer_pair_expertise = res[file_path][reviewers_with_expertise[i]] + res[file_path][
                    reviewers_with_expertise[j]]
                res[file_path][reviewer_pair] = reviewer_pair_expertise
    return res


def build_expertise_table(repo_path: str, output_path: str):
    personal_ownerships = extract_personal_ownerships(repo_path)
    hashmap = build_hashmap(personal_ownerships)
    df = pd.DataFrame(hashmap).fillna(0)
    df.to_csv(output_path, sep=",")


def load_expertise_table(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def merge_columns(expertise_table: pd.DataFrame, file_paths: List[str]) -> pd.DataFrame:
    """
    file_paths are the index of columns, and those columns should be merged
    for each row, calculate the sum of those columns, but only if none of the values are zero
    """
    df = expertise_table[file_paths]
    # calculate sum of rows, but only if none of the values in that row are zero
    row_sums = []
    for i, row in df.iterrows():
        if (row == 0).any():
            row_sums.append(0)
        else:
            row_sums.append(row.sum())
    df_row_sums = pd.DataFrame({'row_sums': row_sums})
    return df_row_sums


def merge_columns_by_average(expertise_table: pd.DataFrame, file_paths: List[str]) -> pd.DataFrame:
    """
    file_paths are the index of columns, and those columns should be merged
    for each row, calculate the sum of those columns, but only if none of the values are zero
    """
    df = expertise_table[file_paths]
    # calculate sum of rows, but only if none of the values in that row are zero
    row_sums = []
    for i, row in df.iterrows():
        if (row == 0).any():
            row_sums.append(0)
        else:
            row_sums.append(row.sum()/(len(file_paths)/2))
    df_row_sums = pd.DataFrame({'row_sums': row_sums})
    return df_row_sums

def extract_reviewers_expertise(expertise_table: pd.DataFrame, workload_table: dict, file_paths: List[str],
                                threshold_workload: int = 2, take_average = False) -> dict:
    """
    Extract {reviewer:expertise} dict where reviewer have expertise on the file_paths where and having a workload
    smaller than threshold_workload

    param expertise_table: dataframe for expertise table
    param workload_table: workload table
    param file_paths: file paths where refactorings are applied on
    param threshold: workload threshold
    """
    if take_average:
        merged = merge_columns_by_average(expertise_table, file_paths)
    else:
        merged = merge_columns(expertise_table, file_paths)
    if (merged["row_sums"] == 0).all():
        return dict()
    non_zero_index = expertise_table.index[merged["row_sums"] != 0]
    expertise = merged.iloc[non_zero_index]["row_sums"]
    reviewers = expertise_table.iloc[non_zero_index]['Unnamed: 0']
    reviewer_expertise = \
        pd.DataFrame({"reviewer": reviewers.tolist(), "expertise": expertise.tolist()}).set_index('reviewer')[
            'expertise'].to_dict()
    res = filter_by_workload(threshold_workload, workload_table, reviewer_expertise)
    return res


def get_highest_expertise_reviewer(reviewers_expertise: dict) -> tuple:
    if len(reviewers_expertise) == 0:
        return "No appropriate expertise reviewer", 0
    return max(reviewers_expertise.items(), key=lambda x: x[1])


@dataclasses.dataclass
class WorkloadExpertise:
    expertise_table: pd.DataFrame
    workload_table: dict
