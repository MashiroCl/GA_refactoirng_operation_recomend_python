import unittest
from utils.directory import trim_path


class MyTestCase(unittest.TestCase):
    def test_trim_path_without_extra_parameter(self):
        path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/123.java"
        res = trim_path(path)
        self.assertEqual(res,"/mbassador/123.java")

    def test_trim_path_with_extra_parameter(self):
        path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/123.java"
        res = trim_path(path, "mbassador")
        self.assertEqual(res, "/123.java")



if __name__ == '__main__':
    unittest.main()
