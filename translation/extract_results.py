def top_k(path, k: int):
    values = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        row = []
        for each in line.strip().split(" "):
            row.append(float(each))
        values.append(row)
    values = sorted(values, key=lambda x: x[0])
    k = min(k, len(values))
    return values[:k]



if __name__ =="__main__":
    pass
