import os.path
from timeit import default_timer as timer
import numpy as np
from itertools import product, combinations
from numpy.linalg import matrix_power
from collections import defaultdict, deque

type Beacon = np.ndarray  # vector: coords of a beacon (bx,by,bz)
type Rotation = np.ndarray  # 3x3 rotation matrix
type Vector = np.ndarray  # general vector (x,y,z)


class Scanner:
    def __init__(self, idx: int, beacons_str: str) -> None:
        self.idx: int = idx
        self._distances: set[int] = set()
        self.set_beacons(beacons_str)
        self.set_pairwise_distances()

    @property
    def beacons(self) -> list[Beacon]:
        return self._beacons

    @property  # { distance: list[ (beacon_i,beacon_j) ] }
    def pairwise_distances(self) -> dict[int, list[tuple[Beacon, Beacon]]]:
        return self._pairwise_distances

    def get_num_overlap(self, overlap: set[int]) -> int:
        return sum(self._num_pairs[dist] for dist in overlap)

    def set_beacons(self, beacons: str) -> None:
        _beacons: list[Beacon] = []
        for beacon in beacons.splitlines()[1:]:
            x, y, z = map(int, beacon.split(","))
            _beacons.append(np.array([x, y, z], dtype=int))
        self._beacons = _beacons

    def set_pairwise_distances(self) -> None:
        distances: dict[int, list[tuple[Beacon, Beacon]]] = defaultdict(list)
        for b1, b2 in combinations(self.beacons, 2):
            dist = ((b2-b1)**2).sum()  # euclidian squared
            distances[dist].append((b1, b2))  # distances are not unique
            self._distances.add(dist)
        self._pairwise_distances = distances
        self._num_pairs = {dist: len(pairs) for dist, pairs in distances.items()}

    def overlap(self, other: Scanner) -> set[int]:
        return self._distances.intersection(other._distances)

    def __repr__(self) -> str:
        return str(self.idx)


def rot_cube() -> np.ndarray:
    ROTX = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=int)
    ROTY = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], dtype=int)
    ROTZ = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)
    IDENTITY = np.eye(3, dtype=int)

    all_rotations = []
    for x, y, z in product(range(4), repeat=3):
        rot = IDENTITY @ matrix_power(ROTX, x) @ matrix_power(ROTY, y) @ matrix_power(ROTZ, z)
        all_rotations.append(rot)

    rotations = np.unique(np.array(all_rotations), axis=0).astype(list)
    return rotations


# from https://gist.github.com/joonahn/607f78e8339283f605b8f89cf5199172
# faster, no duplicates
# see https://groupprops.subwiki.org/wiki/Symmetric_group:S4
def rot_cube2() -> list[Rotation]:
    ROLLMAT = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], dtype=int)
    TURNMAT = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)

    rotations = []
    current_rot = np.eye(3, dtype=int)
    for cycle in range(2):
        for step in range(3):  # RTTT 3 times
            current_rot = ROLLMAT @ current_rot
            rotations.append(current_rot)  # R
            for i in range(3):  # TTT
                current_rot = TURNMAT @ current_rot
                rotations.append(current_rot)
        current_rot = ROLLMAT @ TURNMAT @ ROLLMAT @ current_rot  # RTR
    return rotations


def create_scanners(data: str) -> list[Scanner]:
    scanners_str = data.split("\n\n")
    scanners = [Scanner(i, scanner) for i, scanner in enumerate(scanners_str)]

    return scanners


def find_rot_and_trans(s_i: Scanner, s_j: Scanner, overlap: set[int], rotations) -> tuple[Rotation, Vector]:
    beacons = set(tuple(b) for b in s_i.beacons)
    for dist in overlap:
        for (bi_1, bi_2) in s_i.pairwise_distances[dist]:
            for (bj_1, bj_2) in s_j.pairwise_distances[dist]:
                for b_i, b_j in ((bi_1, bj_1), (bi_1, bj_2)):  # 2 possible pairings
                    for rot_ij in rotations:

                        # b_i = r_ij + rot_ij * b_j
                        r_ij = b_i - rot_ij @ b_j

                        # we have a rotation rot_ij and translation r_ij
                        # lets see if they are correct
                        common_beacons = beacons.intersection(tuple(r_ij + rot_ij @ b) for b in s_j.beacons)
                        if len(common_beacons) >= 12:
                            return (rot_ij, r_ij)

    raise ValueError("No possible rotation found")


