import unittest
from expertise.javafile import File
from expertise.repository import Repository
from expertise.ownership import get_file_ownership, get_repo_ownership, \
    jaccard, get_repo_ownership_t, search_similar_files, get_rev_file_ownership, extract_owners, get_path_owner_dict


class MyTestCase(unittest.TestCase):
    def test_repository(self):
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/antlr4"
        r = Repository(repo_path)
        files = r.get_files(exclude_tests=True)
        for file in files:
            file.get_commits()

    def test_commits2csv(self):
        file_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/antlr4/antlr4-maven-plugin/src/main/java/org/antlr/mojo/antlr4/MojoUtils.java"
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/antlr4"
        f = File(repo_path, file_path)
        f.commits2csv()

    def test_log_commits(self):
        file_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/antlr4/antlr4-maven-plugin/src/main/java/org/antlr/mojo/antlr4/MojoUtils.java"
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/antlr4"
        f = File(repo_path, file_path)
        res=f.get_commits()
        for each in res:
            print(each)
        self.assertEqual("parrt", res[0].author_name)

    def test_get_file_ownership(self):
        file_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/antlr4/antlr4-maven-plugin/src/main/java/org/antlr/mojo/antlr4/MojoUtils.java"
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/antlr4"
        f = File(repo_path, file_path)
        res = get_file_ownership(f)
        self.assertEqual("0.625", res[0].ownership)
        self.assertEqual("0.375", res[0].ownership)

    def test_get_ownership_for_repo(self):
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
        output_path = "./mbassador.csv"
        get_repo_ownership(repo_path, output_path)

    def test_jaccard(self):
        path1 = "1/2/3/4"
        path2 = "3/4/5/6/7/8"
        self.assertEqual(jaccard(path1,path2), 0.25)

    def test_similar_files(self):
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
        files = Repository(repo_path).get_files()
        similar_files = search_similar_files(files[0], files)
        # print(f"origin: {files[0].path}")
        # print("==================================")
        # for each in similar_files:
        #     print(each.path)
        self.assertEqual(len(similar_files),4)

    def test_get_rev_file_ownership(self):
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
        files = Repository(repo_path).get_files()
        similar_files = search_similar_files(files[0], files)
        res = get_rev_file_ownership(files[1],"bennidi",similar_files)
        # print(res)
        self.assertEqual(res.ownership,1.9448464697829062)

    def test_get_ownership_for_repo_t(self):
        import time
        start = time.time()
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/jedis"
        output_path = "./jedis.csv"
        get_repo_ownership_t(repo_path, output_path)
        end = time.time()
        print(end-start)

    def test_extract_owners(self):
        csv_path = "./mbassador_t.csv"
        output_path = "./owners.csv_utils"
        with open(output_path,"w") as f:
            extract_owners(csv_path,f)

    def test_jedis(self):
        import glob
        files = glob.glob("/Users/leichen/ResearchAssistant/InteractiveRebase/data/quasar/**/*.java",recursive=True)
        print(len(files))

    def test_mkdir(self):
        import os
        path = "/Users/leichen/Desktop/output/mkdir"
        if not os.path.exists(path):
            os.mkdir(path)
        os.system("cd /Users/leichen/Desktop/output/mkdir && touch 123.txt")



    def test_get_path_owner_dict(self):
        owners_path = "/Users/leichen/experiement_result/MORCoRE2/RQ1/ActionBarSherlock/csv/owners.csv"
        res = get_path_owner_dict(owners_path)
        self.assertEqual(res['/ActionBarSherlock/actionbarsherlock/src/com/actionbarsherlock/internal/ActionBarSherlockNative.java'], ['JakeWharton', 'Alexandr Tereshchuk'])

if __name__ == '__main__':
    unittest.main()
