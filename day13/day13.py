import os.path

type Pos = tuple[int, int]  # (y,x)
type Paper = set[Pos]


def create_paper(dots_str: str) -> Paper:
    paper: set[Pos] = set()
    for dot in dots_str.splitlines():
        x, y = map(int, dot.split(","))
        paper.add((y, x))
    return paper


def fold(paper: Paper, fold_str: str) -> int:
    num_dots = 0
    for i, inst in enumerate(fold_str.splitlines(), 1):
        axis, num_str = inst.split("=")
        num = int(num_str)
        for y, x in paper.copy():
            if axis[-1] == "y" and y > num:
                paper.add((-y+2*num, x))
                paper.remove((y, x))
            elif axis[-1] == "x" and x > num:
                paper.add((y, -x+2*num))
                paper.remove((y, x))
        if i == 1:
            num_dots = len(paper)
    return num_dots


def print_paper(paper: Paper) -> None:
    yy = sorted(y for y, x in paper)
    xx = sorted(x for y, x in paper)
    dimy, dimx = yy[-1]-yy[0]+1, xx[-1]-xx[0]+1
    matrix = [[" " for _ in range(dimx)] for _ in range(dimy)]
    for y, x in paper:
        matrix[y-yy[0]][x-xx[0]] = "█"
    for row in matrix:
        print("".join(row))


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

dots_str, fold_str = data.split("\n\n")
paper = create_paper(dots_str)
num_dots = fold(paper, fold_str)
print(f"Part 1: {num_dots}")

print("Part 2:\n")
print_paper(paper)
