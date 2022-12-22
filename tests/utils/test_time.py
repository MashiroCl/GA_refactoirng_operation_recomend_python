import unittest
from utils.time import format_committime, format_prtime
from datetime import date


class MyTestCase(unittest.TestCase):
    def test_format_committime(self):
        t = "Thu, 30 Mar 2017 10:44:25 -0700"
        self.assertEqual(date(2017,3,30), format_committime(t))

    def test_format_prtime(self):
        t = "2021-05-15T13:34:55Z"
        self.assertEqual("2021-05-15", format_prtime(t))
