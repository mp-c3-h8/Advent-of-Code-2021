import os.path
from timeit import default_timer as timer
from operator import methodcaller
from math import floor, ceil
from itertools import product
from functools import reduce
from copy import deepcopy


class Node:
    def __init__(self, val: int, parent: Node | None) -> None:
        self.val = val
        self.parent: Node | None = parent
        self.left: Node | None = None
        self.right: Node | None = None

    def set_left(self, node: Node) -> None:
        self.left = node

    def set_right(self, node: Node) -> None:
        self.right = node

    def add_snail(self, snail_str: str) -> None:
        for side, method in zip(self.split_snail_str(snail_str), ("set_left", "set_right")):
            val = int(side) if side.isdigit() else -1
            node = Node(val, self)
            methodcaller(method, node)(self)
            if val == -1:
                node.add_snail(side)

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


def create_snail(snail_str: str) -> Node:
    root = Node(-2, None)
    root.add_snail(snail_str)
    return root


def find_explode(node: Node | None, depth=0) -> Node | None:
    if node is not None:
        if node.left and node.right:
            if node.left.val >= 0 and node.right.val >= 0 and depth >= 4:
                return node

        left = find_explode(node.left, depth+1)
        if left:
            return left
        right = find_explode(node.right, depth+1)
        if right:
            return right


def find_split(node: Node | None) -> Node | None:
    if node is not None:
        if node.val >= 10:
            return node

        left = find_split(node.left)
        if left:
            return left
        right = find_split(node.right)
        if right:
            return right


def find_right(node: Node | None) -> Node | None:
    if node is not None:
        if node.val >= 0:
            return node

        right = find_right(node.right)
        if right:
            return right
        left = find_right(node.left)
        if left:
            return left


def find_left(node: Node | None) -> Node | None:
    if node is not None:
        if node.val >= 0:
            return node

        left = find_left(node.left)
        if left:
            return left

        right = find_left(node.right)
        if right:
            return right


def explode(node: Node) -> None:
    # add to the left
    to_search = node
    assert to_search.parent
    while (to_search.parent.left == to_search):
        to_search = to_search.parent
        if to_search.parent == None:
            break
    if to_search.parent:
        add_left = find_right(to_search.parent.left)
        if add_left:
            assert node.left
            add_left.val += node.left.val

    # add to the right
    to_search = node
    assert to_search.parent
    while (to_search.parent.right == to_search):
        to_search = to_search.parent
        if to_search.parent == None:
            break
    if to_search.parent:
        add_right = find_left(to_search.parent.right)
        if add_right:
            assert node.right
            add_right.val += node.right.val

    # delete node
    node.left = None
    node.right = None
    node.val = 0


def split(node: Node) -> None:
    left_val = floor(node.val/2)
    right_val = ceil(node.val/2)
    node.val = -1
    node.left = Node(left_val, node)
    node.right = Node(right_val, node)


def add_snails(left: Node, right: Node) -> Node:
    root = Node(-2, None)
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


def reduce_snail(snail: Node) -> Node:
    reducing = True
    while reducing:
        if (n := find_explode(snail)):
            explode(n)
            continue
        elif (n := find_split(snail)):
            split(n)
            continue
        reducing = False
    return snail


def magnitude(node: Node) -> int:
    if node is not None:
        if node.val >= 0:
            return node.val
        assert node.left and node.right
        return 3*magnitude(node.left) + 2*magnitude(node.right)


def process(left: Node, right: Node) -> Node:
    added = add_snails(left, right)
    reduced = reduce_snail(added)
    return reduced


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

print("Part 1:", magnitude(reduce(process, (create_snail(snail_str) for snail_str in data))))

p2 = max(magnitude(process(create_snail(s1), create_snail(s2))) for s1, s2 in product(data, repeat=2))
print("Part 2:", p2)

e = timer()
print("time:", e - s)
