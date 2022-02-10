from encoding.IntegerEncoding import IntegerEncoding
from utils import readJson
from jxplatform2.jClass import jClass
class GeneTranslater:
    """
    translate gene sequence into refactoring operations.

    Translate gene sequence into RO sequences according to encoding rules.
    """
    def __init__(self,genes:str):
        self.genes = genes

    def translate(self, projectInfo):
        e = IntegerEncoding()
        e.encoding(projectInfo)
        decoded_sequences = e.decoding(self.genes)
        i=0
        res = list()
        filed_and_method = ['class1field', 'class1method', 'class2field', 'class2method']
        for each in decoded_sequences:
            if not (each['class1field']==None and each['class1method']==None and \
                    each['class2field']==None and each['class2method']==None):
                res.append(each['ROType'])
                res.append(each['class1'].classInfo)
                res.append(each['class1'].filePath)
                res.append(each['class2'].classInfo)
                res.append(each['class2'].filePath)
                for i in filed_and_method:
                    if not each[i]==None:
                        res.append(each[i])
        print(res)
        i=0
        while i <len(res):
            print(res[i:i+6])
            i=i+6

genes = "4 24 48 16 2 198 4 8 6 100 243 16 8 2 248 3 7 28 251 15 5 244 148 1 7 2 226 3 2 95 122 1 7 129 232 3 3 89 3 1 2 203 197 4 1 184 241 3 6 230 124 15 5 55 104 10 5 7 2 2 3 29 251 4 5 167 20 5 7 65 1 16 4 126 6 16 1 173 18 1"
genes = [int(each) for each in genes.split(" ")]
jsonFileRTE = "/Users/leichen/Desktop/mbassador.json"
load = readJson(jsonFileRTE)
jClist = []
for each in load:
    javaClass = jClass(each)
    # if not javaClass.testClass:
    jClist.append(javaClass)
GeneTranslater(genes).translate(jClist)

