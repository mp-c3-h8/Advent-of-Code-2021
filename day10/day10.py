import os.path
from collections import Counter

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

BRACKETS: dict[str, str] = {"(": ")", "[": "]", "{": "}", "<": ">"}
ERROR_SCORE: dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}
SCORE: dict[str, int] = {c: i for i, c in enumerate("([{<", 1)}

illegal: Counter[str] = Counter()
scores: list[int] = []
for line in data:
    brackets = []
    for c in line:
        if c in BRACKETS:  # opening
            brackets.append(c)
        elif c == BRACKETS[brackets.pop()]:  # closing and match
            pass  # cool!
        else:  # closing and no match
            illegal.update(c)
            break
    else:  # loop didnt break -> incomplete
        score = 0
        while brackets:
            score *= 5
            score += SCORE[brackets.pop()]
        scores.append(score)

print("Part 1:", sum(count * ERROR_SCORE[bracket] for bracket, count in illegal.items()))
print("Part 2:", sorted(scores)[len(scores)//2])
