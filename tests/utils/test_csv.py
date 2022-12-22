import unittest
from expertise.ownership import PersonalOwnership
from utils.csv import ownership2csv


class MyTestCase(unittest.TestCase):

    def test_ownership2csv(self):
        p1 = PersonalOwnership("file_path_1","author1","0.2")
        path="./ownership.csv"
        with open(path,"a",encoding="utf-8") as f:
            ownership2csv([p1],f)