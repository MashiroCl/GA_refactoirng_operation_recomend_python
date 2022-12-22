import copy
from search_technique.SearchTechnique import SearchTechnique
from refactoring_operation.RefactoringOperationDispatcher import dispatch
from refactoring_operation.RefactoringOperationEnum import RefactoringOperationEnum
from encoding.IntegerEncoding import IntegerEncoding
from qmood.Qmood import Qmood
from code_ownership.CodeOwnership import CodeOwnership
from code_ownership.DeveloperGraph import DeveloperGraph
from code_ownership.PullRequestService import PullRequestService
from call_graph.CallGraph import CallGraph
from semantic.NameExtractor import NameExtractor
from semantic.Vectorize import TF_IDF


class GeneTranslater:
    """
    translate gene sequence into refactoring operations.

    Translate gene sequence into RO sequences according to encoding rules.
    """

    def __init__(self, genes: str, repo_path, ownership_path, developer_graph, call_graph, projectInfo):
        self.genes = genes
        self.repo_path = repo_path
        self.ownership_path = ownership_path
        self.developer_graph = developer_graph
        self.call_graph = call_graph
        self.projectInfo = projectInfo
        self.classes_nameSequence_dict = self.extract_names_sequences()
        self.tf_idf = TF_IDF()
        self.integerEncoding = IntegerEncoding()

    def exec_RO(self, decoded_sequences, projectInfo):
        '''
        perform refactoring operations in decoded_sequences on projectInfo
        return a list recording which refactorings has passed the preconditions and be executed
        '''
        executed = list()
        for each in decoded_sequences:
            executed.append(dispatch(each["ROType"].value)(each, projectInfo))
        return executed

    def translate(self):
        projectInfo = copy.deepcopy(self.projectInfo)
        self.integerEncoding.encoding(projectInfo)
        initial_objectives = Qmood().calculateQmood(projectInfo)
        decoded_sequences = self.integerEncoding.decoding(self.genes)
        res = list()
        field_and_method = ['class1field', 'class1method', 'class2field', 'class2method']
        for each in decoded_sequences:
            # Filter refactorings didn't pass preconditions
            if dispatch(each["ROType"].value)(each, projectInfo):
                if not (each['class1field'] == None and each['class1method'] == None and \
                        each['class2field'] == None and each['class2method'] == None):
                    res.append(each['ROType'])
                    res.append(each['class1'].classInfo)
                    res.append(each['class1'].filePath)
                    res.append(each['class2'].classInfo)
                    res.append(each['class2'].filePath)
                    for i in field_and_method:
                        if not each[i] is None:
                            res.append(each[i])
                    res.append(self.get_reviewer([each]))
                    res.append(self.calc_quality_gain(projectInfo, initial_objectives))
                    res.append(self.calc_relationship([each]))
                    res.append(self.calc_sematic_coherence(each))
        i = 0
        while i < len(res):
            print(res[i:i + 10])
            i = i + 10

    def translate_return(self):
        projectInfo = copy.deepcopy(self.projectInfo)
        self.integerEncoding.encoding(projectInfo)
        initial_objectives = Qmood().calculateQmood(projectInfo)
        decoded_sequences = self.integerEncoding.decoding(self.genes)
        res = list()
        field_and_method = ['class1field', 'class1method', 'class2field', 'class2method']
        for each_s in decoded_sequences:
            # Filter refactorings didn't pass preconditions
            if dispatch(each_s["ROType"].value)(each_s, projectInfo):
                if not (each_s['class1field'] == None and each_s['class1method'] == None and \
                        each_s['class2field'] == None and each_s['class2method'] == None):
                    res.append(each_s['ROType'])
                    res.append(each_s['class1'].classInfo)
                    res.append(each_s['class1'].filePath)
                    res.append(each_s['class2'].classInfo)
                    res.append(each_s['class2'].filePath)
                    for i in field_and_method:
                        if not each_s[i] is None:
                            res.append(each_s[i])
                    res.append(self.get_reviewer([each_s]))
                    res.append(self.calc_quality_gain(projectInfo, initial_objectives))
                    res.append(self.calc_relationship([each_s]))
                    res.append(self.calc_sematic_coherence(each_s))
        i = 0
        res_l = list()
        while i < len(res):
            res_l.append(res[i:i + 10])
            # print(res[i:i+10])
            i = i + 10
        return res_l

    def get_reviewer(self, decoded_sequences):
        co = CodeOwnership(self.repo_path, self.ownership_path)
        co.findAuthorPairList(decoded_sequences)
        return co.authorPairList

    @staticmethod
    def find_value_index(target: str, path: str):
        with open(path) as f:
            lines = f.readlines()
        for index, each in enumerate(lines):
            if target.strip() == each.strip():
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

    def calc_quality_attribute(self, projectInfo, initial_objectives):
        qmood_metrics_list = ["Effectiveness", "Extendibility", "Flexibility", "Functionality", "Resusability",
                              "Understandability"]
        qmood_metrics_value = Qmood().calculateQmood(projectInfo)
        res = dict()
        for metric in qmood_metrics_list:
            res[metric] = qmood_metrics_value[metric] - initial_objectives[metric]
        return res

    def translate_quality_attribute(self):
        projectInfo = copy.deepcopy(self.projectInfo)
        self.integerEncoding.encoding(projectInfo)
        initial_objectives = Qmood().calculateQmood(projectInfo)
        decoded_sequences = self.integerEncoding.decoding(self.genes)
        res = dict()
        for each_s in decoded_sequences:
            # Filter refactorings didn't pass preconditions
            if dispatch(each_s["ROType"].value)(each_s, projectInfo):
                if not (each_s['class1field'] == None and each_s['class1method'] == None and \
                        each_s['class2field'] == None and each_s['class2method'] == None):
                    quality_attribute = self.calc_quality_attribute(projectInfo, initial_objectives)
                    if each_s['class1'].classInfo == "2#CustomDiscardPolicy":
                        temp1 = quality_attribute
                        print(temp1)
                    if each_s['class1'].classInfo == "18#HouseKeeper":
                        temp2 = quality_attribute
                        print(temp2)
                    for each in quality_attribute.keys():
                        res[each] = res.get(each, 0) + quality_attribute[each]
        for each in temp1.keys():
            temp2[each] = temp2[each]-temp1[each]
        print(temp2)
        return res

    def translate_refactoring_type(self):
        projectInfo = copy.deepcopy(self.projectInfo)
        self.integerEncoding.encoding(projectInfo)
        decoded_sequences = self.integerEncoding.decoding(self.genes)
        res = list()
        for each_s in decoded_sequences:
            # Filter refactorings didn't pass preconditions
            if dispatch(each_s["ROType"].value)(each_s, projectInfo):
                if not (each_s['class1field'] == None and each_s['class1method'] == None and \
                        each_s['class2field'] == None and each_s['class2method'] == None):
                    if each_s['class1'].classInfo in each_s['class2'].superClassList if \
                            len(each_s['class2'].superClassList) == 0 else each_s['class2'].superClassList[0][0]:
                        if each_s['ROType'] == RefactoringOperationEnum.MOVEMETHOD:
                            res.append('PushDownMethod')
                        elif each_s['ROType'] == RefactoringOperationEnum.MOVEFIELD:
                            res.append('PushDownField')
                    elif each_s['class2'].classInfo in each_s['class1'].superClassList if \
                            len(each_s['class1'].superClassList) == 0 else each_s['class1'].superClassList[0][0]:
                        if each_s['ROType'] == RefactoringOperationEnum.MOVEMETHOD:
                            res.append('PullUpMethod')
                        elif each_s['ROType'] == RefactoringOperationEnum.MOVEFIELD:
                            res.append('PullUpField')
                    else:
                        res.append(each_s['ROType'])
        return res

    def calc_relationship(self, decoded_sequence):
        return CodeOwnership(self.repo_path, self.ownership_path).findAuthorPairList(decoded_sequence). \
            calculateRelationship(self.developer_graph)

    def vectorize_classes(self, classes):
        res = list()
        for each in classes:
            res.append(self.classes_nameSequence_dict[each.getKey()])
        return self.tf_idf.vectorize(res)

    def extract_names_sequences(self):
        name_extractor = NameExtractor()
        names_dict = name_extractor.extract(self.projectInfo)
        sequence_dict = name_extractor.dict_names_to_dict_sequence(names_dict)
        return sequence_dict

    def calc_cosine_similarity(self, doc_metric):
        return self.tf_idf.cosine_similarity(doc_metric)

    def calc_sematic_coherence(self, decoded_sequence):
        X = self.vectorize_classes([decoded_sequence["class1"], decoded_sequence["class2"]])
        cosine_smiliarity = self.calc_cosine_similarity(X).tolist()[1]
        call_relation = self.call_graph.calc_call_relation([decoded_sequence])
        return 0.2 * cosine_smiliarity + 0.8 * call_relation

    def add_RE(self, path_fun, path_val):
        result = list()
        with open(path_fun) as f:
            nre = f.readlines()
            for each_nre in nre:
                projectInfo = copy.deepcopy(self.projectInfo)
                self.integerEncoding.encoding(projectInfo)
                each_nre = each_nre.strip()
                gene = self.find_genes(self.find_value_index(target=each_nre, path=path_fun), path_val)
                gene = [int(each_temp) for each_temp in gene.split(" ")]
                decoded_sequences = self.integerEncoding.decoding(gene)
                rs = 0
                count = 0
                for each_s in decoded_sequences:
                    if dispatch(each_s["ROType"].value)(each_s, projectInfo):
                        rs = rs + self.calc_relationship([each_s])
                        count = count + 1
                each_nre = each_nre.strip().split(" ")[0] + " " + str(-1 * rs / (count if count != 0 else 1)) + " " + \
                           each_nre.strip().split(" ")[1]
                result.append([each_nre])
        return result


