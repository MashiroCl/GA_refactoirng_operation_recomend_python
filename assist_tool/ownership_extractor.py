import csv

def extract_highest(filepath):
    res = []
    with open(filepath) as f:
        data = list(csv.reader(f))
        highest =0
        temp = None
        for i,v in enumerate(data):
            cur_path = data[i][0]
            if i==0:
                continue
            if i==1:
                last_path = cur_path
                highest = float(data[i][3])
                temp = data[i]
                continue
            if cur_path != last_path:
                res.append(temp)
                highest = float(data[i][3])
                temp = data[i]
            else:
                if float(data[i][3])>highest:
                    highest = float(data[i][3])
                    temp = data[i]
            last_path = cur_path
    return res

# filepath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv_utils/ownership.csv_utils"
# res = extract_highest(filepath)
# owner = ['Benjamin Diedrichsen', 'benni', 'bennidi']
# # owner = ['']
# count = 0
# for each in res:
#     if each[2] in owner:
#         count += 1
# print(count/len(res))
print(0.00045452840601609146+0.002137751630204715+0.000572246065808274+0.0005020477000812207+0.0007099132645294048-1.6527833565760375e-05)