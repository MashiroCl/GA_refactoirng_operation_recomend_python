import unittest
from expertise.javafile import File
from expertise.repository import Repository
from expertise.ownership import get_file_ownership


class MyTestCase(unittest.TestCase):
    def test_repository(self):
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/antlr4"
        r = Repository(repo_path)
        files = r.get_files(exclude_tests=True)
        for file in files:
            file.get_commits()


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

if __name__ == '__main__':
    unittest.main()
