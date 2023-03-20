import unittest
from expertise.build_table import *


class MyTestCase(unittest.TestCase):
    def test_build_expertise_table(self):
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mockito"
        build_expertise_table(repo_path, "./expertise_table.csv")

    def test_build_hashmap(self):
        repo_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/HikariCP"
        personal_ownerships = extract_personal_ownerships(repo_path)
        build_hashmap(personal_ownerships)

    def test_extract_reviewers(self):
        expertise_table_path = "./expertise_table.csv"
        workload_path = "/Users/leichen/Code/pythonProject/pythonProject/salabResearch/tests/workload.json"
        file_paths = ['/mockito/src/main/java/org/mockito/internal/junit/DefaultStubbingLookupListener.java', '/mockito/src/main/java/org/mockito/internal/exceptions/stacktrace/ConditionalStackTraceFilter.java', '/mockito/src/main/java/org/mockito/internal/creation/bytebuddy/InlineByteBuddyMockMaker.java', '/mockito/src/main/java/org/mockito/internal/creation/bytebuddy/SubclassByteBuddyMockMaker.java', '/mockito/src/main/java/org/mockito/stubbing/Stubber.java', '/mockito/src/main/java/org/mockito/internal/configuration/injection/MockInjectionStrategy.java', '/mockito/src/main/java/org/mockito/ArgumentMatcher.java', '/mockito/src/main/java/org/mockito/internal/util/collections/Sets.java', '/mockito/src/main/java/org/mockito/internal/creation/bytebuddy/ByteBuddyMockMaker.java', '/mockito/src/main/java/org/mockito/internal/creation/bytebuddy/InlineByteBuddyMockMaker.java', '/mockito/src/main/java/org/mockito/internal/stubbing/defaultanswers/ReturnsEmptyValues.java', '/mockito/src/main/java/org/mockito/internal/stubbing/answers/ClonesArguments.java', '/mockito/src/main/java/org/mockito/internal/verification/checkers/NumberOfInvocationsChecker.java', '/mockito/src/main/java/org/mockito/internal/matchers/Same.java', '/mockito/src/main/java/org/mockito/internal/creation/bytebuddy/ByteBuddyMockMaker.java', '/mockito/src/main/java/org/mockito/internal/creation/bytebuddy/InlineByteBuddyMockMaker.java', '/mockito/src/main/java/org/mockito/internal/creation/bytebuddy/ByteBuddyMockMaker.java', '/mockito/src/main/java/org/mockito/internal/creation/bytebuddy/InlineByteBuddyMockMaker.java', '/mockito/src/main/java/org/mockito/internal/matchers/And.java', '/mockito/src/main/java/org/mockito/internal/matchers/Or.java']
        res = extract_reviewers_expertise(expertise_table_path=expertise_table_path,
                                    workload_path=workload_path,
                                    file_paths=file_paths,
                                    threshold_workload=2)

        print(res)


    def test_get_highest_expertise_reviewer(self):
        reviewer_expertise = {'Stephan Schroevers': 0.4950376454483231, 'Rafael Winterhalter': 89.10044490075289, 'Szczepan Faber': 31.558350444900753, 'Allon Murienik': 3.04414784394250}
        res = get_highest_expertise_reviewer(reviewer_expertise)
        self.assertEqual("Rafael Winterhalter", res[0])