def translate_NRE():
    'translate FUN.xxxNRE'
    targets = ["-0.7727382249231167 -0.9108934863331157"]
    # 'in mockito Tim van der Lippe, Szczepan Faber'
    # targets = ["-0.009694511913036774 -0.45103811477801214"]
    # 'in mockito, Rafael Winterhalter, Brice Dutheil, Review effort 0.14810329376637735'
    # targets = ["-0.0033237055955012695 -0.8510603174865987"]
    ros = list()
    for target in targets:
        repo = "mockito"
        path_sequence = f"/Users/leichen/experiement_result/MORCoRE/RQ1/{repo}/VAR.Nsga3NRE"
        path_value = f"/Users/leichen/experiement_result/MORCoRE/RQ1/{repo}/FUN.Nsga3NRE"
        genes = GeneTranslater.find_genes(GeneTranslater.find_value_index(target, path_value), path_sequence)
        genes = [int(each) for each in genes.split(" ")]
        jsonFileRTE = f"/Users/leichen/Desktop/StaticalAnalysis/{repo}.json"
        jClist = SearchTechnique().load_repository(json_file=jsonFileRTE, exclude_test=True, exclude_anonymous=True)
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo
        ownership_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/ownership.csv"

        relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/pullrequest.csv"

        call_graph = CallGraph(
            "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/callgraph.json")

        res = PullRequestService().loadPullRequest(relationshipCsvPath)
        developerGraph = DeveloperGraph(res).generate_vertices().build()

        ros.append(
            GeneTranslater(genes, repo_path, ownership_path, developerGraph, call_graph, jClist).translate_return())
    return ros


