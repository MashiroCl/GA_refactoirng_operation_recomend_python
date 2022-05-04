from encoding.IntegerEncoding import IntegerEncoding
from utils import readJson
from jxplatform2.jClass import jClass
from search_technique.NSGAIIInteger import load_repository
from refactoring_operation.RefactoringOperationDispatcher import dispatch
from encoding.IntegerEncoding import IntegerEncoding
from qmood.Qmood import Qmood


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
        initial_objectives =  Qmood().calculateQmood(projectInfo)
        decoded_sequences = e.decoding(self.genes)
        res = list()
        filed_and_method = ['class1field', 'class1method', 'class2field', 'class2method']
        for each in decoded_sequences:
            # Filter refactorings didn't pass preconditions and show only refactorings which can improve quality
            if dispatch(each["ROType"].value)(each, projectInfo):
            #     dispatch(each["ROType"].value)(each, projectInfo)
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
                    res.append(self.calc_quality_gain(projectInfo, initial_objectives))
        i=0
        while i <len(res):
            print(res[i:i+7])
            i=i+7

    @staticmethod
    def find_value_index(target:str, path:str):
        with open(path) as f:
            lines = f.readlines()
        for index,each in enumerate(lines):
            if target.strip()==each.strip():
                return index
        print("No result found")
        return None

    @staticmethod
    def find_genes(index, path):
        with open(path) as f:
            lines = f.readlines()
        return lines[index].strip()


    def calc_quality_gain(self, projectInfo, initial_objectives):
        qmood_metrics_list = ["Effectiveness", "Extendibility", "Flexibility", "Functionality", "Resusability",
                              "Understandability"]

        qmood_metrics_value = Qmood().calculateQmood(projectInfo)
        return sum([(qmood_metrics_value[metric] - initial_objectives[metric]) for metric in qmood_metrics_list])

if __name__ =="__main__":
    local = False
    target = "-0.05648275862068591 -1.5240483265091924 -0.6288077744372642"
    if local:
        path_value = "/Users/leichen/Desktop/output/mbassador/FUN.NSGAII.SearchRO"
        path_sequence = "/Users/leichen/Desktop/output/mbassador/VAR.NSGAII.SearchRO"
        genes = GeneTranslater.find_genes(GeneTranslater.find_value_index(target, path_value), path_sequence)
        genes = [int(each) for each in genes.split(" ")]
        jsonFileRTE = "/Users/leichen/Desktop/mbassador.json"
        jClist = load_repository(jsonFile=jsonFileRTE, exclude_test=True, exclude_anonymous=True)
        GeneTranslater(genes).translate(jClist)
    else:
        repo = "mbassador"
        path_sequence = f"/Users/leichen/data/MORCO/experiment_result/{repo}/VAR.NSGAII.SearchRO"
        path_value = f"/Users/leichen/data/MORCO/experiment_result/{repo}/FUN.NSGAII.SearchRO"
        genes = GeneTranslater.find_genes(GeneTranslater.find_value_index(target, path_value), path_sequence)
        genes = [int(each) for each in genes.split(" ")]
        jsonFileRTE = f"/Users/leichen/Desktop/output/{repo}.json"
        jClist = load_repository(jsonFile=jsonFileRTE, exclude_test=True, exclude_anonymous=True)
        GeneTranslater(genes).translate(jClist)
        d = dict()