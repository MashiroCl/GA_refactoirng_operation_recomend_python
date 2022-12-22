from typing import List
class PullRequest():
    def __init__(self,pullRequest_info:List[str]):
        self.url = pullRequest_info[0].strip()
        self.state = pullRequest_info[1].strip()
        self.proposer = pullRequest_info[2].strip().replace("\"","").replace(" ", "").replace("-", "").lower()
        self.proposed_time = pullRequest_info[3].replace("\"","").strip()[:10]
        self.commentators = [pullRequest_info[i].strip().replace(" ","").replace("-", "").replace("\"", "").lower() for i in range(len(pullRequest_info)) if i%2==0 and i>3]
        self.comment_timestamps = [pullRequest_info[i].replace("\"","").strip()[:10]\
                                   for i in range(len(pullRequest_info)) if i%2!=0 and i>1]
        self.num_of_participants = str((len(pullRequest_info)-2)/2)

    def __str__(self):
        return "url: "+self.url+" state: "+self.state +" proposer: "+self.proposer+" proposed_time: "+self.proposed_time \
               +" num_of_participants: "+self.num_of_participants + " commentators: "+str(self.commentators) + \
               " comment_timestamps"+str(self.comment_timestamps)

class PullRequestService():
    def __init__(self):
        pass

    def loadPullRequest(self,csv_path:str)->List[PullRequest]:
        '''
        load pull request information from csv_utils file
        :param csv_path:
        :return:
        '''
        with open(csv_path) as f:
            pull_requests = f.readlines()
        pull_request_list = list()
        for each_pullrequest in pull_requests:
            pull_request_list.append(PullRequest(list(filter(lambda x:x!=" \n",each_pullrequest.split(",")))))
        return pull_request_list

    def calculate_time_weight(self,proposed_time,baseline,deadline)->float:
        return (proposed_time-baseline)/(deadline-baseline)