def translate_RE(*others):
    'translate FUN.xxxRE'
    target = "-0.02454980842912219 -0.547911029481592 -12.742170936827694"
    repo = "mbassador"


    path_sequence = f"/Users/leichen/experiement_result/MORCoRE2/RQ1/{repo}/VAR.Nsga3RE"
    path_value = f"/Users/leichen/experiement_result/MORCoRE2/RQ1/{repo}/FUN.Nsga3RE"
    genes = GeneTranslater.find_genes(GeneTranslater.find_value_index(target, path_value), path_sequence)
    # path_sequence = f"/Users/leichen/Desktop/output/{repo}/VAR.Nsga3RE"
    # path_value = f"/Users/leichen/Desktop/output/{repo}/FUN.Nsga3RE"
    genes = [int(each) for each in genes.split(" ")]
    jsonFileRTE = f"/Users/leichen/Desktop/StaticalAnalysis/{repo}.json"
    jClist = SearchTechnique().load_repository(json_file=jsonFileRTE, exclude_test=True, exclude_anonymous=True)

    repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo
    ownership_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/ownership.csv"
    relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/pullrequest.csv"
    call_graph = CallGraph(
        "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/callgraph.json")

    res = PullRequestService().loadPullRequest(relationshipCsvPath)
    developerGraph = DeveloperGraph(res).generate_vertices().build()

    GeneTranslater(genes, repo_path, ownership_path, developerGraph, call_graph, jClist).translate()


