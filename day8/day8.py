import os.path
from collections import defaultdict

MASK: dict[str, int] = {c: 1 << i for i, c in enumerate("abcdefg")}
NUMBERS: dict[int, str] = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}
NUMBERS_MASK: dict[int, int] = {sum(MASK[c] for c in letters): num for num, letters in NUMBERS.items()}


def decrypt(order: list[str], digits: str) -> int:
    res = ""
    rewire = {new: old for new, old in zip(order, "abcdefg")}
    for digit in digits.split(" "):
        mask = sum(MASK[rewire[d]] for d in digit)
        res += str(NUMBERS_MASK[mask])
    return int(res)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

p1, p2 = 0, 0
count: defaultdict[int, set[str]] = defaultdict(set)
for line in data.splitlines():
    patterns, out = line.split(" | ")
    p1 += sum(len(o) in {2, 3, 4, 7} for o in out.split(" "))

    count.clear()
    for pattern in patterns.split(" "):
        if (l := len(pattern)) in (5, 6) and count[l]:  # save intersections for 5 and 6
            count[l] &= set(pattern)
        else:
            count[l] = set(pattern)

    a = count[3] - count[2]
    g = count[6] - (count[3] | count[4])
    b = count[6] - count[2] - (g | a)
    d = count[5] - (a | g)
    f = count[6] - (a | b | g)
    c = count[2] - f
    e = count[7] - (count[4] | count[3] | g)

    order = [*a, *b, *c, *d, *e, *f, *g]
    p2 += decrypt(order, out)

print("Part 1:", p1)
print("Part 2:", p2)
