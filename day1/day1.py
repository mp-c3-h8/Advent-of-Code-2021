import os.path
from itertools import pairwise
from more_itertools import windowed

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()


print("Part 1:", sum(int(d1) < int(d2) for d1, d2 in pairwise(data)))

w_old, p2 = 10**10, 0
for window in windowed(data, 3, fillvalue="0"):
    if (w := sum(map(int, window))) > w_old:
        p2 += 1
    w_old = w

print("Part 2:", p2)
