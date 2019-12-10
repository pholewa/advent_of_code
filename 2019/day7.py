from itertools import permutations


class Intcode:
    def __init__(self, instructions):
        self.instructions = instructions
        self.instruction_pointer = 0
        self.opcode = -1
        self.output = -1
        self.inputs = []
        self.modes = []

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
        # print(value)
        return value

    def provide_output(self, value):
        if self.modes[-1] == 0:
            value = self.instructions[value]
        self.output = value
        self.instruction_pointer += 2

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

    def get_amp_output(self, inputs):
        self.inputs = inputs
        self.get_opcode()
        while self.opcode != 99:
            if self.opcode == 1:
                self.get_param_mode()
                self.sum_and_store(self.instructions[self.instruction_pointer + 1],
                                   self.instructions[self.instruction_pointer + 2],
                                   self.instructions[self.instruction_pointer + 3])
            elif self.opcode == 2:
                self.get_param_mode()
                self.multiply_and_save(self.instructions[self.instruction_pointer + 1],
                                       self.instructions[self.instruction_pointer + 2],
                                       self.instructions[self.instruction_pointer + 3])
            elif self.opcode == 3:
                try:
                    self.store_input(self.instructions[self.instruction_pointer + 1], self.inputs)
                    del self.inputs[0]
                except IndexError:
                    return self.output
            elif self.opcode == 4:
                self.get_param_mode()
                self.provide_output(self.instructions[self.instruction_pointer + 1])
            elif self.opcode == 5:
                self.get_param_mode()
                self.jump_if_true(self.instructions[self.instruction_pointer + 1],
                                  self.instructions[self.instruction_pointer + 2])
            elif self.opcode == 6:
                self.get_param_mode()
                self.jump_if_false(self.instructions[self.instruction_pointer + 1],
                                   self.instructions[self.instruction_pointer + 2])
            elif self.opcode == 7:
                self.get_param_mode()
                self.check_less_than(self.instructions[self.instruction_pointer + 1],
                                     self.instructions[self.instruction_pointer + 2],
                                     self.instructions[self.instruction_pointer + 3])
            elif self.opcode == 8:
                self.get_param_mode()
                self.check_equality(self.instructions[self.instruction_pointer + 1],
                                    self.instructions[self.instruction_pointer + 2],
                                    self.instructions[self.instruction_pointer + 3])
            elif self.opcode == 9:
                pass  # handling relative mode

            self.get_opcode()
        return self.output


data = [3,8,1001,8,10,8,105,1,0,0,21,42,51,76,101,118,199,280,361,442,99999,3,9,101,5,9,9,102,2,9,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,1002,9,3,9,4,9,99,3,9,1002,9,4,9,1001,9,3,9,1002,9,5,9,101,3,9,9,1002,9,2,9,4,9,99,3,9,101,4,9,9,1002,9,2,9,1001,9,3,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,101,3,9,9,1002,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99]
test = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
test_cp = test.copy()

# inputs = []
# for i in range(0, 5):
#     amplifiers.append(Intcode(data.copy()))
#     inputs.append(9 - i)
#     amplifiers[i].get_amp_output(inputs)

    # amps[i].get_amp_output(9-i)
amplifiers, inputs, results = [], [], []
phases = [9,8,7,6,5]
amp = 0
for comb in list(permutations(phases, 5)):
    for i in range(0, 5):
        amplifiers.append(Intcode(data.copy()))
    for phase in range(0, len(comb)):
        inputs.append(comb[phase])
        amplifiers[amp % 5].get_amp_output(inputs)
        amp += 1
    inputs = [0]
    while amplifiers[-1].opcode != 99:
        inputs.append(amplifiers[amp % 5].get_amp_output(inputs))
        amp += 1
    results.append(amplifiers[-1].output)
    amplifiers, inputs = [], []
    amp = 0

print(max(results))



# computer = Intcode(test_cp)
# computer.get_opcode()
# phases = [9,8,7,6,5]
# outputs = [0]
# input_counter = 0


# def get_amp_output(phase, inp, input_counter):
#     while computer.opcode != 99:
#         if computer.opcode == 1:
#             computer.param_mode()
#             computer.sum_and_store(computer.instructions[computer.instruction_pointer + 1],
#                                    computer.instructions[computer.instruction_pointer + 2],
#                                    computer.instructions[computer.instruction_pointer + 3])
#         elif computer.opcode == 2:
#             computer.param_mode()
#             computer.multiply_and_save(computer.instructions[computer.instruction_pointer + 1],
#                                        computer.instructions[computer.instruction_pointer + 2],
#                                        computer.instructions[computer.instruction_pointer + 3])
#         elif computer.opcode == 3:
#             if input_counter % 2 == 0:
#                 computer.store_input(computer.instructions[computer.instruction_pointer + 1], phase)
#                 # del phases[0]
#             else:
#                 computer.store_input(computer.instructions[computer.instruction_pointer + 1], inp)
#                 # del outputs[0]
#             input_counter += 1
#         elif computer.opcode == 4:
#             computer.param_mode()
#             outputs.append(computer.show_value(computer.instructions[computer.instruction_pointer + 1]))
#             computer.instruction_pointer += 2
#         elif computer.opcode == 5:
#             computer.param_mode()
#             computer.jump_if_true(computer.instructions[computer.instruction_pointer + 1],
#                                   computer.instructions[computer.instruction_pointer + 2])
#         elif computer.opcode == 6:
#             computer.param_mode()
#             computer.jump_if_false(computer.instructions[computer.instruction_pointer + 1],
#                                    computer.instructions[computer.instruction_pointer + 2])
#         elif computer.opcode == 7:
#             computer.param_mode()
#             computer.check_less_than(computer.instructions[computer.instruction_pointer + 1],
#                                      computer.instructions[computer.instruction_pointer + 2],
#                                      computer.instructions[computer.instruction_pointer + 3])
#         elif computer.opcode == 8:
#             computer.param_mode()
#             computer.check_equality(computer.instructions[computer.instruction_pointer + 1],
#                                     computer.instructions[computer.instruction_pointer + 2],
#                                     computer.instructions[computer.instruction_pointer + 3])
#
#         computer.get_opcode()
#     return outputs[-1]

# res = []
# for comb in list(permutations(phases, 5)):
#     for amps in range(0, len(comb)):
#         test_cp = test.copy()
#         computer = Intcode(test_cp)
#         computer.get_opcode()
#         res.append(get_amp_output(comb[amps], outputs[-1], 0))
#     outputs = [outputs[-1]]
# print(max(res))
#
