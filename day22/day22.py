import os.path
from timeit import default_timer as timer
import re
import numpy as np
from collections import Counter
from math import prod

type Interval = tuple[int, int]  # (x1,x2)
type Cube = tuple[Interval, ...]  # ( (x1,x2) , (y1,y2) , (z1,z2) )


def part1(data: str) -> int:
    regexp = re.compile(r"-?\d+")
    MX = 50
    cube = np.zeros((2*MX+1, 2*MX+1, 2*MX+1), dtype=int)

    for line in data.splitlines():
        x1, x2, y1, y2, z1, z2 = map(int, regexp.findall(line))
        state = 1 if line[:2] == "on" else 0

        if -MX <= x1 and x2 <= MX and -MX <= y1 and y2 <= MX and -MX <= z1 and z2 <= MX:
            cube[x1+MX:x2+MX+1, y1+MX:y2+MX+1, z1+MX:z2+MX+1] = state
    return cube.sum()


def intersection(cube: Cube, other: Cube) -> Cube | None:
    inter: Cube = tuple((max(i1[0], i2[0]), min(i1[1], i2[1])) for i1, i2 in zip(cube, other))
    if all(i_min <= i_max for i_min, i_max in inter):
        return inter
    return None


def vol(cube: Cube) -> int:
    return prod(i_max-i_min+1 for i_min, i_max in cube)

# we are using https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle
def part2(data: str) -> int:
    regexp = re.compile(r"-?\d+")

    cubes: Counter[Cube] = Counter()
    for line in data.splitlines():
        # we add "on" cubes and subtract "off" cubes
        other_state = 1 if line[:2] == "on" else -1
        x1, x2, y1, y2, z1, z2 = map(int, regexp.findall(line))
        other: Cube = ((x1, x2), (y1, y2), (z1, z2))

        # calc intersection with every cube so far
        new_cubes: Counter[Cube] = Counter()
        for cube, state in cubes.items():
            if (inter := intersection(cube, other)):
                new_cubes[inter] -= state

        # only add other cube, if he turns "on"
        if other_state == 1:
            new_cubes[other] += other_state

        # update cubes
        cubes.update(new_cubes)

        # delete "0" cubes
        cubes = Counter({cube: state for cube, state in cubes.items() if state != 0})

    return sum(state*vol(cube) for cube, state in cubes.items())


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

print("Part 1:", part1(data))
print("Part 2:", part2(data))

e = timer()
print("time:", e - s)
