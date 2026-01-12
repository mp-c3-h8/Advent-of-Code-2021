import os.path
from timeit import default_timer as timer
from heapq import heapify, heappop, heappush
from typing import Iterator
from itertools import product

type Pos = complex
type Grid = dict[Pos, int]


def neighbors(pos: Pos) -> Iterator[Pos]:
    for d in (1, -1, 1j, -1j):
        yield pos+d


def dijkstra(grid: Grid, start: Pos, end: Pos) -> int:

    shortest_paths: Grid = {start: 0}
    done: set[Pos] = set()
    q: list[tuple[float, int, Pos]] = [(0, 0, start)]
    heapify(q)
    i = 0
    while q:
        prio, _, pos = heappop(q)

        if pos == end:
            return shortest_paths[pos]

        if pos in done:
            continue
        done.add(pos)

        for n in neighbors(pos):
            if n in grid and n not in done:
                curr_shortest = shortest_paths.get(n, 10**10)
                if (new_shortest := shortest_paths[pos] + grid[n]) < curr_shortest:
                    shortest_paths[n] = new_shortest
                    i += 1
                    new_prio = new_shortest
                    heappush(q, (new_prio, i, n))

    raise ValueError(f"End position {end} not found")


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

start = 0
dimy, dimx = len(data), len(data[0])
end = complex(dimx-1, dimy-1)
grid = {x+y*1j: int(r) for y, row in enumerate(data) for x, r in enumerate(row)}

part1 = dijkstra(grid, start, end)
print("Part 1:", part1)

factor = 5
expanded_grid = {pos + dx*dimx + dy*dimy * 1j: c if (c := grid[pos]+dy+dx) <= 9 else c-9
                 for pos in grid for (dy, dx) in product(range(factor), repeat=2)}
new_end = complex((factor-1)*dimx+end.real, (factor-1)*dimy+end.imag)
part2 = dijkstra(expanded_grid, start, new_end)
print("Part 2:", part2)


e = timer()
print("time:", e - s)
