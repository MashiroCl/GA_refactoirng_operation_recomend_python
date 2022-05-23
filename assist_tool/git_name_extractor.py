import csv
from github import Github
import json
import time
import os
from tqdm import tqdm
from code_ownership.Commit import Commit

class NameExtractor:
    def extract(self, source) -> set:
        pass


class GitLogNameExtractor(NameExtractor):
    def extract(self, source) -> set:
        '''
        extract name set from git log(json)
        '''
        result = set()
        with open(source) as file:
            data = "[" + file.read() + "]"
        data = data.replace("\\", " ")
        data = json.loads(data)
        commits = []
        for each in data:
            commits.append(Commit(each))
        for each in commits:
            result.add(each.authorName)
        return result

class NameUnifier():
    def _append_csv(self, row):
        with open("./fixed_pull_request.csv", "a") as fixed_csv:
            writer = csv.writer(fixed_csv)
            writer.writerow(row)
    def _write_csv(self, contents):
        with open("./fixed_pull_request_w.csv", "w") as fixed_csv:
            writer = csv.writer(fixed_csv)
            writer.writerows(contents)

    def _append_json(self, content):
        with open("login_name.json", "a") as f:
            f.write(content)
            f.write(",")

    def _read_json(self, jsonpath)->dict:
        res = dict()
        with open(jsonpath) as f:
            data = f.read()
            if data[-1]==",":
                data = json.loads("[" + data[:-1] + "]")
            else:
                data = json.loads("[" + data + "]")
            for each in data:
                for login in each.keys():
                    if res.get(login,0)!=0:
                        print(login)
                    res[login] = each[login]
        return res

    def unify(self, pr):
        login_name_dict = self._read_json("./login_name.json")
        new_content = list()
        with open(pr) as f:
            reader = csv.reader(f)
            for row in reader:
                for i in range(len(row)):
                    if row[i] in login_name_dict.keys():
                        print(f"change {row[i]} to {login_name_dict[row[i]]}")
                        row[i] = login_name_dict[row[i]]
                new_content.append(row)
            self._write_csv(new_content)
        print("written into csv")

    def get_login_name_dict(self, pr, start = 0, end = 1000)->dict:
        res = dict()
        logins = PullRequestNameExtractor().extract(pr)
        count = 0
        logins = list(sorted(logins))
        print(f"total length of logins is: {len(logins)}")
        for each in tqdm(logins[start: min(end,len(logins))]):
            #Default the first searching result as the most optimal result
            count+=1
            user_candidiates = self.search_name_by_login(each)
            # limitation of github search api:30 requests per minute
            if count%15==0:
                self._append_json(json.dumps(res))
                res= dict()
                time.sleep(61)
            if user_candidiates.totalCount!=0:
                if user_candidiates[0].name:
                    res[each] = user_candidiates[0].name
                else:
                    # the user didn't set name, login is the only identifier
                    res[each] = each
            else:
                print(each)
        return res

    def search_name_by_login(self, name) -> set:
        g = Github(os.getenv("GIT_SERVICE_IMPLEMENTAION_TOKEN"))
        res = g.search_users(name)
        return res


class PullRequestNameExtractor(NameExtractor):
    '''
    extract name set from pull request csv
    '''
    def extract(self, source) -> set:
        result = set()
        with open(source) as f:
            reader = csv.reader(f)
            for row in reader:
                for i in self.name_index(row):
                    if row[i]!= "" and row[i]!=" ":
                        result.add(row[i])
        return result

    def name_index(self, row):
        l = len(row)
        if row[-1] == " ":
            #last index is " "
            l=l-1
        #url and status
        l=l-2
        l=int(l/2)
        return [2*index for index in range(1, l+1)]

if __name__ == "__main__":

    csv_path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/HikariCP/MORCOoutput/csv/pullrequest.csv"
    #
    # NameUnifier().get_login_name_dict(csv_path, 300, 358)
    NameUnifier().unify(csv_path)

    # data = NameUnifier()._read_json("./login_name.json")
    # print(len(data))
    # import pprint
    # pprint.pprint(data)
