from datetime import date, datetime
import calendar

abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}


def format_committime(t: str) -> date:
    '''
    commit time format
    e.g. Thu, 30 Mar 2017 10:44:25 -0700 ->2017-03-30
    '''
    if not t:
        return None
    t = t.split(" ")[1:4]
    return date(int(t[2]), abbr_to_num[t[1]], int(t[0]))


def format_prtime(t: str) -> str:
    '''
    pull request time format
    e.g. 2021-05-15T13:34:55Z ->2021-05-15
    '''
    if not t:
        return None
    t = t.split("T")[0].split("-")
    return date(int(t[0]), int(t[1]), int(t[2])).__str__()


def to_datetime(t):
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
