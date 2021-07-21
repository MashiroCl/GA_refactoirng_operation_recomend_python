class Commit():
    def __init__(self,jsonStr:str):
        self.jsonStr=jsonStr
        self.log2Commits()

    'analyse the json format into class Commit'
    def log2Commits(self):
        self.commitID = self.jsonStr["commit"]
        self.authorName = self.jsonStr["author"]["name"]
        self.authorEmail=self.jsonStr["author"]["email"]
        self.authenticationData=self.jsonStr["author"]["date"]
        self.commiterName = self.jsonStr["commiter"]["name"]
        self.commiterEmail=self.jsonStr["commiter"]["email"]
        self.commitData=self.jsonStr["commiter"]["date"]
        self.subject = self.jsonStr["subject"]
