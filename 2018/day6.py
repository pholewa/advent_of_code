import numpy as np
from itertools import repeat
from scipy.spatial import distance
from operator import itemgetter
from collections import defaultdict
import fileinput
import re

test_data = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

input_data = """181, 47
337, 53
331, 40
137, 57
200, 96
351, 180
157, 332
113, 101
285, 55
189, 188
174, 254
339, 81
143, 61
131, 155
239, 334
357, 291
290, 89
164, 149
248, 73
311, 190
54, 217
285, 268
354, 113
318, 191
182, 230
156, 252
114, 232
159, 299
324, 280
152, 155
295, 293
194, 214
252, 345
233, 172
272, 311
230, 82
62, 160
275, 96
335, 215
185, 347
134, 272
58, 113
112, 155
220, 83
153, 244
279, 149
302, 167
185, 158
72, 91
264, 67"""

points = []
width, height = 0, 0
lines = input_data.splitlines()
for line in lines:
    width, height = list(map(int, line.split(',')))
    points.append((width, height))

# points = [tuple(map(int, re.findall(r'\d+', x))) for x in fileinput.input()]

x0, x1 = min(x for x, y in points), max(x for x, y in points)
y0, y1 = min(y for x, y in points), max(y for x, y in points)

def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# part 1
counts = defaultdict(int)
infinite = set()
for y in range(y0, y1 + 1):
    for x in range(x0, x1 + 1):
        ds = sorted((dist(x, y, px, py), i)
            for i, (px, py) in enumerate(points))
        if ds[0][0] != ds[1][0]:
            counts[ds[0][1]] += 1
            if x == x0 or y == y0 or x == x1 or y == y1:
                infinite.add(ds[0][1])
for k in infinite:
    counts.pop(k)
print(max(counts.values()))

# part 2
count = 0
for y in range(y0, y1 + 1):
    for x in range(x0, x1 + 1):
        if sum(dist(x, y, px, py) for px, py in points) < 10000:
            count += 1
print(count)

#

#
#
# def day6(data):
#     coordinates = []
#
#     width, height = 0, 0
#     lines = data.splitlines()
#     for line in lines:
#         width, height = list(map(int, line.split(',')))
#         coordinates.append((width, height))
#     matrix_h = max(coordinates, key=itemgetter(1))[0]
#     matrix_w = max(coordinates, key=itemgetter(1))[1]
#     # print(edited)
#     surface = np.zeros((height + 1, width + 1))
#     # for i, line in enumerate(lines):
#     #     edited.append(list(map(int, line.replace(',', '').split())))
#     #     if edited[i][0] > width:
#     #         width = edited[i][0]
#     #     if edited[i][1] > height:
#     #         height = edited[i][1]
#     #
#     # surface = np.zeros((height + 1, width + 1), dtype=int)
#     # for i in range(1, len(edited)+1):
#     #     surface[edited[i-1][1]][edited[i-1][0]] = i #chr(ord('A') + i) #for characters literal
#     #
#     # lengths = []
#     # for x in range(1, len(edited)+1):
#     #     itemindex = np.where(surface == x)
#     #     lengths.append([[distance.cityblock([line, element, 0], [itemindex[0][0], itemindex[1][0], 0] ) for element in range(surface.shape[1])]for line in range(surface.shape[0])])
#     #
#     # sur = [[[lengths[item][line][element] for item in range(len(lengths))]for element in range(surface.shape[1])]for line in range(surface.shape[0])]
#     # infinites = set()
#     # for y in range(surface.shape[0]):
#     #     for x in range(surface.shape[1]):
#     #         itemindex = np.where(sur[y][x] == min(sur[y][x]))
#     #         if len(itemindex[0]) == 1:
#     #             surface[y][x] = itemindex[0] + 1
#     #         if x == 0 or x == surface.shape[1] - 1 or y == 0 or y == surface.shape[0] - 1:
#     #             infinites.add(surface[y][x])
#     #
#     # unique, counts = np.unique(surface, return_counts=True)
#     # unique = list(set(unique) ^ infinites)
#     #
#     # a = dict(zip(unique, counts[unique]))
#     # print(max(a.values()))
#
#     pass
#
# day6(test_data)