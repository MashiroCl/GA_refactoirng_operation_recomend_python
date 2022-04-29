import unittest
import sys
sys.path.append("../")
from search_technique.NSGAIIInteger import load_repository
from jxplatform2.jVariable import jVariable

class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.jsonFile = "mbassador.json"

    def test_load_repository_exclude_test_classes(self):
        res = load_repository(jsonFile=self.jsonFile, exclude_test=True, exclude_anonymous=False)
        self.assertEqual(92, len(res))

    def test_load_repository_not_exclude_test_classes(self):
        res = load_repository(jsonFile=self.jsonFile, exclude_test=False)
        self.assertEqual(255, len(res))

    def test_check_elements_in_jclass(self):
        res = load_repository(jsonFile=self.jsonFile, exclude_test=True, exclude_anonymous=True)
        print(f"class name:{res[0].getClassName()},"
              f"\n repository path:{res[0].getFilePath()},"
              f"\n field names:{[jVariable(each).getName() for each in res[0].getField()]},"
              f"\n method names:{[each.getName() for each in res[0].getMethod()]},"
              f"\n parameters names:{[each.getParameterName() for each in res[0].getMethod()]}")


if __name__ == '__main__':
    unittest.main()
