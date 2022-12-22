import unittest
from search_technique.enviroment.Platform import *

class MyTestCase(unittest.TestCase):
    def test_load_platform_no_specification(self):
        p = Platform()
        self.assertEqual(str(p),"name:platform\njson file path:\noutput path:\nrelationship csv_utils path:\nownership csv_utils file path:\nrepository path:\ncall graph csv_utils file path:")

    def test_load_local(self):
        pass

    def test_load_titan(self):
        pass

    def test_hello(self, i):
        for j in range(50):
            print(f"hello {i}")

