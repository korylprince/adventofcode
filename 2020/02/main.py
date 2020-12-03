def parseRule(line):
    rule, passwd = [x.strip() for x in line.split(":")]
    span, letter = [x.strip() for x in rule.split(" ")]
    min, max = [x.strip() for x in span.split("-")]
    return {
        "passwd": passwd,
        "letter": letter,
        "min": int(min),
        "max": int(max),
    }

def validate(rule):
    return rule["min"] <= rule["passwd"].count(rule["letter"]) <= rule["max"]

def validate2(rule):
    checks = (rule["passwd"][rule["min"]-1] == rule["letter"], rule["passwd"][rule["max"]-1] == rule["letter"])
    return True in checks and False in checks

with open("./input.txt") as f:
    rules = [parseRule(line.strip()) for line in f.read().strip().splitlines()]

print("Answer 1:", len([r for r in rules if validate(r)]))
print("Answer 2:", len([r for r in rules if validate2(r)]))
