import unittest
import os
import code_ownership.Repository


class MyTestCase(unittest.TestCase):
    path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
    r = code_ownership.Repository.Repository(path)

    def test_owner_extraction(self):
        csvPath = os.path.join(self.path, "MORCoREoutput", "ownership.csv")
        commitOutputPath = os.path.join(self.path, "MORCoREoutput")
        csvOutputPath = os.path.join(self.path, "MORCoREoutput", "csv")
        csvName = "ownership.csv"
        localPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data"
        MyTestCase.r.countAuthorCommit(commitOutputPath).authorCommitDict2CSV(csvOutputPath, csvName, localPath).extract_owner_csv()


if __name__ == '__main__':
    unittest.main()
