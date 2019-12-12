from numpy import ones,vstack
from numpy.linalg import lstsq
import math as m
from operator import itemgetter

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []

    def check_if_neighoburs(self, asteroid):
        dx = (asteroid.x - self.x)
        dy = (asteroid.y - self.y)
        if dx == dy == 0:
            return
        if dx > 0:
            sign = 1
        elif dx < 0:
            sign = -1
        try:
            slope = dy / dx
        except ZeroDivisionError:
            if dx == 0 and dy > 0:
                sign = -1
                slope = -999
            else:
                sign = 1
                slope = -999
        self.neighbours.append((slope, sign))

    def get_neighbours(self):
        return set(self.neighbours)


test = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
data = """#.#....#.#......#.....#......####.
#....#....##...#..#..##....#.##..#
#.#..#....#..#....##...###......##
...........##..##..##.####.#......
...##..##....##.#.....#.##....#..#
..##.....#..#.......#.#.........##
...###..##.###.#..................
.##...###.#.#.......#.#...##..#.#.
...#...##....#....##.#.....#...#.#
..##........#.#...#..#...##...##..
..#.##.......#..#......#.....##..#
....###..#..#...###...#.###...#.##
..#........#....#.....##.....#.#.#
...#....#.....#..#...###........#.
.##...#........#.#...#...##.......
.#....#.#.#.#.....#...........#...
.......###.##...#..#.#....#..##..#
#..#..###.#.......##....##.#..#...
..##...#.#.#........##..#..#.#..#.
.#.##..#.......#.#.#.........##.##
...#.#.....#.#....###.#.........#.
.#..#.##...#......#......#..##....
.##....#.#......##...#....#.##..#.
#..#..#..#...........#......##...#
#....##...#......#.###.#..#.#...#.
#......#.#.#.#....###..##.##...##.
......#.......#.#.#.#...#...##....
....##..#.....#.......#....#...#..
.#........#....#...#.#..#....#....
.#.##.##..##.#.#####..........##..
..####...##.#.....##.............#
....##......#.#..#....###....##...
......#..#.#####.#................
.#....#.#..#.###....##.......##.#."""

lines = data.split('\n')
asteroids = []
insight = []

for y in range(0, len(lines)):
    for x, elem in enumerate(lines[y]):
        if elem == '.':
            continue
        elif elem == '#':
            asteroids.append(Asteroid(x, y))
        else:
            print("input data not valid")
            break

for ast in asteroids:
    for i in range(0, len(asteroids)):
        ast.check_if_neighoburs(asteroids[i])
    insight.append(len(ast.get_neighbours()))

print('Part 1: ', max(insight))

target = asteroids[insight.index(max(insight))].neighbours.copy()
target = list(set(target))
target.sort(key=itemgetter(0))
target.sort(key=itemgetter(1),reverse=True)
print('Part 2: ', asteroids[asteroids[insight.index(max(insight))].neighbours.index(target[199])].x * 100 + asteroids[asteroids[insight.index(max(insight))].neighbours.index(target[199])].y)




