

test_data = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

input_data ="""Step W must be finished before step G can begin.
Step N must be finished before step X can begin.
Step M must be finished before step O can begin.
Step S must be finished before step I can begin.
Step F must be finished before step Y can begin.
Step Q must be finished before step K can begin.
Step K must be finished before step Y can begin.
Step Z must be finished before step J can begin.
Step G must be finished before step L can begin.
Step J must be finished before step C can begin.
Step R must be finished before step E can begin.
Step X must be finished before step I can begin.
Step P must be finished before step E can begin.
Step V must be finished before step Y can begin.
Step C must be finished before step I can begin.
Step O must be finished before step H can begin.
Step T must be finished before step B can begin.
Step Y must be finished before step A can begin.
Step E must be finished before step L can begin.
Step B must be finished before step D can begin.
Step L must be finished before step U can begin.
Step A must be finished before step I can begin.
Step I must be finished before step D can begin.
Step H must be finished before step D can begin.
Step U must be finished before step D can begin.
Step B must be finished before step I can begin.
Step S must be finished before step F can begin.
Step M must be finished before step R can begin.
Step A must be finished before step H can begin.
Step Z must be finished before step O can begin.
Step K must be finished before step I can begin.
Step K must be finished before step D can begin.
Step B must be finished before step A can begin.
Step G must be finished before step I can begin.
Step Z must be finished before step B can begin.
Step R must be finished before step P can begin.
Step J must be finished before step E can begin.
Step R must be finished before step I can begin.
Step Q must be finished before step U can begin.
Step S must be finished before step Z can begin.
Step E must be finished before step I can begin.
Step F must be finished before step E can begin.
Step F must be finished before step I can begin.
Step S must be finished before step J can begin.
Step O must be finished before step I can begin.
Step V must be finished before step B can begin.
Step A must be finished before step U can begin.
Step M must be finished before step T can begin.
Step K must be finished before step A can begin.
Step L must be finished before step I can begin.
Step I must be finished before step U can begin.
Step G must be finished before step U can begin.
Step B must be finished before step U can begin.
Step E must be finished before step D can begin.
Step J must be finished before step T can begin.
Step M must be finished before step Y can begin.
Step P must be finished before step B can begin.
Step M must be finished before step S can begin.
Step E must be finished before step U can begin.
Step R must be finished before step Y can begin.
Step J must be finished before step I can begin.
Step J must be finished before step D can begin.
Step Y must be finished before step E can begin.
Step A must be finished before step D can begin.
Step X must be finished before step H can begin.
Step O must be finished before step E can begin.
Step E must be finished before step B can begin.
Step E must be finished before step A can begin.
Step F must be finished before step U can begin.
Step G must be finished before step J can begin.
Step M must be finished before step Z can begin.
Step Y must be finished before step U can begin.
Step Y must be finished before step D can begin.
Step S must be finished before step D can begin.
Step G must be finished before step H can begin.
Step C must be finished before step Y can begin.
Step B must be finished before step H can begin.
Step P must be finished before step V can begin.
Step M must be finished before step K can begin.
Step L must be finished before step A can begin.
Step G must be finished before step A can begin.
Step Q must be finished before step P can begin.
Step P must be finished before step I can begin.
Step H must be finished before step U can begin.
Step G must be finished before step X can begin.
Step L must be finished before step H can begin.
Step X must be finished before step P can begin.
Step Z must be finished before step Y can begin.
Step N must be finished before step K can begin.
Step Q must be finished before step X can begin.
Step X must be finished before step L can begin.
Step T must be finished before step Y can begin.
Step P must be finished before step A can begin.
Step C must be finished before step T can begin.
Step J must be finished before step V can begin.
Step X must be finished before step O can begin.
Step S must be finished before step C can begin.
Step R must be finished before step C can begin.
Step E must be finished before step H can begin.
Step V must be finished before step H can begin.
Step L must be finished before step D can begin."""

data = input_data.splitlines()
needs = {}
steps = set()

for line in data:
    line = line.split(' ')
    if line[7] in needs:
        needs[line[7]].append(line[1])
    else:
        needs[line[7]] = [line[1]]
    steps.add(line[7])
    steps.add(line[1])

# candidates = [i for i in steps if i not in needs.keys()]
# first.sort()
# result = [first.pop(0)]
# available = first
done = set()
seconds = 0
counts = [0] * 5
work = [''] * 5

while True:
    for i, count in enumerate(counts):
        if count == 1:
            done.add(work[i])
            for key in needs.keys():
                if work[i] in needs[key]:
                    needs[key].remove(work[i])
            needs = {k: v for k, v in needs.items() if v != []}
        counts[i] = max(0, count - 1)
    while 0 in counts:
        i = counts.index(0)
        candidates = [x for x in steps if x not in needs.keys()]
        if not candidates:
            break
        task = min(candidates)
        steps.remove(task)
        counts[i] = ord(task) - ord('A') + 61
        work[i] = task
    if sum(counts) == 0:
        break
    seconds += 1

print(seconds)



# part 1
# for step in range(len(steps) - 1):
#     for key in needs.keys():
#         if result[-1] in needs[key]:
#             needs[key].remove(result[-1])
#             if needs[key] == []:
#                 available.append(key)
#     available.sort()
#     result.append(available.pop(0))
#     needs = {k: v for k, v in needs.items() if v != []}

# print(''.join(result))
pass

