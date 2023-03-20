import unittest
from workload.workload import *

from workload.workload import get_issue_participants


class MyUnitTest(unittest.TestCase):
    def test_get_issue_participants_HikariCP(self):
        url = "https://github.com/brettwooldridge/HikariCP"
        get_issue_participants(url, 1, 1)

    def test_get_pullrequests_participants_mockito(self):
        url = "https://github.com/mockito/mockito"
        end_point = datetime.datetime(2023, 3, 18)
        period = datetime.timedelta(days=7)
        get_pullrequest_participants(url, end_point, period)

    def test_cal_workload(self):
        url = "https://github.com/mockito/mockito"
        end_point = datetime.datetime(2023, 3, 18)
        period = datetime.timedelta(days=7)
        workload = cal_workload(url, end_point, period)
        print(workload)

    def test_store_workload(self):
        path = "./workload.json"
        url = "https://github.com/mockito/mockito"
        end_point = datetime.datetime(2023, 3, 19)
        period = datetime.timedelta(days=7)
        workload = cal_workload(url, end_point, period)
        store_workload(workload, path)

    def test_append_pair_workload(self):
        path = "./workload.json"
        workload = load_workload(path)
        res = append_pair_workload(workload)
        print(res)

    def test_load_workload(self):
        path = "./workload.json"
        res = load_workload(path)
        print(res)

    def test_filter_by_workload(self):
        path = "./workload.json"
        workload = load_workload(path)
        reviewers = {'Tim van der Lippe': 100, 'krzyk': 50, 'robertotru': 25}
        res = filter_by_workload(2, workload, reviewers)
        print(res)


    def test_get_workload_dict(self):
        from expertise.build_table import load_expertise_table
        path = "/Users/leichen/Code/pythonProject/pythonProject/salabResearch/tests/expertise/expertise_table.csv"
        expertise_table = load_expertise_table(path)
        reviewers = expertise_table['Unnamed: 0'].tolist()

        # url = "https://github.com/mockito/mockito"
        # end_point = datetime.datetime(2023, 3, 18)
        # period = datetime.timedelta(days=7)
        # workload = cal_workload(url, end_point, period)

        workload = {'dependabot[bot]': 8, 'codecov-commenter': 4, 'Tim van der Lippe': 3, 'Roberto Trunfio': 1, 'jfrantzius': 1, 'Rafael Winterhalter': 1, 'PBoddington': 1}
        d = get_workload_dict(workload, reviewers)
        store_workload(d, "./workload.json")
