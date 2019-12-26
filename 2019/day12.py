from copy import deepcopy
from collections import defaultdict
import math

class Moon:
    def __init__(self, pos_x, pos_y, pos_z):
        self.pos_x, self.pos_y, self.pos_z = pos_x, pos_y, pos_z
        self.startX = deepcopy(self.pos_x)
        self.startY = deepcopy(self.pos_y)
        self.startZ = deepcopy(self.pos_z)
        self.vel_x, self.vel_y, self.vel_z = 0, 0, 0
        self.pot, self.kin = 0, 0
        self.periods = defaultdict(int)

    def __eq__(self, other):
        if not isinstance(other, Moon):
            return NotImplemented
        return self.pos_x == other.pos_x and self.pos_y == other.pos_y and self.pos_z == other.pos_z and \
               self.vel_x == other.vel_x and self.vel_y == other.vel_y and self.vel_z == other.vel_z

    def calculate_velocity(self, m):
        dx, dy, dz = 0, 0, 0
        for moon in m:
            if self.pos_x > moon.pos_x:
                dx -= 1
            elif self.pos_x < moon.pos_x:
                dx += 1
            if self.pos_y > moon.pos_y:
                dy -= 1
            elif self.pos_y < moon.pos_y:
                dy += 1
            if self.pos_z > moon.pos_z:
                dz -= 1
            elif self.pos_z < moon.pos_z:
                dz += 1
        self.vel_x += dx
        self.vel_y += dy
        self.vel_z += dz

    def update_position(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.pos_z += self.vel_z

    def calculate_energy(self):
        self.pot = abs(self.pos_x) + abs(self.pos_y) + abs(self.pos_z)
        self.kin = abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z)
        return self.pot * self.kin

    def check_period(self, position, start_pos, velocity):
        if position == start_pos:
            if velocity == 0:
                return True

    def is_at_start(self, start_state):
        if self.pos_x != start_state.pos_x or self.pos_y != start_state.pos_y or self.pos_z != start_state.pos_z:
            return False
        elif self.pos_x == start_state.pos_x \
            and self.pos_y == start_state.pos_y \
            and self.pos_z == start_state.pos_z \
            and self.vel_x == start_state.vel_x \
            and self.vel_y == start_state.vel_t \
            and self.vel_z == start_state.vel_z:
            return True

    def initialise_periods(self):
        self.periods['pos_x'] = 0
        self.periods['pos_y'] = 0
        self.periods['pos_z'] = 0

    def check_common_period(self, mns, axis):
        for mn in mns:
            if self.periods['pos_{axis}'.format(axis=axis)] != mn.periods['pos_{axis}'.format(axis=axis)] or self.periods['pos_{axis}'.format(axis=axis)] == 0:
                return False
        return True



def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

data = """<x=6, y=-2, z=-7>
<x=-6, y=-7, z=-4>
<x=-9, y=11, z=0>
<x=-3, y=-4, z=6>"""
test = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
# test = """<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>"""

data = data.splitlines()
moons, start_positions, initials = [], [], []
STEPS = 1000

for line in data:
    values = line.replace('<x=', '').replace('>', '').replace(' y=', '').replace(' z=', '').split(',')
    for elem in values:
        start_positions.append(int(elem))
    moons.append(Moon(start_positions[0], start_positions[1], start_positions[2]))
    initials.append(deepcopy(moons[-1]))
    start_positions = []

periods = 3 * [False]
# print(lcm(33,43))
loops = 1
for m in moons:
    m.initialise_periods()
    m.calculate_velocity(moons)
for m in moons:
    m.update_position()
# for i in range(0, STEPS):
while False in periods:
    for i, m in enumerate(moons):
        if m.check_period(m.pos_x, m.startX, m.vel_x):
            m.periods['pos_x'] = loops
        if m.check_period(m.pos_y, m.startY, m.vel_y):
            m.periods['pos_y'] = loops
        if m.check_period(m.pos_z, m.startZ, m.vel_z):
            m.periods['pos_z'] = loops
        if m.check_common_period(moons, 'x') and not periods[0]:
            periods[0] = loops
        if m.check_common_period(moons, 'y') and not periods[1]:
            periods[1] = loops
        if m.check_common_period(moons, 'z') and not periods[2]:
            periods[2] = loops
        m.calculate_velocity(moons)
    for i, m in enumerate(moons):
        m.update_position()

    loops += 1
print("Come back to initials after ", lcm(periods[0], lcm(periods[1], periods[2])) , " steps")

# energy = []
# for m in moons:
#     energy.append(m.calculate_energy())
# print("total energy: ", sum(energy))
