class Time:
    def __init__(self):
        pass


class CommitTime(Time):
    def __init__(self, time:str):
        '''
        commit time format
        e.g. Thu, 30 Mar 2017 10:44:25 -0700
        '''
        reg = ""
        time.split()