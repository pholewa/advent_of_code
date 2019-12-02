data_input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,2,19,13,23,1,23,10,27,1,13,27,31,2,31,10,35,1,35,9,39,1,39,13,43,1,13,43,47,1,47,13,51,1,13,51,55,1,5,55,59,2,10,59,63,1,9,63,67,1,6,67,71,2,71,13,75,2,75,13,79,1,79,9,83,2,83,10,87,1,9,87,91,1,6,91,95,1,95,10,99,1,99,13,103,1,13,103,107,2,13,107,111,1,111,9,115,2,115,10,119,1,119,5,123,1,123,2,127,1,127,5,0,99,2,14,0,0]
data_input_copy = data_input.copy()
test = [1,1,1,4,99,5,6,0,99]

data_input[1] = 12
data_input[2] = 2
res1, res2 = 0, 0


def do_summation(a, b):
    return a + b


def do_multiplication(a, b):
    return a * b


def intcode(data, opcode, a_pos, b_pos, result_position):
    if opcode == 99:
        return
    elif opcode == 1:
        data[result_position] = do_summation(data[a_pos], data[b_pos])

    elif opcode == 2:
        data[result_position] = do_multiplication(data[a_pos], data[b_pos])



def check_pair(data, a, b):
    it = 0
    data[1] = a
    data[2] = b
    while data[it] != 99:
        intcode(data, data[it], data[it+1], data[it+2], data[it+3])
        it += 4
    return a, b

for x in range(0, 100):
    for y in range(0, 100):
        a, b = check_pair(data_input, x, y)
        if data_input[0] == 19690720:
            res1, res2 = x, y
            break
        data_input = data_input_copy.copy()


print(res1, res2)
print(data_input[0])