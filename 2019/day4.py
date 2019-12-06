data = "153517-630395"
data = [int(elem) for elem in data.split('-')]

print(data)
res = []

for op in range(data[0], data[1] + 1):
    has_dbl = False
    decreases = True
    part_of_bg = False
    if len(set(str(op))) < 6:
        has_dbl = True
        for i in range(1, 6):
            if str(op)[i] < str(op)[i - 1]:
                decreases = False
                break




    else:
        continue
    if has_dbl and decreases:
        res.append(op)

print(len(res))