def translate_quality_attribute(repo):
    'translate FUN.xxxRE'
    path_sequence = f"/Users/leichen/experiement_result/MORCoRE/RQ1/{repo}/VAR.Nsga3RE"
    path_value = f"/Users/leichen/experiement_result/MORCoRE/RQ1/{repo}/FUN.Nsga3RE"
    jsonFileRTE = f"/Users/leichen/Desktop/StaticalAnalysis/{repo}.json"
    jClist = SearchTechnique().load_repository(json_file=jsonFileRTE, exclude_test=True, exclude_anonymous=True)
    repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo
    ownership_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/ownership.csv"
    relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/pullrequest.csv"
    call_graph = CallGraph(
        "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/callgraph.json")
    pull_request = PullRequestService().loadPullRequest(relationshipCsvPath)
    developerGraph = DeveloperGraph(pull_request).generate_vertices().build()
    targets = get_ranked(path_value)

    res = dict()
    for target in targets[:5]:
        target = (" ").join([str(each) for each in target])
        genes = GeneTranslater.find_genes(GeneTranslater.find_value_index(target, path_value), path_sequence)
        genes = [int(each) for each in genes.split(" ")]
        quality_attribute = GeneTranslater(genes, repo_path, ownership_path, developerGraph, call_graph,
                                           jClist).translate_quality_attribute()
        for each in quality_attribute:
            res[each] = res.get(each, 0) + quality_attribute[each]
    return res


def get_ranked(path):
    data = list()
    with open(path) as f:
        for line in f.readlines():
            data.append([float(each) for each in line.split(" ")[0:3]])
    data = sorted(data, key=lambda x: x[0])
    return data


def cal_refactoring_types(repo):
    path_sequence = f"/Users/leichen/experiement_result/MORCoRE2/RQ1/{repo}/VAR.Nsga3RE"
    path_value = f"/Users/leichen/experiement_result/MORCoRE2/RQ1/{repo}/FUN.Nsga3RE"
    jsonFileRTE = f"/Users/leichen/Desktop/StaticalAnalysis/{repo}.json"
    jClist = SearchTechnique().load_repository(json_file=jsonFileRTE, exclude_test=True, exclude_anonymous=True)
    repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo
    ownership_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/ownership.csv"
    relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/pullrequest.csv"
    call_graph = CallGraph(
        "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/callgraph.json")
    pull_request = PullRequestService().loadPullRequest(relationshipCsvPath)
    developerGraph = DeveloperGraph(pull_request).generate_vertices().build()
    targets = get_ranked(path_value)

    res = list()
    for target in targets[:5]:
        target = (" ").join([str(each) for each in target])
        genes = GeneTranslater.find_genes(GeneTranslater.find_value_index(target, path_value), path_sequence)
        genes = [int(each) for each in genes.split(" ")]
        res.append(GeneTranslater(genes, repo_path, ownership_path, developerGraph, call_graph,
                                  jClist).translate_refactoring_type())
    return res

