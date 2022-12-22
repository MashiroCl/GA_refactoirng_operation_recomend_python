import unittest
from semantic.NameExtractor import NameExtractor
import sys
sys.path.append("../")
from search_technique.SearchTechnique import SearchTechnique

class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.nameExtractor = NameExtractor()
        self.json_file = "../mbassador.json"
        self.projectInfo = SearchTechnique().load_repository(json_file=self.json_file, exclude_test=True)

    def test_parse_camel_style_oneTwoThree(self):
        res = self.nameExtractor.parse_camel_style(name="oneTwoThree")
        self.assertEqual(['one', 'Two', 'Three'],res)

    def test_parse_camel_style_ONE(self):
        res = self.nameExtractor.parse_camel_style(name="ONE")
        self.assertEqual(['O', 'N', 'E'],res)

    def test_parse_camel_style_O(self):
        res = self.nameExtractor.parse_camel_style(name="O")
        self.assertEqual(['O'],res)

    def test_parse_camel_style_null(self):
        res = self.nameExtractor.parse_camel_style(name="")
        self.assertEqual([],res)

    def test_upper_2_lower(self):
        words = ["One", "TWO", "three", "4", ""]
        res = self.nameExtractor.upper_2_lower(words)
        self.assertEqual(["one", "two", "three", "4", ""],res)

    def test_parse_camel_style_list_words(self):
        words = ["One", "TWO", "three", "4", ""]
        res = self.nameExtractor.parse_camel_style_list_words(words)
        self.assertEqual(["One", "T", "W", "O", "three", "4"],res)

    def test_to_sequence(self):
        words = ["Bob", "has", "an", "apple", "Jane", "has", "an", "apple"]
        res = self.nameExtractor.to_sequence(words)
        self.assertEqual("Bob has an apple Jane has an apple",res)

    def test_extract(self):
        res = self.nameExtractor.extract(abs_representation=self.projectInfo)
        self.assertEqual(
            ['subscription', 'id', 'listeners', 'dispatcher', 'context', 'on','subscription', 'subscription','by','priority','desc',
             'context', 'dispatcher', 'listeners', 'listener', 'listener', 'message','type', 'publication', 'message', 'o',
             'existing','listener', 'id', 'listeners', 'dispatcher', 'context', 'on','subscription', 'subscription','by','priority','desc'],
                         res['/mbassador/src/main/java/net/engio/mbassy/subscription/Subscription.java#Subscription'])

    def test_dict_names_to_dict_sequence(self):
        res = self.nameExtractor.extract(abs_representation=self.projectInfo)
        res = self.nameExtractor.dict_names_to_dict_sequence(res)
        self.assertEqual(['strong concurrent set value next'],res['/mbassador/src/main/java/net/engio/mbassy/common/StrongConcurrentSet.java#StrongConcurrentSet'])