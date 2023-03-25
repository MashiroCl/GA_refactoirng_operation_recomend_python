"""
calculate workload use github pullrequest & issues
Use the result of calc_workload() to check whether manually unifying reviewers' names are required
Use get_workload_dict() to obtain the workload table for all reviewers
"""
from dataclasses import dataclass
import datetime
from enum import Enum
from typing import List
from collections import Counter
import json
from utils.githubapi import api_request, get_REPO_USER_from_github_url
from utils.time import to_datetime


class EnumEvent(Enum):
    PULLREQUEST = "PULLREQUEST"
    ISSUE = "ISSUE"


@dataclass
class ParticipantInfo:
    event: EnumEvent
    action_time: datetime.datetime


class Event:
    def __init__(self, response):
        self.url = response.get("url", None)
        self.proposer = response.get("user").get("login")
        self.comments_url = response.get("comments_url")
        self.comments = self._get_comments()
        self.created_at = response.get("created_at")
        self.updated_at = response.get("updated_at", None)
        self.github_api = None

    def is_later_than_endpoint(self, end_point: datetime.datetime) -> bool:
        """
        determine if events are proposed after the endpoint, should not be counted into workload
        """
        if not self.updated_at:
            raise RuntimeError("updated_at not exists for event ", self.url)
        if datetime.timedelta(days=0) > end_point - to_datetime(self.updated_at):
            return True
        return False

    def is_time_valid(self, end_point: datetime.datetime, period: datetime.timedelta) -> bool:
        if not self.updated_at:
            raise RuntimeError("updated_at not exists for event ", self.url)
        if datetime.timedelta(days=0) <= end_point - to_datetime(self.updated_at) <= period:
            return True
        return False

    def _get_comments(self):
        response = api_request(self.comments_url).json()
        comments = []
        for each in response:
            comments.append(Comment(each))
        return comments


def build_author_pair(a1: str, a2: str):
    return a1 + "," + a2


class Comment:
    def __init__(self, response):
        self.url = response.get("url", None)
        self.user = response.get("user").get("login")


def get_time_valid_issues(url, end_point, period) -> List[Event]:
    repo_user = get_REPO_USER_from_github_url(url)
    page_num = 1
    issues = list()
    while True:
        request = f"https://api.github.com/repos/{repo_user}/issues?page={page_num}&state=all"
        response = api_request(request).json()
        if len(response) == 0:  # no issue on this page
            break
        for each in response:
            try:
                e = Event(each)
                if e.is_later_than_endpoint(end_point):
                    continue
                if e.is_time_valid(end_point, period):
                    issues.append(e)
            except RuntimeError:
                print("RuntimeError for event", each)
                print("In response", response)
        page_num += 1
    return issues


def get_time_valid_pullrequest(url, end_point, period) -> List[Event]:
    repo_user = get_REPO_USER_from_github_url(url)
    page_num = 1
    pullrequests = list()
    while True:
        request = f"https://api.github.com/repos/{repo_user}/pulls?page={page_num}&state=all"
        response = api_request(request).json()
        if len(response) == 0:  # no pr on this page
            break
        for each in response:
            e = Event(each)
            if e.is_later_than_endpoint(end_point):
                continue
            if e.is_time_valid(end_point, period):
                pullrequests.append(e)
        page_num += 1
    return pullrequests


def get_issue_participants(url, end_point, period) -> List[str]:
    participants = list()
    issues = get_time_valid_issues(url, end_point, period)
    for issue in issues:
        comment_participants = set()  # count 1 if participated in single/multiple commetns
        comment_participants.add(issue.proposer)  # issue proposer
        for comment in issue.comments:
            comment_participants.add(comment.user)  # issue commentators
        participants += list(comment_participants)
    return participants


def get_pullrequest_participants(url, end_point, period):
    participants = list()
    pullrequests = get_time_valid_pullrequest(url, end_point, period)
    for pullrequest in pullrequests:
        print(pullrequest.url)
        comment_participants = set()  # count 1 if participated in single/multiple commetns
        comment_participants.add(pullrequest.proposer)  # pullrequest proposer
        for comment in pullrequest.comments:
            comment_participants.add(comment.user)
        participants += comment_participants
    return participants


def append_pair_workload(workload: Counter) -> dict:
    workload = dict(sorted(workload.items(), key=lambda x: x[0]))
    devs = list(workload.keys())
    for i in range(len(devs)):
        for j in range(i + 1, len(devs)):
            workload[build_author_pair(devs[i], devs[j])] = workload[devs[i]] + workload[devs[j]]
    return workload


def get_workload_dict(workload: dict, all_reviewers):
    """
    build the workload table for all_reviewers
    """
    res = dict()
    for reviewer in all_reviewers:
        if "," in reviewer:  # reviewer pair
            reviewers = reviewer.split(",")
            v = 2
            if reviewers[0] in workload.keys():
                v += workload[reviewers[0]]
            if reviewers[1] in workload.keys():
                v += workload[reviewers[1]]
            res[reviewer] = v
        else:  # single reviewer
            v = 1
            if reviewer in workload.keys():
                v += workload[reviewer]
            res[reviewer] = v
    return res


def cal_workload(url, end_point, period) -> dict:
    """
    one participation in a pullrequest/issue count to 1 point in workload, the workload is calculated
    for all_reviewers
    participation means reviewers who propose a pullrequest/issue or propose a comment
    """
    issue_participants = get_issue_participants(url, end_point, period)
    pullreqeust_participants = get_pullrequest_participants(url, end_point, period)
    workload = issue_participants + pullreqeust_participants
    return Counter(workload)


def store_workload(workload: dict, output_p: str):
    with open(output_p, "w") as f:
        json.dump(workload, f)


def load_workload(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def filter_by_workload(threshold, workload, reviewers):
    """
    filter reviewers according to the workload threshold
    param workload: workload dict, output of load_workload()
    param reviewers: dict whose key is reviewer/ reviewer pair, value is expertise
    """
    res = dict()
    for reviewer in reviewers.keys():
        if workload.get(reviewer, 0) <= threshold:
            res[reviewer] = reviewers[reviewer]
    return res
