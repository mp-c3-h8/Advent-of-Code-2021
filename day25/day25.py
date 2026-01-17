import os.path
from timeit import default_timer as timer

type SeaCucumber = tuple[int, int]  # (y,x)
type Herd = set[SeaCucumber]


def cucumber_jam(east: Herd, south: Herd, dimy: int, dimx: int) -> tuple[int, Herd, Herd]:
    max_iter = 10**4

    for i in range(1, max_iter):
        movement, east, south = move(east, south, dimy, dimx)
        if not movement:
            return (i, east, south)

    raise ValueError(f"Max iterations {max_iter} reached.")


def move(east: Herd, south: Herd, dimy: int, dimx: int) -> tuple[int, Herd, Herd]:

    east_: Herd = set()
    south_: Herd = set()
    movement: bool = False

    for cuc in east:
        moved = (cuc[0], (cuc[1]+1) % dimx)
        if moved not in east and moved not in south:
            east_.add(moved)
            movement = True
        else:
            east_.add(cuc)
    east = east_

    for cuc in south:
        moved = ((cuc[0]+1) % dimy, cuc[1])
        if moved not in east and moved not in south:
            south_.add(moved)
            movement = True
        else:
            south_.add(cuc)
    south = south_

    return (movement, east, south)


def create_matrix(east: Herd, south: Herd, dimy: int, dimx: int):
    import numpy as np
    X = np.ones((dimy, dimx)) * np.nan

    for cuc in east:
        X[cuc] = 1
    for cuc in south:
        X[cuc] = 5

    return X


def plot_cucumber(east: Herd, south: Herd, dimy: int, dimx: int) -> None:
    import matplotlib.pyplot as plt

    X = create_matrix(east, south, dimy, dimx)
    plt.imshow(X, cmap="tab20b")
    plt.show()


def animate_cucumber(east: Herd, south: Herd, dimy: int, dimx: int) -> None:
    import matplotlib.pyplot as plt
    from celluloid import Camera

    gcf = plt.gcf()
    gca = plt.gca()
    gca.set_axis_off()
    camera = Camera(gcf)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    out_path = os.path.join(dir_path, "animated_cucumbers.mp4")

    max_iter = 10**4

    for i in range(1, max_iter):
        movement, east, south = move(east, south, dimy, dimx)

        X = create_matrix(east, south, dimy, dimx)
        plt.imshow(X, cmap="tab20b")
        camera.snap()

        if not movement:
            animation = camera.animate()
            # animation.save("animated_cucumbers.gif",fps=10)
            out_path = os.path.join(dir_path, "animated_cucumbers.mp4")
            animation.save(out_path, fps=30)
            return

    raise ValueError(f"Max iterations {max_iter} reached.")


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

east: Herd = {(y, x) for y, row in enumerate(data) for x, c in enumerate(row) if c == ">"}
south: Herd = {(y, x) for y, row in enumerate(data) for x, c in enumerate(row) if c == "v"}
dimy, dimx = len(data), len(data[0])

# animate_cucumber(east, south, dimy, dimx)

steps, east, south = cucumber_jam(east, south, dimy, dimx)
print("Part 1:", steps)


e = timer()
print("time:", e - s)

plot_cucumber(east, south, dimy, dimx)
