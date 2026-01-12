import os.path
from timeit import default_timer as timer
from heapq import heapify, heappop, heappush
from typing import Iterator

type Pos = complex
type Grid = dict[Pos, int]


def neighbors(pos: Pos) -> Iterator[Pos]:
    for d in (1, -1, 1j, -1j):
        yield pos+d


def dijkstra(grid: Grid, dimy: int, dimx: int, start: Pos, end: Pos, repeats: int = 0) -> int:

    def is_valid_and_cost(pos: Pos) -> tuple[bool, int]:
        div_y, mod_y = divmod(int(pos.imag), dimy)
        div_x, mod_x = divmod(int(pos.real), dimx)
        local_pos = complex(mod_x, mod_y)
        if (
            div_y < 0 or div_x < 0 or
            div_y > repeats or div_x > repeats or
            local_pos not in grid
        ):
            return (False, 0)

        # valid pos, calc cost
        cost = grid[local_pos] + div_y + div_x  # max 9 + 4 + 4 = 17
        if cost > 9:
            cost -= 9  # works for repeats <= 4
        return (True, cost)

    end = complex(repeats*dimx+end.real, repeats*dimy+end.imag)
    shortest_paths: Grid = {start: 0}
    done: set[Pos] = set()
    q: list[tuple[int, int, Pos]] = [(0, 0, start)]
    heapify(q)
    i = 0
    while q:
        cost, _, pos = heappop(q)

        if pos == end:
            return cost

        if pos in done:
            continue
        done.add(pos)

        for n in neighbors(pos):
            is_valid, cost_n = is_valid_and_cost(n)
            if is_valid and n not in done:
                curr_shortest = shortest_paths.get(n, 10**10)
                if (new_shortest := cost + cost_n) < curr_shortest:
                    shortest_paths[n] = new_shortest
                    i += 1
                    heappush(q, (new_shortest, i, n))

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

part1 = dijkstra(grid, dimy, dimx, start, end)
print("Part 1:", part1)

# repeat 4 = 5 x size
part2 = dijkstra(grid, dimy, dimx, start, end, 4)
print("Part 2:", part2)

e = timer()
print("time:", e - s)
