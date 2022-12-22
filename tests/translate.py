import unittest
from translation.translate import get_genes, decode_gene, encode_abs, trans_decoded_gene, build_NRE_a
from search_technique.SearchTechnique import SearchTechnique
from translation.extract_results import top_k
from copy import deepcopy

class MyTestCase(unittest.TestCase):
    def test_get_genes_RE(self):
        fun = "-0.02454980842912219 -0.547911029481592 -12.742170936827694"
        fun_p = "/Users/leichen/Desktop/output/mbassador/FUN.Nsga3RE"
        var_p = "/Users/leichen/Desktop/output/mbassador/VAR.Nsga3RE"
        res = get_genes(fun, fun_p, var_p)
        self.assertEqual(res, [2, 61, 4, 2, 2, 53, 52, 15, 5, 22, 61, 11, 3, 16, 15, 11, 3, 82, 74, 12])

    def test_get_genes_NRE(self):
        fun = "-0.02723470694992325 -0.8091368343799099"
        fun_p = "/Users/leichen/Desktop/output/mbassador/FUN.Nsga3NRE"
        var_p = "/Users/leichen/Desktop/output/mbassador/VAR.Nsga3NRE"
        res = get_genes(fun, fun_p, var_p)
        self.assertEqual(res,[7, 80, 63, 8, 7, 46, 60, 10, 2, 11, 15, 14, 2, 16, 66, 1, 3, 49, 12, 14])

    def test_trans_decoded_gene_RE(self):
        st = SearchTechnique()
        json_file_path = "/Users/leichen/Desktop/output/mbassador.json"
        abs = st.load_repository(json_file=json_file_path, exclude_test=True, exclude_anonymous=True)
        gene = [int(each) for each in "2 61 4 2 2 53 52 15 5 22 61 11 3 16 15 11 3 82 74 12".split(" ")]
        owners_p = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCoRE/csv/owners.csv"
        encoder = encode_abs(abs)
        refactorings = decode_gene(gene, encoder)
        paths = dict()
        paths["owners"] = owners_p
        paths["pr"] = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCoRE/csv/pullrequest.csv"
        res = trans_decoded_gene(refactorings, abs, paths)
        print(res)


    def test_trans_decoded_gene_NRE(self):
        st = SearchTechnique()
        json_file_path = "/Users/leichen/Desktop/output/mbassador.json"
        abs = st.load_repository(json_file=json_file_path, exclude_test=True, exclude_anonymous=True)
        gene = [int(each) for each in "7 80 63 8 7 46 60 10 2 11 15 14 2 16 66 1 3 49 12 14".split(" ")]
        owners_p = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCoRE/csv/owners.csv"
        encoder = encode_abs(abs)
        refactorings = decode_gene(gene, encoder)
        paths = dict()
        paths["owners"] = owners_p
        paths["pr"] = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCoRE/csv/pullrequest.csv"
        res = trans_decoded_gene(refactorings, abs, paths)
        for each in res:
            print(each)


    def test_top_k(self):
        fun_p = "/Users/leichen/Desktop/output/mbassador/FUN.Nsga3NRE"
        res = top_k(fun_p,5)
        print(res)

    def test_trans_decoded_genes_RE(self):
        st = SearchTechnique()
        json_file_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCoRE/csv/abs.json"
        abs = st.load_repository(json_file=json_file_path, exclude_test=True, exclude_anonymous=True)
        fun_p = "/Users/leichen/Desktop/output/mbassador/FUN.Nsga3NRE"
        var_p = "/Users/leichen/Desktop/output/mbassador/VAR.Nsga3NRE"
        owners_p = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCoRE/csv/owners.csv"
        funs = top_k(fun_p,5)
        paths = dict()
        paths["owners"] = owners_p
        paths["pr"] = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCoRE/csv/pullrequest.csv"
        for fun in funs:
            gene = get_genes(fun, fun_p, var_p)
            encoder = encode_abs(abs)
            refactorings = decode_gene(gene, encoder)
            res = trans_decoded_gene(refactorings, abs, paths)
            print(res)


    def test_collaboration_score_calculation_valkyrie(self):
        repo  = "ActionBarSherlock"
        st = SearchTechnique()
        json_file_path = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo}/csv/abs.json"
        abs = st.load_repository(json_file=json_file_path, exclude_test=True, exclude_anonymous=True)
        fun_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo}/FUN.Nsga3NRE"
        var_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo}/VAR.Nsga3NRE"
        owners_p = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo}/csv/owners.csv"
        funs = top_k(fun_p,5)
        count = 0
        from copy import deepcopy
        for fun in funs[:]:
            abs_temp = deepcopy(abs)
            encoder = encode_abs(abs_temp)
            count+=1
            gene = get_genes(fun, fun_p, var_p)
            refactorings = decode_gene(gene, encoder)
            paths = dict()
            paths["owners"] = owners_p
            paths["pr"] = f"/Users/leichen/experiement_result/MORCoRE2/1st_test_output/{repo}/csv/pullrequest.csv"
            res = trans_decoded_gene(refactorings, abs_temp, paths)
            for each in res:
                print(each["reviewers"])
            print(sum(each["collaboration_score"] for each in res)/len(res))


    # write NRE_a for a RE file to check the correctness of the collabortion score
    def test_build_NRE_a_HikariCP(self):
        repo_name = "HikariCP"
        output_root = "/Users/leichen/experiement_result/MORCoRE2/output/HikariCP/output1/"
        fun_p = output_root+"FUN.Nsga3RE"
        var_p = output_root+"VAR.Nsga3RE"
        infos = {
            "abs":f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/abs.json",
            "owner":f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/owners.csv",
            "pr":f"/Users/leichen/experiement_result/MORCoRE2/infos/{repo_name}/csv/pullrequest.csv"
        }
        build_NRE_a(fun_p,var_p,infos)