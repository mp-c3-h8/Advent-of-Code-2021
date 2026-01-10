import os.path
from typing import Iterator
from collections import deque
from math import prod

type Pos = complex


def neighbors(pos: Pos) -> Iterator[Pos]:
    for d in (1, -1, 1j, -1j):
        yield d+pos


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

grid: dict[Pos, int] = {x+y*1j: int(c) for y, row in enumerate(data) for x, c in enumerate(row)}

p1 = 0
basins: list[int] = []
for pos, height in grid.items():
    # skip if no lowpoint
    if any(grid[pos] >= grid[n] for n in neighbors(pos) if n in grid):
        continue

    # floodfill
    basin: set[Pos] = {pos}
    q: deque[Pos] = deque([pos])

    while q:
        pos = q.popleft()

        for n in neighbors(pos):
            if n in grid and n not in basin and grid[n] < 9 and grid[n] > grid[pos]:
                q.append(n)
                basin.add(n)
    p1 += 1+height
    basins.append(len(basin))

print("Part 1:", p1)
print("Part 2:", prod(size for size in sorted(basins, reverse=True)[:3]))
