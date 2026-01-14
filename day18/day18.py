import os.path
from timeit import default_timer as timer
from operator import methodcaller, attrgetter
from math import floor, ceil
from itertools import permutations
from functools import reduce


class Node:
    def __init__(self, val: int, parent: Node | None) -> None:
        self.val = val
        self.parent = parent
        self.left: Node | None = None
        self.right: Node | None = None

    def set_left(self, node: Node) -> None:
        self.left = node

    def set_right(self, node: Node) -> None:
        self.right = node

    def add_nodes(self, snail_str: str) -> None:
        left, right = self.split_snail_str(snail_str)
        # mark for (maybe) exploding
        if left.isdigit() and right.isdigit():
            self.val = -2
            self.left = Node(int(left), self)
            self.right = Node(int(right), self)
        else:
            for side, method in zip((left, right), ("set_left", "set_right")):
                val = int(side) if side.isdigit() else -1
                node = Node(val, self)
                methodcaller(method, node)(self)
                if val == -1:
                    node.add_nodes(side)

    def split_snail_str(self, snail_str: str) -> tuple[str, str]:
        count = 0
        for i, c in enumerate(snail_str):
            match c:
                case "[":
                    count += 1
                case "]":
                    count -= 1
                case ",":
                    if count == 1:
                        break
        else:
            raise ValueError("Split impossible")

        return snail_str[1:i], snail_str[i+1:-1]

    @property
    def magnitude(self) -> int:
        if self.val >= 0:
            return self.val
        # always exists by construction
        return 3*self.left.magnitude + 2*self.right.magnitude  # type: ignore


def create_snail(snail_str: str) -> Node:
    root = Node(-1, None)
    root.add_nodes(snail_str)
    return root


def find_explode(node: Node, depth=0) -> Node | None:
    if depth >= 4 and node.val == -2:
        return node
    if node.left and (left := find_explode(node.left, depth+1)):
        return left
    if node.right and (right := find_explode(node.right, depth+1)):
        return right


def find_split(node: Node) -> Node | None:
    if node.val >= 10:
        return node
    if node.left and (left := find_split(node.left)):
        return left
    if node.right and (right := find_split(node.right)):
        return right


def find(node: Node, go_left: bool) -> Node | None:
    if node.val >= 0:
        return node
    elif go_left and node.left:
        return find(node.left, go_left)
    elif not go_left and node.right:
        return find(node.right, go_left)


def explode(node: Node) -> None:
    # add to the left
    search = node
    assert search.parent
    while (search.parent.left == search):
        search = search.parent
        if search.parent == None:
            break
    if search.parent and search.parent.left:
        if (add_left := find(search.parent.left, False)) and node.left:
            add_left.val += node.left.val

    # add to the right
    search = node
    assert search.parent
    while (search.parent.right == search):
        search = search.parent
        if search.parent == None:
            break
    if search.parent and search.parent.right:
        if (add_right := find(search.parent.right, True)) and node.right:
            add_right.val += node.right.val

    # delete node
    node.left = None
    node.right = None
    node.val = 0

    # mark for (maybe) exploding
    if node.parent and node.parent.left and node.parent.right:
        if node.parent.left.val >= 0 and node.parent.right.val >= 0:
            node.parent.val = -2


def split(node: Node) -> None:
    node.left = Node(floor(node.val/2), node)
    node.right = Node(ceil(node.val/2), node)
    node.val = -2


def add_snails(left: Node, right: Node) -> Node:
    root = Node(-1, None)
    left.val = -1
    left.parent = root
    right.val = -1
    right.parent = root
    root.left = left
    root.right = right
    return root


def to_snail(node: Node | None) -> str:
    if node is None:
        return ""
    if node.val >= 0:
        return str(node.val)
    return f"[{to_snail(node.left)},{to_snail(node.right)}]"


def reduce_snail(snail: Node) -> None:
    reducing = True
    while reducing:
        if (node := find_explode(snail)):
            explode(node)
            continue
        elif (node := find_split(snail)):
            split(node)
            continue
        reducing = False


def process(left: Node, right: Node) -> Node:
    added = add_snails(left, right)
    reduce_snail(added)
    return added


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

print("Part 1:", (reduce(process, (create_snail(snail_str) for snail_str in data))).magnitude)

p2 = max((process(create_snail(s1), create_snail(s2))).magnitude for s1, s2 in permutations(data, 2))
print("Part 2:", p2)

e = timer()
print("time:", e - s)
