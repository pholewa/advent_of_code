from itertools import permutations

class Intcode:
    def __init__(self, instructions):
        self.instructions = instructions
        self.instruction_pointer = 0
        self.opcode = 0
        self.modes = []

    def get_opcode(self):
        self.opcode = self.instructions[self.instruction_pointer] % 100

    def param_mode(self):
        self.modes = list(map(int, str(int(self.instructions[self.instruction_pointer]/100))))
        while len(self.modes) < 3:
            self.modes = [0] + self.modes

    def store_input(self, address, value):
        self.instructions[address] = value
        self.instruction_pointer += 2

    def show_value(self, value):
        if self.modes[-1] == 0:
            value = self.instructions[value]
        # print(value)
        return value

    def sum_and_store(self, a, b, address):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        self.instructions[address] = a + b
        self.instruction_pointer += 4

    def multiply_and_save(self, a, b, address):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        self.instructions[address] = a * b
        self.instruction_pointer += 4

    def jump_if_true(self, a, b):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        if a != 0:
            self.instruction_pointer = b
        else:
            self.instruction_pointer += 3

    def jump_if_false(self, a, b):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        if a == 0:
            self.instruction_pointer = b
        else:
            self.instruction_pointer += 3

    def check_less_than(self, a, b, address):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        if a < b:
            self.instructions[address] = 1
        else:
            self.instructions[address] = 0
        self.instruction_pointer += 4

    def check_equality(self, a, b, address):
        if self.modes[-1] == 0:
            a = self.instructions[a]
        if self.modes[-2] == 0:
            b = self.instructions[b]
        if a == b:
            self.instructions[address] = 1
        else:
            self.instructions[address] = 0
        self.instruction_pointer += 4


data = [3,8,1001,8,10,8,105,1,0,0,21,42,51,76,101,118,199,280,361,442,99999,3,9,101,5,9,9,102,2,9,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,1002,9,3,9,4,9,99,3,9,1002,9,4,9,1001,9,3,9,1002,9,5,9,101,3,9,9,1002,9,2,9,4,9,99,3,9,101,4,9,9,1002,9,2,9,1001,9,3,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99]
# data_input = [3,225,1,225,6,6,1100,1,238,225,104,0,1001,152,55,224,1001,224,-68,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,62,41,225,1101,83,71,225,102,59,147,224,101,-944,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,2,40,139,224,1001,224,-3905,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,6,94,224,101,-100,224,224,4,224,1002,223,8,223,101,6,224,224,1,224,223,223,1102,75,30,225,1102,70,44,224,101,-3080,224,224,4,224,1002,223,8,223,1001,224,4,224,1,223,224,223,1101,55,20,225,1102,55,16,225,1102,13,94,225,1102,16,55,225,1102,13,13,225,1,109,143,224,101,-88,224,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1002,136,57,224,101,-1140,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,101,76,35,224,1001,224,-138,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1006,224,329,1001,223,1,223,8,677,226,224,102,2,223,223,1006,224,344,101,1,223,223,1107,226,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,389,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,404,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,419,1001,223,1,223,8,226,677,224,102,2,223,223,1005,224,434,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,449,1001,223,1,223,7,677,677,224,102,2,223,223,1006,224,464,1001,223,1,223,8,226,226,224,1002,223,2,223,1005,224,479,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,494,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,102,2,223,223,1006,224,539,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,554,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,569,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,226,677,224,102,2,223,223,1005,224,599,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,614,101,1,223,223,108,677,226,224,102,2,223,223,1005,224,629,101,1,223,223,107,226,677,224,102,2,223,223,1006,224,644,1001,223,1,223,1108,226,226,224,1002,223,2,223,1006,224,659,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226]
test = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
test_cp = test.copy()

computer = Intcode(test_cp)
computer.get_opcode()
phases = [9,8,7,6,5]
outputs = [0]
input_counter = 0


def get_amp_output(phase, inp, input_counter):
    while computer.opcode != 99:
        if computer.opcode == 1:
            computer.param_mode()
            computer.sum_and_store(computer.instructions[computer.instruction_pointer + 1],
                                   computer.instructions[computer.instruction_pointer + 2],
                                   computer.instructions[computer.instruction_pointer + 3])
        elif computer.opcode == 2:
            computer.param_mode()
            computer.multiply_and_save(computer.instructions[computer.instruction_pointer + 1],
                                       computer.instructions[computer.instruction_pointer + 2],
                                       computer.instructions[computer.instruction_pointer + 3])
        elif computer.opcode == 3:
            if input_counter % 2 == 0:
                computer.store_input(computer.instructions[computer.instruction_pointer + 1], phase)
                # del phases[0]
            else:
                computer.store_input(computer.instructions[computer.instruction_pointer + 1], inp)
                # del outputs[0]
            input_counter += 1
        elif computer.opcode == 4:
            computer.param_mode()
            outputs.append(computer.show_value(computer.instructions[computer.instruction_pointer + 1]))
            computer.instruction_pointer += 2
        elif computer.opcode == 5:
            computer.param_mode()
            computer.jump_if_true(computer.instructions[computer.instruction_pointer + 1],
                                  computer.instructions[computer.instruction_pointer + 2])
        elif computer.opcode == 6:
            computer.param_mode()
            computer.jump_if_false(computer.instructions[computer.instruction_pointer + 1],
                                   computer.instructions[computer.instruction_pointer + 2])
        elif computer.opcode == 7:
            computer.param_mode()
            computer.check_less_than(computer.instructions[computer.instruction_pointer + 1],
                                     computer.instructions[computer.instruction_pointer + 2],
                                     computer.instructions[computer.instruction_pointer + 3])
        elif computer.opcode == 8:
            computer.param_mode()
            computer.check_equality(computer.instructions[computer.instruction_pointer + 1],
                                    computer.instructions[computer.instruction_pointer + 2],
                                    computer.instructions[computer.instruction_pointer + 3])

        computer.get_opcode()
    return outputs[-1]

res = []
for comb in list(permutations(phases, 5)):
    for amps in range(0, len(comb)):
        test_cp = test.copy()
        computer = Intcode(test_cp)
        computer.get_opcode()
        res.append(get_amp_output(comb[amps], outputs[-1], 0))
    outputs = [outputs[-1]]
print(max(res))

