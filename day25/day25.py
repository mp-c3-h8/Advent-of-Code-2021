import os.path
from timeit import default_timer as timer

type SeaCucumber = tuple[int, int]  # (y,x)
type Herd = set[SeaCucumber]
type Horde = list[Herd]


def move(horde: Horde, dimy: int, dimx: int) -> tuple[int, Horde]:

    max_iter = 10**4

    for i in range(1, max_iter):
        movement: bool = False

        for n, (herd, (dy, dx)) in enumerate(zip(horde, ((0, 1), (1, 0)))):

            new: Herd = set()
            for cuc in herd:
                moved = ((cuc[0]+dy) % dimy, (cuc[1]+dx) % dimx)
                if all(moved not in h for h in horde):
                    new.add(moved)
                    movement = True
                else:
                    new.add(cuc)
            horde[n] = new

        if not movement:
            return (i, horde)

    raise ValueError(f"Max iterations {max_iter} reached.")


def plot_cucumber(horde: Horde, dimy: int, dimx: int) -> None:
    import numpy as np
    import matplotlib.pyplot as plt

    X = np.ones((dimy, dimx)) * np.nan


    for i,herd in enumerate(horde):
        for cuc in herd:
            X[cuc] = i
    plt.imshow(X, cmap="tab20b")
    plt.show()


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

east: Herd = {(y, x) for y, row in enumerate(data) for x, c in enumerate(row) if c == ">"}
south: Herd = {(y, x) for y, row in enumerate(data) for x, c in enumerate(row) if c == "v"}
dimy, dimx = len(data), len(data[0])

steps, horde = move([east, south], dimy, dimx)
print("Part 1:", steps)

e = timer()
print("time:", e - s)

plot_cucumber(horde, dimy, dimx)