def generate_re_a(repo, path, path_value):
    repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo
    ownership_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/ownership.csv"
    call_graph = CallGraph("/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/callgraph.json")
    relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/pullrequest.csv"
    res = PullRequestService().loadPullRequest(relationshipCsvPath)
    developerGraph = DeveloperGraph(res).generate_vertices().build()
    jsonFileRTE = f"/Users/leichen/Desktop/StaticalAnalysis/{repo}.json"
    jClist = SearchTechnique().load_repository(json_file=jsonFileRTE, exclude_test=True, exclude_anonymous=True)
    genes = [""]
    res = GeneTranslater(genes, repo_path, ownership_path, developerGraph, call_graph, jClist).add_RE(path, path_value)

    with open(f"/Users/leichen/experiement_result/MORCoRE/RQ1_03/{repo}/FUN.Nsga3NRE_A", "w") as f:
        for each in res:
            f.writelines(each)
            f.write("\n")

if __name__ == "__main__":
    'translate FUN.xxxRE'
    translate_RE()

    'translate FUN.xxxNRE'
    # res = translate_NRE()
    # for each in res[0]:
    #     print(each)

    'Use FUN.xxxNRE and VAL.xxxNRE to calculate review effort and write into FUN.xxxRE_A, review effort is the 2nd column'
    # repos = ["javapoet", "HikariCP", "mbassador"]
    # repos = ["mockito", "quasar"]
    # for repo in repos:
    #     generate_re_a(repo,
    #                   f"/Users/leichen/experiement_result/MORCoRE/RQ1_03/{repo}/FUN.Nsga3NRE",
    #                   f"/Users/leichen/experiement_result/MORCoRE/RQ1_03/{repo}/VAR.Nsga3NRE")

    # res = translate_quality_attribute("javapoet")
    # print(res)
    # get_top("/Users/leichen/experiement_result/MORCoRE/RQ1/javapoet/FUN.Nsga3RE")

    'Count number of refactoring types in recommended refactoirng sequence in each repository'
    # repos = ["javapoet", "HikariCP", "mbassador", "quasar", "mockito"]
    # import collections
    # res = dict()
    # for repo in repos:
    #     refactoring_types = cal_refactoring_types(repo)
    #     l = collections.Counter([i for k in refactoring_types for i in k])
    #     for each in l.keys():
    #         res[each] = res.get(each,0)+l.get(each)
    # print(res)

    'translate quality attribute for example used in 5.2.2 of thesis'
    # repo = "HikariCP"
    # path_sequence = f"/Users/leichen/experiement_result/MORCoRE/RQ1/{repo}/VAR.Nsga3RE"
    # path_value = f"/Users/leichen/experiement_result/MORCoRE/RQ1/{repo}/FUN.Nsga3RE"
    # jsonFileRTE = f"/Users/leichen/Desktop/StaticalAnalysis/{repo}.json"
    # jClist = load_repository(jsonFile=jsonFileRTE, exclude_test=True, exclude_anonymous=True)
    # repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo
    # ownership_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/ownership.csv"
    # relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/pullrequest.csv"
    # call_graph = CallGraph(
    #     "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repo + "/MORCOoutput/csv/callgraph.json")
    # pull_request = PullRequestService().loadPullRequest(relationshipCsvPath)
    # developerGraph = DeveloperGraph(pull_request).generate_vertices().build()
    # target = ["-0.0729362224455112 -0.8571428571428571 -0.5264928986368382"]
    # target = " ".join([str(each) for each in target])
    # genes = GeneTranslater.find_genes(GeneTranslater.find_value_index(target, path_value), path_sequence)
    # genes = [int(each) for each in genes.split(" ")]
    # res = GeneTranslater(genes, repo_path, ownership_path, developerGraph, call_graph, jClist).translate_quality_attribute()
