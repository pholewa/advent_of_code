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
        game.append(value)
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


data = [1,380,379,385,1008,2617,718741,381,1005,381,12,99,109,2618,1102,1,0,383,1102,0,1,382,20101,0,382,1,21001,383,0,2,21102,1,37,0,1105,1,578,4,382,4,383,204,1,1001,382,1,382,1007,382,43,381,1005,381,22,1001,383,1,383,1007,383,23,381,1005,381,18,1006,385,69,99,104,-1,104,0,4,386,3,384,1007,384,0,381,1005,381,94,107,0,384,381,1005,381,108,1105,1,161,107,1,392,381,1006,381,161,1101,0,-1,384,1105,1,119,1007,392,41,381,1006,381,161,1102,1,1,384,21002,392,1,1,21102,21,1,2,21101,0,0,3,21101,138,0,0,1105,1,549,1,392,384,392,20101,0,392,1,21101,21,0,2,21101,3,0,3,21102,161,1,0,1105,1,549,1101,0,0,384,20001,388,390,1,21001,389,0,2,21101,180,0,0,1105,1,578,1206,1,213,1208,1,2,381,1006,381,205,20001,388,390,1,20101,0,389,2,21101,0,205,0,1106,0,393,1002,390,-1,390,1101,0,1,384,20101,0,388,1,20001,389,391,2,21101,0,228,0,1105,1,578,1206,1,261,1208,1,2,381,1006,381,253,20101,0,388,1,20001,389,391,2,21101,253,0,0,1106,0,393,1002,391,-1,391,1101,1,0,384,1005,384,161,20001,388,390,1,20001,389,391,2,21101,0,279,0,1106,0,578,1206,1,316,1208,1,2,381,1006,381,304,20001,388,390,1,20001,389,391,2,21101,0,304,0,1105,1,393,1002,390,-1,390,1002,391,-1,391,1102,1,1,384,1005,384,161,20101,0,388,1,21001,389,0,2,21102,0,1,3,21101,0,338,0,1106,0,549,1,388,390,388,1,389,391,389,20101,0,388,1,20101,0,389,2,21102,4,1,3,21101,0,365,0,1106,0,549,1007,389,22,381,1005,381,75,104,-1,104,0,104,0,99,0,1,0,0,0,0,0,0,363,19,18,1,1,21,109,3,21201,-2,0,1,21202,-1,1,2,21102,1,0,3,21102,1,414,0,1105,1,549,21201,-2,0,1,21201,-1,0,2,21101,0,429,0,1105,1,601,1202,1,1,435,1,386,0,386,104,-1,104,0,4,386,1001,387,-1,387,1005,387,451,99,109,-3,2105,1,0,109,8,22202,-7,-6,-3,22201,-3,-5,-3,21202,-4,64,-2,2207,-3,-2,381,1005,381,492,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,481,21202,-4,8,-2,2207,-3,-2,381,1005,381,518,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,507,2207,-3,-4,381,1005,381,540,21202,-4,-1,-1,22201,-3,-1,-3,2207,-3,-4,381,1006,381,529,21202,-3,1,-7,109,-8,2105,1,0,109,4,1202,-2,43,566,201,-3,566,566,101,639,566,566,2102,1,-1,0,204,-3,204,-2,204,-1,109,-4,2105,1,0,109,3,1202,-1,43,593,201,-2,593,593,101,639,593,593,21001,0,0,-2,109,-3,2106,0,0,109,3,22102,23,-2,1,22201,1,-1,1,21102,1,499,2,21102,1,317,3,21102,989,1,4,21102,630,1,0,1105,1,456,21201,1,1628,-2,109,-3,2106,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,2,2,0,0,2,2,2,2,2,0,2,2,2,2,2,2,0,2,2,2,0,2,0,2,2,2,2,0,0,2,0,2,2,2,0,2,2,0,2,0,1,1,0,2,2,0,2,0,0,2,2,2,2,0,2,2,2,2,0,0,2,2,0,0,0,0,0,0,2,2,2,0,0,2,2,0,0,2,2,0,2,2,0,1,1,0,0,2,2,0,2,2,2,2,0,2,0,2,2,0,0,0,2,2,2,0,2,0,0,2,2,2,0,2,0,2,2,2,2,2,2,2,2,2,2,0,1,1,0,2,2,0,0,0,2,2,0,2,2,0,0,0,2,2,2,0,2,0,2,0,2,0,2,0,2,2,2,0,0,2,0,0,0,2,0,0,2,2,0,1,1,0,2,2,0,2,2,0,0,0,0,2,2,2,0,0,0,2,2,2,2,2,0,0,2,2,2,2,0,0,2,0,0,0,0,2,2,0,2,0,0,0,1,1,0,2,0,2,0,2,2,0,2,2,0,0,0,0,2,0,2,0,2,0,0,2,2,0,0,0,0,0,0,0,0,2,2,0,2,2,2,2,0,2,0,1,1,0,2,2,2,0,2,2,0,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,0,2,2,2,0,2,0,2,2,0,0,2,0,1,1,0,2,0,0,2,2,2,2,2,0,2,0,0,2,0,2,0,0,2,0,0,2,2,2,0,2,2,2,2,2,2,2,2,0,0,2,2,0,0,2,0,1,1,0,0,2,2,2,0,2,2,0,2,2,2,2,0,0,2,2,2,0,2,2,2,2,2,2,2,0,0,0,2,0,2,0,0,2,0,2,2,2,2,0,1,1,0,2,2,0,0,0,2,2,2,2,2,0,0,2,0,2,0,2,0,0,2,2,0,2,2,2,2,0,2,0,2,0,2,0,2,2,2,0,2,2,0,1,1,0,0,2,2,0,2,0,0,2,2,2,2,2,0,2,0,0,2,0,2,2,0,2,2,2,2,0,2,2,0,0,0,0,0,2,0,2,0,2,0,0,1,1,0,2,0,0,2,0,2,2,2,2,2,0,0,2,0,2,2,0,2,2,2,2,2,2,2,0,2,2,0,0,0,2,0,0,2,2,0,2,0,0,0,1,1,0,2,2,0,2,0,2,2,2,0,2,0,0,2,0,0,2,2,2,2,2,0,2,0,0,2,0,2,0,0,2,0,0,2,0,2,2,2,2,2,0,1,1,0,2,2,0,0,2,2,2,2,2,0,2,2,2,2,2,0,2,2,2,2,0,0,2,0,2,2,0,2,2,2,0,2,2,2,0,2,0,2,2,0,1,1,0,2,2,2,0,2,0,0,2,2,0,2,2,2,2,2,0,2,2,2,2,2,0,2,2,2,2,2,2,0,2,0,0,2,2,2,2,2,2,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,62,61,33,96,12,3,42,31,62,61,69,2,65,62,56,36,70,53,51,12,11,2,34,79,44,80,63,26,53,77,25,41,86,27,22,53,2,91,21,83,29,72,43,97,90,39,16,31,81,19,60,98,12,7,47,34,12,79,25,34,37,39,8,1,42,23,54,50,9,89,1,87,34,75,96,69,28,67,15,87,10,13,71,26,48,63,30,64,41,79,48,15,80,3,76,93,46,50,46,95,68,70,1,49,19,8,73,30,28,62,73,22,3,36,31,6,4,25,20,23,95,48,82,27,68,88,53,40,24,21,85,69,71,94,77,63,4,79,74,95,72,37,4,46,10,32,46,79,94,54,31,35,46,32,39,44,53,55,48,3,26,92,81,43,56,23,62,15,82,94,20,26,59,22,47,32,68,37,64,8,28,61,90,24,49,47,36,80,8,2,57,11,65,45,22,44,67,29,48,16,82,94,19,11,46,55,79,64,94,84,6,78,12,88,16,95,47,41,8,60,34,85,59,88,49,78,34,61,83,52,58,16,54,24,29,5,87,68,18,60,22,76,35,87,75,42,75,98,43,56,77,12,64,40,53,67,79,31,94,17,65,70,12,67,12,80,62,9,83,72,75,97,52,86,80,19,82,75,80,62,46,3,19,59,97,67,41,22,15,12,48,43,11,98,59,75,48,23,6,16,66,9,8,15,16,90,84,75,24,15,92,44,14,23,87,14,43,70,41,27,65,57,22,45,15,49,10,95,29,41,38,5,81,48,94,6,9,97,43,77,80,61,29,88,37,20,52,96,36,77,25,80,87,90,95,77,67,68,2,80,6,92,98,53,95,35,66,61,40,57,74,50,13,86,38,45,29,74,39,87,97,75,12,22,20,74,24,15,28,20,82,53,32,18,15,54,16,53,65,61,59,72,6,28,6,49,54,65,59,56,12,41,15,90,82,27,94,41,80,63,72,80,33,98,42,49,22,30,93,93,66,5,79,65,42,49,68,43,79,78,14,76,68,22,29,86,47,51,2,61,91,27,68,32,96,84,54,52,3,73,43,27,62,16,68,22,88,57,67,92,92,42,1,95,14,56,92,3,32,42,36,75,4,9,23,49,78,92,87,69,19,37,15,44,44,65,88,69,76,91,5,96,89,33,31,48,32,39,8,1,22,80,96,20,11,65,60,77,47,1,8,27,58,51,47,52,76,4,31,18,89,94,82,97,63,49,95,24,53,35,28,88,39,23,20,44,22,96,86,4,1,15,52,30,18,1,48,34,1,68,12,84,89,83,31,12,98,10,9,10,91,60,97,46,23,88,71,32,38,29,58,21,95,81,86,57,13,7,82,23,63,74,79,1,30,32,53,33,56,25,70,62,17,8,53,21,43,17,27,67,5,4,64,5,65,65,75,25,60,75,42,87,27,40,36,9,7,10,90,91,3,34,57,55,57,25,83,91,88,66,75,22,88,68,67,3,97,40,90,52,60,3,66,78,78,75,41,71,36,5,78,2,50,96,2,35,60,36,61,47,11,11,48,52,4,51,62,57,70,55,60,81,89,25,74,1,26,13,18,31,52,36,31,3,49,60,94,29,15,67,96,25,22,80,69,47,97,11,68,40,17,70,82,42,10,94,30,70,7,3,3,69,47,16,8,8,8,28,35,36,6,42,52,56,22,31,28,69,20,24,90,48,30,70,61,95,45,10,74,3,65,54,46,96,61,31,72,49,92,88,12,49,19,92,11,69,66,78,12,79,32,17,33,41,70,87,71,41,78,12,94,90,36,63,18,64,21,62,24,47,10,77,16,12,1,62,69,13,55,94,11,16,7,35,79,21,18,67,96,60,21,31,21,97,33,90,55,41,14,50,41,3,32,89,22,44,57,55,6,87,9,19,21,22,43,78,16,8,67,25,93,28,43,33,89,83,73,61,70,65,16,77,59,80,78,22,97,77,41,7,27,82,51,42,82,91,18,56,64,33,39,16,70,34,83,85,2,5,67,81,86,19,10,44,15,3,29,2,92,85,8,92,65,51,65,91,59,57,26,2,56,33,52,40,70,98,71,47,27,43,52,78,91,16,83,83,30,32,26,57,77,16,57,65,5,60,81,23,70,51,37,55,94,25,74,10,7,30,25,10,60,41,88,61,4,79,38,67,85,51,98,30,39,81,86,10,55,66,72,18,64,86,69,25,62,37,55,21,79,38,59,4,28,88,65,11,62,79,89,52,21,10,37,7,34,26,47,62,57,718741]
boost = [0] * 10000
data += boost
game = []

amp = Intcode(data)
amp.get_amp_output([])
del game[:2]
game = game[::3].count(2)
print('Block tiles counter: ', game)
