import re

required = set(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"))

with open("./input.txt") as f:
    passports = [p.replace("\n", " ").split(" ") for p in f.read().strip().split("\n\n")]
    passports = [[item.split(":") for item in p] for p in passports]
    passports = [{k: v for k, v in p} for p in passports]

def validate1(p):
    if len(required.difference(set(p.keys()))) != 0:
        return False
    return True

def validate2(p):
    if len(required.difference(set(p.keys()))) != 0:
        return False
    if re.match(r"^\d{4}$", p["byr"]) is None or not (1920 <= int(p["byr"]) <= 2002):
        return False
    if re.match(r"^\d{4}$", p["iyr"]) is None or not (2010 <= int(p["iyr"]) <= 2020):
        return False
    if re.match(r"^\d{4}$", p["eyr"]) is None or not (2020 <= int(p["eyr"]) <= 2030):
        return False
    if (mat := re.match(r"^(\d+)(cm|in)$", p["hgt"])) is None:
        return False
    if mat.groups()[1] == "cm" and not(150 <= int(mat.groups()[0]) <= 193):
        return False
    if mat.groups()[1] == "in" and not(59 <= int(mat.groups()[0]) <= 76):
        return False
    if re.match(r"^#[0-9a-f]{6}$", p["hcl"]) is None:
        return False
    if p["ecl"] not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
        return False
    if re.match(r"^[0-9]{9}$", p["pid"]) is None:
        return False

    return True


print("Answer 1:", len([p for p in passports if validate1(p)]))
print("Answer 2:", len([p for p in passports if validate2(p)]))
