import unittest
from dataanalyse.rq1 import aggregate_top_k_from_outputs

class MyTestCase(unittest.TestCase):
    def test_aggregate_data_HikariCP_top5(self):
        repo_name = "HikariCP"
        file = "FUN.Nsga3RE"
        res = aggregate_top_k_from_outputs(repo_name, file,5)
        self.assertEqual(len(res),5)
        self.assertEqual(len(res[0]),5)


if __name__ == '__main__':
    unittest.main()
