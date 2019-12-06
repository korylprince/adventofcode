def get_codes():
    with open("./input.txt") as f:
        return [int(i.strip()) for i in f.read().strip().split(",")]

def run(codes, input):
    output = None

    idx = 0
    while True:
        code = "{:0>5}".format(codes[idx])
        op = int(code[3:])
        if op == 99:
            break
        elif op == 1:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            codes[codes[idx+3]] = a + b
            idx += 4
        elif op == 2:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            codes[codes[idx+3]] = a * b
            idx += 4
        elif op == 3:
            codes[codes[idx+1]] = input
            idx += 2
        elif op == 4:
            a = codes[idx+1] if int(code[2]) else codes[codes[idx+1]]
            output = a
            idx += 2
        elif op == 5:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            if a != 0:
                idx = b
            else:
                idx += 3
        elif op == 6:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            if a == 0:
                idx = b
            else:
                idx += 3
        elif op == 7:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            codes[codes[idx+3]] = int(a < b)
            idx += 4
        elif op == 8:
            a = codes[idx+1] if code[2] == "1" else codes[codes[idx+1]]
            b = codes[idx+2] if code[1] == "1" else codes[codes[idx+2]]
            codes[codes[idx+3]] = int(a == b)
            idx += 4
        else:
            print("Unknown op:", op)
            break

    return output

print("Answer 1:", run(get_codes(), 1))
print("Answer 2:", run(get_codes(), 5))
