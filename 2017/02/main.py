with open("./input.txt") as f:
    sheet = [[int(col.strip()) for col in row.strip().split("\t")] for row in f.read().splitlines()]

checksum = 0
checksum2 = 0

for row in sheet:
    checksum += (max(row) - min(row))

    for x in range(len(row)):
        for y in range(len(row)):
            if x == y:
                continue
            if row[x] % row[y] == 0:
                checksum2 += row[x] // row[y]

print("Answer 1:", checksum)
print("Answer 2:", checksum2)
