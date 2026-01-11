import os.path
from collections import deque, defaultdict
from timeit import default_timer as timer
from functools import cache

type Node = str
type Graph = defaultdict[Node, set[Node]]
type Path = set[Node]
type Item = tuple[Node, Path, bool]  # (current node , small caves seen , can revisit)


def create_graph(data: str) -> Graph:
    graph: Graph = defaultdict(set)
    for edge in data.splitlines():
        n1, n2 = edge.split("-")
        graph[n1].add(n2)
        graph[n2].add(n1)
    return graph


def paths(graph: Graph, start: Node, end: Node, allow_revisit: bool = False) -> int:
    count = 0
    # (current node , small caves seen , can revisit)
    # no need to track big caves
    q: deque[Item] = deque([(start, {start}, allow_revisit)])

    while q:
        curr, small_caves, allow_revisit = q.pop()

        for adj in graph[curr]:
            if adj == end:
                count += 1
                continue

            if adj not in small_caves:
                small_cave = set() if adj.isupper() else {adj}
                q.append((adj, small_caves | small_cave, allow_revisit))
            elif allow_revisit and adj != start:
                q.append((adj, small_caves | {adj}, False))

    return count


def paths_memo(graph: Graph, start: Node, end: Node, allow_revisit: bool = False) -> int:

    @cache
    def dfs(curr: Node, small_caves: frozenset[Node], allow_revisit: bool = False) -> int:
        count = 0
        for adj in graph[curr]:
            if adj == end:
                count += 1
            elif adj not in small_caves:
                small_cave = set() if adj.isupper() else {adj}
                count += dfs(adj, small_caves | small_cave, allow_revisit)
            elif allow_revisit and adj != start:
                count += dfs(adj, small_caves | {adj}, False)

        return count

    return dfs(start, frozenset({start}), allow_revisit)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

graph = create_graph(data)

s = timer()

print("Part 1:", paths(graph, "start", "end"))
print("Part 2:", paths(graph, "start", "end", True))


e = timer()
print("time:", e - s)

print("Part 1 (memo):", paths_memo(graph, "start", "end"))
print("Part 2 (memo):", paths_memo(graph, "start", "end", True))

k = timer()
print("time:", k - e)