def solve(data: str) -> tuple[int, int]:
    scanners = create_scanners(data)
    rotations = rot_cube2()

    # we build a map of coordinate transformations between scanner s_i and scanners s_j:
    # { s_i : list(s_j, rot_ij,r_ij) }
    # such that for all common beacons b in s_i and s_j:
    # b_i = r_ij + rot_ij * b_j
    transforms: defaultdict[Scanner, list[tuple[Scanner, Rotation, Vector]]] = defaultdict(list)
    for s_i, s_j in combinations(scanners, 2):

        # rotations are distance-preserving
        # see https://en.wikipedia.org/wiki/Orthogonal_matrix
        overlap: set[int] = s_i.overlap(s_j)

        # distances might not be unique
        if s_i.get_num_overlap(overlap) < 66 or s_j.get_num_overlap(overlap) < 66:
            # 12 choose 2 = 66 distances must at least match
            continue

        # find rotation and translation
        # b_i = r_ij + rot_ij * b_j for all common beacons b
        rot_ij, r_ij = find_rot_and_trans(s_i, s_j, overlap, rotations)
        transforms[s_i].append((s_j, rot_ij, r_ij))

        # the inverse of a rotation matrix is its transpose
        # left multiply above equation with rot_ji := (rot_ij)^-1 = (rot_ij)^T:
        # rot_ji * b_i = rot_ji * r_ij + b_j      <=>    b_j = -( rot_ji * r_ij) + (rot_ji * b_i)
        # this would yield the same: rot_ji, r_ji = find_rot_and_trans(s_j, s_i, overlap, rotations)
        rot_ji = rot_ij.T
        r_ji = - (rot_ji @ r_ij)
        transforms[s_j].append((s_i, rot_ji, r_ji))

    # now we calculate every beacons position relative to scanner 0
    # we need a kinematic "chain" through the transformations such that we visit every scanner
    scanner0: Scanner = scanners[0]  # we could pick any scanner
    origin0: Vector = np.array([0, 0, 0], dtype=int)
    rot0: Rotation = np.eye(3, dtype=int)

    beacons: set[tuple[int, int, int]] = set(tuple(b) for b in scanner0.beacons)
    origins: list[Vector] = [origin0]
    seen: set[Scanner] = {scanner0}
    init: tuple[Scanner, Rotation, Vector] = (scanner0, rot0, origin0)
    q = deque([init])
    while q:
        if len(seen) == len(scanners):
            break
        s_i, rot_0i, r_0i = q.popleft()  # rot_0i and r_0i are from scanner 0 to scanner i
        for s_j, rot_ij, r_ij in transforms[s_i]:  # local transformation from s_i to s_j
            if s_j in seen:
                continue

            # origin of scanner j relative to scanner 0
            r_0j = r_0i + rot_0i @ r_ij
            origins.append(r_0j)

            # rotation of scanner j relative to scanner 0
            rot_0j = rot_0i @ rot_ij

            # we finally have the beacons of scanner j relative to scanner 0
            beacons.update(tuple(r_0j + rot_0j  @ b) for b in s_j.beacons)
            seen.add(s_j)

            # extend the kinematic "chain"
            q.append((s_j, rot_0j, r_0j))

    # did we locate every scanner?
    if len(seen) != len(scanners):
        raise ValueError("Scanner configuration mismatch.")

    p1 = len(beacons)
    p2 = max(abs(o1-o2).sum() for o1, o2 in combinations(origins, 2))  # manhatten

    return p1, p2


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

p1, p2 = solve(data)

print("Part 1:", p1)
print("Part 2:", p2)

e = timer()
print("time:", e - s)
