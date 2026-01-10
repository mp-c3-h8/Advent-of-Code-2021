import os.path
from collections import Counter


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

counter = Counter(map(int, data.split(",")))
T = 256

for i in range(T):
    newborn = counter[0]
    for j in range(0, 8):
        counter[j] = counter[j+1]
    counter[6] += newborn
    counter[8] = newborn
    if i == 79:
        print("Part 1:", counter.total())

print("Part 2:", counter.total())
