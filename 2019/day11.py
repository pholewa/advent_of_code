from collections import defaultdict
import matplotlib.pyplot as plt

class Intcode:
    def __init__(self, instructions):
        self.instructions = instructions
        self.instruction_pointer = 0
        self.opcode = -1
        self.output = []
        self.relative_base = 0
        self.inputs = []
        self.modes = []
        self.direction = 0      #0 - up, 1 - right, 2 - down, 3 - left
        self.x = 0
        self.y = 0
        self.points = defaultdict(int)

    def get_opcode(self):
        self.opcode = self.instructions[self.instruction_pointer] % 100

    def get_param_mode(self):
        self.modes = list(map(int, str(int(self.instructions[self.instruction_pointer]/100))))
        while len(self.modes) < 3:
            self.modes = [0] + self.modes

    def store_input(self, address, value):
        self.instructions[address] = value[0]
        self.instruction_pointer += 2

    def show_value(self, value):
        if self.modes[-1] == 0:
            value = self.instructions[value]
        elif self.modes[-1] == 2:
            value = self.instructions[self.relative_base + value]
        # print(value)
        return value

    def provide_output(self, value):
        if self.modes[-1] == 0:
            value = self.instructions[value]
        elif self.modes[-1] == 2:
            value = self.instructions[self.relative_base + value]
        self.output.append(value)
        # print(value)
        self.instruction_pointer += 2
        if len(self.output) == 2:
            if self.output[-1] == 0:
                self.direction = (self.direction - 1) % 4       #turn left
            elif self.output[-1] == 1:
                self.direction = (self.direction + 1) % 4       #turn right
            self.points[(self.x, self.y)] = self.output[0]     #.append(Point(self.x, self.y, self.output[0]))
            self.update_position()
            self.output = []

    def update_position(self):
        if self.direction == 0:
            self.y += 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y -= 1
        elif self.direction == 3:
            self.x -= 1

    def sum_and_store(self, a, b, address):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        elif self.modes[-1] == 2:
            a = self.instructions[self.relative_base + a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        elif self.modes[-2] == 2:
            b = self.instructions[self.relative_base + b]
        if self.modes[-3] == 2:
            address += self.relative_base
        self.instructions[address] = a + b
        self.instruction_pointer += 4

    def multiply_and_save(self, a, b, address):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        elif self.modes[-1] == 2:
            a = self.instructions[self.relative_base + a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        elif self.modes[-2] == 2:
            b = self.instructions[self.relative_base + b]
        if self.modes[-3] == 2:
            address += self.relative_base
        self.instructions[address] = a * b
        self.instruction_pointer += 4

    def jump_if_true(self, a, b):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        elif self.modes[-1] == 2:
            a = self.instructions[self.relative_base + a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        elif self.modes[-2] == 2:
            b = self.instructions[self.relative_base + b]
        if a != 0:
            self.instruction_pointer = b
        else:
            self.instruction_pointer += 3

    def jump_if_false(self, a, b):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        elif self.modes[-1] == 2:
            a = self.instructions[self.relative_base + a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        elif self.modes[-2] == 2:
            b = self.instructions[self.relative_base + b]
        if a == 0:
            self.instruction_pointer = b
        else:
            self.instruction_pointer += 3

    def check_less_than(self, a, b, address):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        elif self.modes[-1] == 2:
            a = self.instructions[self.relative_base + a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        elif self.modes[-2] == 2:
            b = self.instructions[self.relative_base + b]
        if self.modes[-3] == 2:
            address += self.relative_base
        if a < b:
            self.instructions[address] = 1
        else:
            self.instructions[address] = 0
        self.instruction_pointer += 4

    def check_equality(self, a, b, address):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        elif self.modes[-1] == 2:
            a = self.instructions[self.relative_base + a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        elif self.modes[-2] == 2:
            b = self.instructions[self.relative_base + b]
        if self.modes[-3] == 2:
            address += self.relative_base
        if a == b:
            self.instructions[address] = 1
        else:
            self.instructions[address] = 0
        self.instruction_pointer += 4

    def change_relative_base(self, param):
        if self.modes[-1] == 0:
            param = self.instructions[param]
        elif self.modes[-1] == 2:
            param = self.instructions[self.relative_base + param]
        self.relative_base += param
        self.instruction_pointer += 2

    # def parse_output(self):
    #     if self.output[0] ==

    def get_amp_output(self, inputs):
        self.inputs = inputs
        self.get_opcode()
        self.get_param_mode()
        while self.opcode != 99:
            if self.opcode == 1:
                self.sum_and_store(self.instructions[self.instruction_pointer + 1],
                                   self.instructions[self.instruction_pointer + 2],
                                   self.instructions[self.instruction_pointer + 3])
            elif self.opcode == 2:
                self.multiply_and_save(self.instructions[self.instruction_pointer + 1],
                                       self.instructions[self.instruction_pointer + 2],
                                       self.instructions[self.instruction_pointer + 3])
            elif self.opcode == 3:
                if self.modes[-1] == 2:
                    address = self.relative_base + self.instructions[self.instruction_pointer + 1]
                elif self.modes[-1] == 0:
                    address = self.instructions[self.instruction_pointer + 1]
                try:
                    if self.inputs == []:
                        self.inputs.append(self.points[(self.x, self.y)])
                    self.store_input(address, self.inputs)
                    del self.inputs[0]
                except IndexError:
                    return self.output
            elif self.opcode == 4:
                self.provide_output(self.instructions[self.instruction_pointer + 1])
            elif self.opcode == 5:
                self.jump_if_true(self.instructions[self.instruction_pointer + 1],
                                  self.instructions[self.instruction_pointer + 2])
            elif self.opcode == 6:
                self.jump_if_false(self.instructions[self.instruction_pointer + 1],
                                   self.instructions[self.instruction_pointer + 2])
            elif self.opcode == 7:
                self.check_less_than(self.instructions[self.instruction_pointer + 1],
                                     self.instructions[self.instruction_pointer + 2],
                                     self.instructions[self.instruction_pointer + 3])
            elif self.opcode == 8:
                self.check_equality(self.instructions[self.instruction_pointer + 1],
                                    self.instructions[self.instruction_pointer + 2],
                                    self.instructions[self.instruction_pointer + 3])
            elif self.opcode == 9:
                self.change_relative_base(self.instructions[self.instruction_pointer + 1])

            self.get_opcode()
            self.get_param_mode()
        return self.output


data = [3,8,1005,8,352,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,28,1,1003,20,10,2,106,11,10,2,1107,1,10,1,1001,14,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,67,2,1009,7,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,92,1,105,9,10,1006,0,89,1,108,9,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,126,1,1101,14,10,1,1005,3,10,1006,0,29,1006,0,91,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,161,1,1,6,10,1006,0,65,2,106,13,10,1006,0,36,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,198,1,105,15,10,1,1004,0,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,228,2,1006,8,10,2,1001,16,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,257,1006,0,19,2,6,10,10,2,4,13,10,2,1002,4,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,295,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,316,2,101,6,10,1006,0,84,2,1004,13,10,1,1109,3,10,101,1,9,9,1007,9,1046,10,1005,10,15,99,109,674,104,0,104,1,21101,387365315340,0,1,21102,369,1,0,1105,1,473,21101,666685514536,0,1,21102,380,1,0,1106,0,473,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,46266346536,1,21102,427,1,0,1105,1,473,21101,235152829659,0,1,21101,438,0,0,1105,1,473,3,10,104,0,104,0,3,10,104,0,104,0,21102,838337188620,1,1,21101,461,0,0,1105,1,473,21102,988753429268,1,1,21102,1,472,0,1106,0,473,99,109,2,22101,0,-1,1,21101,40,0,2,21101,504,0,3,21102,494,1,0,1106,0,537,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,499,500,515,4,0,1001,499,1,499,108,4,499,10,1006,10,531,1101,0,0,499,109,-2,2106,0,0,0,109,4,2101,0,-1,536,1207,-3,0,10,1006,10,554,21102,1,0,-3,21202,-3,1,1,21201,-2,0,2,21102,1,1,3,21101,573,0,0,1105,1,578,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,601,2207,-4,-2,10,1006,10,601,21201,-4,0,-4,1105,1,669,22101,0,-4,1,21201,-3,-1,2,21202,-2,2,3,21101,620,0,0,1106,0,578,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,639,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,661,22101,0,-1,1,21102,661,1,0,106,0,536,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]
boost = [0] * 10000
data += boost


amp = Intcode(data)
amp.get_amp_output([1])
print("part 1: ", len(amp.points))

x = [k[0] for k, v in amp.points.items() if v == 1]
y = [k[1] for k, v in amp.points.items() if v == 1]
plt.scatter(x, y)
plt.show()