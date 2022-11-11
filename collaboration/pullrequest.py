import json
from typing import List
import utils.githubapi as api
import utils.time as time
from collaboration.comment import Comment


class Pullrequest:
    def __init__(self, pullrequest:json):
        self.url = pullrequest.get("url", None)
        self.proposer = pullrequest.get("user").get("login")
        self.comments_url = pullrequest.get("comments_url")
        self.comments = None
        self.state = pullrequest.get("state")
        self.closed_merged_by = None
        self.closed_merged_at = None
        if self.state == "closed":
            content = self.get_content()
            if content.get("merged"):
                self.state = "merged"
            self.closed_merged_by = self._get_closer(content)
            self.closed_merged_at = time.format_prtime(content.get("closed_at", None))

    def get_content(self):
        return api.api_request(self.url).json()

    def _get_closer(self, pullrequest):
        res = None
        if self.state == "merged":
            closed_merged_by = pullrequest.get("merged_by", None)
            if closed_merged_by:
                res = closed_merged_by.get("login")
        elif self.state == "closed":
            closed_merged_by = pullrequest.get("closed_by", None)
            if closed_merged_by:
                res = closed_merged_by.get("login")
            else:
                res = self.proposer
        return res

    def get_comments(self) -> List[Comment]:
        response = api.api_request(self.comments_url)
        self.comments = [Comment(each) for each in response.json()]
        return self.comments

    def to_list(self) -> List[str]:
        comments = []
        for each in self.comments:
            comments += each.to_list()
        close_info = []
        if self.closed_merged_by and self.closed_merged_at:
            close_info.append(self.closed_merged_by)
            close_info.append(self.closed_merged_at)
        return [self.url, self.state, self.proposer] + comments + close_info
