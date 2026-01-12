import os.path
from collections import Counter
from itertools import pairwise
from timeit import default_timer as timer


type Element = str  # single char like "B"
type Pair = str  # two chars like "CH"
type Rules = dict[Pair, Element]


def insert(rules: Rules, polymer: str, steps: int) -> int:
    # init counter of elements
    counter: Counter[Element] = Counter(polymer)
    # dict of new pairs for next step
    NEW_PAIRS: dict[Pair, tuple[Pair, Pair]] = {pair: (pair[0]+ele, ele+pair[1]) for pair, ele in rules.items()}
    # init todo
    todo: Counter[Pair] = Counter(pair for c1, c2 in pairwise(polymer) if (pair := c1+c2) in rules)
    for _ in range(steps):
        new_todo = Counter()  # todos for next step
        for pair, count in todo.items():
            counter[rules[pair]] += count
            for new_pair in NEW_PAIRS[pair]:
                if new_pair in rules:  # do we have a rule for the new pair?
                    new_todo[new_pair] += count
        todo = new_todo

    elements_count = sorted(counter.values())
    return elements_count[-1] - elements_count[0]


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

polymer, rules_str = data.split("\n\n")
rules: Rules = dict(r.split(" -> ") for r in rules_str.splitlines())

part1 = insert(rules, polymer, 10)
print("Part 1:", part1)

part2 = insert(rules, polymer, 40)
print("Part 2:", part2)


e = timer()
print("time:", e - s)
