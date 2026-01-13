import os.path
from timeit import default_timer as timer
from operator import methodcaller
from math import floor, ceil
from itertools import permutations
from functools import reduce


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

    def add_nodes(self, snail_str: str) -> None:
        for side, method in zip(self.split_snail_str(snail_str), ("set_left", "set_right")):
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

    def magnitude(self) -> int:
        if self.val >= 0:
            return self.val
        assert self.left and self.right
        return 3*self.left.magnitude() + 2*self.right.magnitude()


def create_snail(snail_str: str) -> Node:
    root = Node(-2, None)
    root.add_nodes(snail_str)
    return root


def find_explode(node: Node | None, depth=0) -> Node | None:
    if node is not None:
        if node.left and node.right:
            if node.left.val >= 0 and node.right.val >= 0 and depth >= 4:
                return node

        return find_explode(node.left, depth+1) or find_explode(node.right, depth+1)


def find_split(node: Node | None) -> Node | None:
    if node is not None:
        if node.val >= 10:
            return node

        return find_split(node.left) or find_split(node.right)


def find_right(node: Node | None) -> Node | None:
    if node is not None:
        if node.val >= 0:
            return node
        return find_right(node.right)


def find_left(node: Node | None) -> Node | None:
    if node is not None:
        if node.val >= 0:
            return node
        return find_left(node.left)


def explode(node: Node) -> None:
    # add to the left
    find = node
    assert find.parent
    while (find.parent.left == find):
        find = find.parent
        if find.parent == None:
            break
    if find.parent and (add_left := find_right(find.parent.left)) and node.left:
        add_left.val += node.left.val

    # add to the right
    find = node
    assert find.parent
    while (find.parent.right == find):
        find = find.parent
        if find.parent == None:
            break
    if find.parent and (add_right := find_left(find.parent.right)) and node.right:
        add_right.val += node.right.val

    # delete node
    node.left = None
    node.right = None
    node.val = 0


def split(node: Node) -> None:
    node.left = Node(floor(node.val/2), node)
    node.right = Node(ceil(node.val/2), node)
    node.val = -1


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

print("Part 1:", (reduce(process, (create_snail(snail_str) for snail_str in data))).magnitude())

p2 = max((process(create_snail(s1), create_snail(s2))).magnitude() for s1, s2 in permutations(data, 2))
print("Part 2:", p2)

e = timer()
print("time:", e - s)
