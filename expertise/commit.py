'''
Class for git commit
Initialized by json form commit message:
  "commit": "b5648f405b746d87ec559132ad1939fb6d402053",
 "author": {
    "name": "parrt",
    "email": "parrt@cs.usfca.edu",
    "date": "Thu, 30 Mar 2017 10:44:25 -0700"
  },
'''


class Commit:
    def __init__(self, commit: str):
        self.sha = commit.get("commit",None)
        if self.sha:
            self.author_name = commit.get("author").get("name")
            self.author_email = commit.get("author").get("email")
            self.time = commit.get("author").get("date")

    def __str__(self):
        return f"sha: {self.sha}, author_name:{self.author_name}, author_email:{self.author_email}, commit_time:{self.time}"
