import csv

def ownership2csv(ownerships: 'List[expertise.ownership.PersonalOwnership]', file):
    writer = csv.writer(file)
    if isinstance(ownerships, list):
        for each in ownerships:
            writer.writerow(each.tolist())


def pullrequest2csv(prs: 'List[collaboration.pullrequest.Pullrequest]', file):
    writer = csv.writer(file)
    if isinstance(prs, list):
        for pr in prs:
            writer.writerow(pr.to_list())
