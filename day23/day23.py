import os.path
from timeit import default_timer as timer
from heapq import heapify, heappop, heappush
from collections import defaultdict
from itertools import batched
import re


type Hallway = str
type Rooms = str


def solve(input: list[str]) -> int:
    COSTS: dict[str, int] = {"A": 1, "B": 10, "C": 100, "D": 1000}
    ROOMS = "ABCD"
    ROOMS_IDX = {c: i for i, c in enumerate(ROOMS)}
    ROOM_LENGTH = len(input) // 4

    hallway = "." * 11
    rooms = "".join(room for room in input)
    paths: defaultdict[tuple[Hallway, Rooms], int] = defaultdict(lambda: 10**6, {(hallway, rooms): 0})

    def heuristic(hallway: str, rooms: str) -> int:
        nonlocal COSTS, ROOMS, ROOM_LENGTH, ROOMS_IDX

        res = 0
        for i, (DESTINATION, subrooms) in enumerate(zip(ROOMS, batched(rooms, ROOM_LENGTH))):
            for sroom in subrooms:
                if sroom != DESTINATION and sroom != ".":
                    res += (abs(i-ROOMS_IDX[sroom])*2 + 2) * COSTS[sroom]

        for i, h in enumerate(hallway):
            if h != ".":
                room_idx = ROOMS_IDX[h] * 2
                res += (abs(i-(room_idx+2)) + 1) * COSTS[h]

        return res

    q = [(0, 0, 0, hallway, rooms)]
    heapify(q)

    n = 0
    while q:
        prio, cost, _, hallway, rooms = heappop(q)

        # do we know a shorter path?
        if paths[(hallway, rooms)] < cost:
            continue

        # move (hallway -> room) first
        # if we have a valid move, no move (room -> hallway) can occur
        for i, h in enumerate(hallway):
            if h != ".":
                room_idx = ROOMS_IDX[h] * 2  # A=0, B=2, C=4, D=6
                local_idx = ROOMS_IDX[h] * ROOM_LENGTH

                # where to move?
                offset = -1
                for k in range(local_idx, local_idx+ROOM_LENGTH):
                    if rooms[k] == ".":
                        offset += 1
                    elif rooms[k] != h:
                        break

                # free spot found
                else:

                    # WAY MUST BE FREE!
                    start = min(i, room_idx+2)
                    end = max(i, room_idx+2)
                    if any(hallway[k] != "." for k in range(start+1, end)):
                        continue

                    new_hallway = hallway[:i] + "." + hallway[i+1:]  # spot now empty
                    new_rooms = rooms[:local_idx+offset] + h + rooms[local_idx+offset+1:]  # spot now taken by h
                    new_cost = cost + (abs(i-(room_idx+2)) + 1 + offset) * COSTS[h]
                    if paths[(new_hallway, new_rooms)] > new_cost:
                        paths[(new_hallway, new_rooms)] = new_cost
                        n += 1
                        add = 0
                        # add = heuristic(new_hallway, new_rooms)
                        heappush(q, (new_cost+add, new_cost, n, new_hallway, new_rooms))
                        break  # THIS skips the else clause below

        # no valid (hallway -> room move), consider (room -> hallway) moves
        else:
            done = True
            for i, (DESTINATION, subrooms) in enumerate(zip(ROOMS, batched(rooms, ROOM_LENGTH))):

                for sroom in subrooms:
                    if sroom == DESTINATION:
                        continue
                    elif sroom == ".":
                        done = False
                    else:
                        done = False
                        break

                # room finished -> skip
                else:
                    continue

                room_idx = i * 2  # A=0, B=2, C=4, D=6
                local_idx = i * ROOM_LENGTH

                # who can move?
                mover = "Z"
                offset = 0
                for k in range(local_idx, local_idx+ROOM_LENGTH):
                    if rooms[k] == ".":
                        offset += 1
                    else:
                        mover = rooms[k]
                        break

                new_rooms = rooms[:local_idx+offset] + "." + rooms[local_idx+offset+1:]  # spot now empty

                # go left / right
                for incr in (-1, 1):
                    curr = room_idx + 2  # directly above the room
                    while (0 < curr < 10):
                        curr += incr
                        if curr in (2, 4, 6, 8):  # dont stop directly above any room
                            continue
                        if hallway[curr] != ".":  # path blocked, cant go further
                            break
                        new_hallway = hallway[:curr] + mover + hallway[curr+1:]  # spot now taken by mover
                        new_cost = cost + (abs(curr-(room_idx+2)) + 1 + offset) * COSTS[mover]
                        if paths[(new_hallway, new_rooms)] > new_cost:
                            paths[(new_hallway, new_rooms)] = new_cost
                            n += 1
                            add = 0
                            # add = heuristic(new_hallway, new_rooms)
                            heappush(q, (new_cost+add, new_cost, n, new_hallway, new_rooms))

            if done:  # solution found
                return paths[(hallway, rooms)]

    return 10**10


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

amphi = re.findall(r"[A-Z]", data)
p1 = [amphi[i+4*j] for i in range(4) for j in range(2)]
print("Part 1:", solve(p1))

p2 = p1[:1] + ["D", "D"] + p1[1:3] + ["C", "B"] + p1[3:5] + ["B", "A"] + p1[5:7] + ["A", "C"] + p1[7:]
print("Part 2:", solve(p2))


e = timer()
print("time:", e - s)
