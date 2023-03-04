from typing import List
from javamodel.JClass import JClass
from javamodel.jVariable import jVariable


class NameExtractor():
    """
    Extractor extract names from source code elements
    """

    def __init__(self):
        pass

    def parse_camel_style(self, name: str):
        left, right = 0, 0
        res = []
        while left <= right and right < len(name):
            if name[right].isupper() and right > 0:
                res.append(name[left:right])
                left = right
            right += 1
        if left < right:
            res.append(name[left:right])
        return res

    def parse_camel_style_list_words(self, names: List[str]):
        res = []
        for each in names:
            res += self.parse_camel_style(each)
        return res

    def extract_names(self, jclass: JClass):
        return self.__extract_class_name(jclass), \
               self.__extract_method_names(jclass), \
               self.__extract_parameters_names(jclass), \
               self.__extract_field_names(jclass)

    def __extract_class_name(self, jclass: JClass):
        return jclass.getClassName()

    def __extract_method_names(self, jclass: JClass):
        return [jVariable(each).getName().replace('()', '') for each in jclass.getField()]

    def __extract_parameters_names(self, jclass: JClass):
        return [each.getParameterName() for each in jclass.getMethod()]

    def __extract_field_names(self, jclass: JClass):
        return [jVariable(each).getName() for each in jclass.getField()]

    def __assemble_names(self, class_name, method_names, parameters_names, field_names):
        res = []
        res.append(class_name)
        res += method_names
        for each in parameters_names:
            res += each
        res += field_names
        return res

    def upper_2_lower(self, words: List[str]):
        res = list()
        for each in words:
            res.append(each.lower())
        return res

    def to_sequence(self, words: List[str]):
        return " ".join(words)

    def extract(self, abs_representation: List[JClass]) -> dict:
        """
        projectInfo: list of jClass

        return: {K: repository path +'#'+class name, V: list of names in the class}
        Because one repository may contain multiple classes, we use repository+class name to be the unique key
        """
        raw_names = []
        res = dict()
        "extract"
        for each in abs_representation:
            repo = each.getKey()
            class_name, method_names, parameters_names, field_names = self.extract_names(each)
            names = self.__assemble_names(class_name, method_names, parameters_names, field_names)
            res[repo] = names

        "parse camel style & upper to lower"
        for each in res:
            res[each] = self.parse_camel_style_list_words(res[each])
            res[each] = self.upper_2_lower(res[each])

        return res

    def dict_names_to_dict_sequence(self, names_dict: dict):
        for each in names_dict:
            names_dict[each] = self.to_sequence(names_dict[each])

        return names_dict
