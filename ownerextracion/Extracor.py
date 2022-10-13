from typing import List
from csv import reader
from multiprocessing import Pool
from pygit2 import clone_repository
import os

NAME_COLUMN_NUMBER = 0
URL_COLUMN_NUMBER = 5


def extract_column(column_num: int) -> List[str]:
    with open("./java.csv") as f:
        r = reader(f)
        return [row[column_num] for row in r][1:]

def clone(url:str, path):
    repo_name = url.split('/')[-1]
    print(f"clone {repo_name} starts",flush=True)
    clone_repository(url,os.path.join(path,repo_name))
    print(f"clone {repo_name} finished",flush=True)

def clone_repostories(url_list: List[str], path: str):
    '''
    url_list: repository urls
    path: local path to clone into
    '''
    pool = Pool()
    pool.starmap(clone, [(url,path)for url in url_list])
    pool.close()
    pool.join()

if __name__ == "__main__":
    url_list = extract_column(URL_COLUMN_NUMBER)
    url_list = ["https://github.com/bennidi/mbassador", "https://github.com/danilofes/refactoring-toy-example", "https://github.com/daimajia/NumberProgressBar"]
    clone_repostories(url_list, "/Users/leichen/东工大课程/2022_3q/technical writing/10.12/123/")
