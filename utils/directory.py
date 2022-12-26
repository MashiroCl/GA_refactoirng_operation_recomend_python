import os

LOCAL_FILE_PATH = "/Users/leichen/ResearchAssistant/InteractiveRebase/data"
TITAN_FILE_PATH = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt"
VALKYRIE_FILE_PATH = "/home/chenlei/projects/master_thesis/dataset/mailmapBuilt"


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def trim_path(path: str, *args):
    if LOCAL_FILE_PATH in path:
        path = path.split(LOCAL_FILE_PATH)[1]
    elif VALKYRIE_FILE_PATH in path:
        path = path.split(VALKYRIE_FILE_PATH)[1]
    elif TITAN_FILE_PATH in path:
        path = path.split(TITAN_FILE_PATH)[1]
    else:
        with open("config.txt") as f:
            data = f.readlines()[0].strip()
            if data in path:
                path = path.split(data[:-1])[1]
    if len(args)==1:
        path = path.split(args[0])[1]

    return path
