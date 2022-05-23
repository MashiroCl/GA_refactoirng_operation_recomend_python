import unittest
from git_name_extractor import NameUnifier

class MyTestCase(unittest.TestCase):
    def test_search_name_by_login(self):
        csv_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/retrolambda/MORCOoutput/csv/pullrequest.csv"
        with NameUnifier() as name_unifier:
            login_name_dict = name_unifier.get_login_name_dict(csv_path)
        print(login_name_dict)



if __name__ == '__main__':
    unittest.main()
