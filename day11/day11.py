import os.path
from typing import Iterator
from collections import deque

type Pos = complex


def neighbors(pos: Pos) -> Iterator[Pos]:
    for d in (1, -1, 1j, -1j, -1-1j, -1+1j, 1-1j, 1+1j):
        yield d+pos


def flashes_after_step(octopuses: dict[Pos, int]) -> int:
    q: deque[Pos] = deque()

    # octo: Pos :)
    def does_flash_after_increase(octo: Pos, energy: int) -> bool:
        energy += 1
        if energy > 9:
            energy = 0
            q.append(octo)  # collect for chain reaction
        octopuses[octo] = energy
        return energy == 0

    # increase every energy level by 1
    flashes = sum(does_flash_after_increase(octo, energy) for octo, energy in octopuses.items())

    # chain reaction flashes
    while q:
        octo = q.popleft()
        flashes += sum(does_flash_after_increase(n, energy) for n in neighbors(octo)
                       if n in octopuses and (energy := octopuses[n]) > 0)

    return flashes


def simulate(octopuses: dict[Pos, int], steps: int) -> int:
    return sum(flashes_after_step(octopuses) for _ in range(steps))


def all_flash(octopuses: dict[Pos, int]) -> int:
    goal = len(octopuses)
    for i in range(1, 10**3):
        if flashes_after_step(octopuses) == goal:
            return i
    raise ValueError("Reached max iterations")


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

octopuses: dict[Pos, int] = {x+y*1j: int(e) for y, row in enumerate(data) for x, e in enumerate(row)}

steps_p1 = 100
print("Part 1:", simulate(octopuses, steps_p1))
print("Part 2:", steps_p1 + all_flash(octopuses))
