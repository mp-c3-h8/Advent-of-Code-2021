import os.path
from collections import Counter


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

counter = Counter()
counter2 = Counter()
for line in data.splitlines():
    a, b = line.split(" -> ")
    x1, y1, x2, y2 = map(int, line.replace(" -> ", ",").split(","))
    if x1 == x2 or y1 == y2:
        counter.update(
            (y, x)
            for y in range(min(y1, y2), max(y1, y2)+1)
            for x in range(min(x1, x2), max(x1, x2)+1)
        )
    else:  # diag
        dx = x2-x1
        dy = y2-y1
        ex = round(dx / abs(dx))
        ey = round(dy / abs(dy))
        counter2.update((y1+i*ey, x1+i*ex) for i in range(abs(dx)+1))

counter2.update(counter)
print("Part 1:", sum(count >= 2 for count in counter.values()))
print("Part 2:", sum(count >= 2 for count in counter2.values()))
