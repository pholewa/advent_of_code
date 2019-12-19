from copy import deepcopy
import math

class Moon:
    def __init__(self, pos_x, pos_y, pos_z):
        self.pos_x, self.pos_y, self.pos_z = pos_x, pos_y, pos_z
        self.vel_x, self.vel_y, self.vel_z = 0, 0, 0
        self.pot, self.kin = 0, 0

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

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

data = """<x=6, y=-2, z=-7>
<x=-6, y=-7, z=-4>
<x=-9, y=11, z=0>
<x=-3, y=-4, z=6>"""
test = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

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


# print(lcm(33,43))
i = 1
# for m in moons:
#     m.calculate_velocity(moons)
# for m in moons:
#     m.update_position()
for i in range(0, STEPS):
# while not(moons[0].vel_x == 0 and moons[0].vel_y == 0 and moons[0].vel_z == 0):
    for m in moons:
        m.calculate_velocity(moons)
    for m in moons:
        m.update_position()
    # i += 1
# print("Come back to initials after ", i, " steps")

energy = []
for m in moons:
    energy.append(m.calculate_energy())
print("total energy: ", sum(energy))
