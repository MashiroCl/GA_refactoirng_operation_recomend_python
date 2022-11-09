'''
git repository
'''
import glob
from typing import List
from expertise.javafile import File


class Repository:
    def __init__(self, path: str):
        self.path = path
        self.name = path.split("/")[-1]

    def get_files(self, exclude_tests: bool = True) -> List[File]:
        paths = glob.glob(self.path+"/*/*.java")
        files = []
        for path in paths:
            if exclude_tests:
                if "test" in path or "Test" in path:
                    continue
            files.append(File(path))
        return files
