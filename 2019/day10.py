from numpy import ones,vstack
from numpy.linalg import lstsq

test = """.#..#
.....
#####
....#
...##"""

lines = test.split('\n')
asteroids = []

for y in range(0, len(lines)):
    for x, elem in enumerate(lines[y]):
        if elem == '.':
            continue
        elif elem == '#':
            asteroids.append((x, y))
        else:
            print("input data not valid")
            break

equations, eq = [], []

for ast in asteroids:
    (x, y) = ast
    for i in range(1, len(asteroids)):
        (x1, y1) = asteroids[i]
        points = [ast, asteroids[i]]
        x_coords, y_coords = zip(*points)
        A = vstack([x_coords,ones(len(x_coords))]).T
        m, c = lstsq(A, y_coords)[0]
        m = float("{0:.4f}".format(m))
        c = float("{0:.4f}".format(c))
        equations.append((m, c))

        # if x == x1 or y == y1:
        #     a = 0
        # else:
        #     a = (x1 - x) / (y1 - y)
        #     a = float("{0:.4f}".format(a))
        # b = y - (a * x)
        # b = a = float("{0:.4f}".format(b))
        # equations.append((a, b))
    eq.append(len(set(equations)))
    equations = []


print(max(eq))

# for i, pair in enumerate(asteroids):
#     (x, y) = pair
#     print(pair)
