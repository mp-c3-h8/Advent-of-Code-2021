import os.path
from timeit import default_timer as timer
from typing import Iterator, Callable

type Pos = tuple[int, int]  # (y,x)
type Image = set[Pos]


def kernel(pos: Pos) -> Iterator[Pos]:
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            yield (pos[0]+dy, pos[1]+dx)


def edges(y_min: int, y_max: int, x_min: int, x_max: int) -> Iterator[tuple[Pos, Pos]]:
    yield from (
        ((y_min, y_min+1), (x_min, x_max)),  # top
        ((y_max-1, y_max), (x_min, x_max)),  # bottom
        ((y_min+2, y_max-2), (x_min, x_min+1)),  # left
        ((y_min+2, y_max-2), (x_max-1, x_max))  # right
    )


def bounding(image: Image) -> tuple[Pos, Pos]:
    y_max, x_max = map(max, *image)
    y_min, x_min = map(min, *image)
    return (y_min, y_max), (x_min, x_max)


def get_new_image(image: Image, algo: list[int], y_min: int, y_max: int, x_min: int, x_max: int, odd: bool, is_inside: Callable[[int, int], int]) -> Image:
    new_image: Image = set()
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            pos = (y, x)
            # calc index
            idx = 0
            if not odd:
                for n, k in enumerate(kernel(pos)):
                    if k in image:
                        idx += 1 << (8-n)
                if algo[idx]:
                    new_image.add(pos)
            else:
                for n, (ky, kx) in enumerate(kernel(pos)):
                    if is_inside(ky, kx):
                        if (ky, kx) in image:
                            idx += 1 << (8-n)
                    else:
                        idx += 1 << (8-n)
                if algo[idx]:
                    new_image.add(pos)
    return new_image


def enhance(image: Image, algo: list[int], steps: int) -> Image:

    (y_min, y_max), (x_min, x_max) = bounding(image)

    for i in range(steps):
        # image grows every step by 1 pixel on each side
        y_min -= 1
        y_max += 1
        x_min -= 1
        x_max += 1
        def is_inside(ky, kx): return y_min+1 <= ky <= y_max-1 and x_min+1 <= kx <= x_max-1
        new_image: Image = set()

        # even iteration, no special cases
        if i % 2 == 0:
            new_image = get_new_image(image, algo, y_min, y_max, x_min, x_max, False, is_inside)

        # every odd iteration, the complete (infinite) outside is lit
        else:

            # safe inner part
            new_image = get_new_image(image, algo, y_min+2, y_max-2, x_min+2, x_max-2, False, is_inside)

            # edge parts
            for (min_y, max_y), (min_x, max_x) in edges(y_min, y_max, x_min, x_max):
                new_image |= get_new_image(image, algo, min_y, max_y, min_x, max_x, True, is_inside)

        image = new_image
    return image


def plot_image(image: Image) -> None:
    import numpy as np
    import matplotlib.pyplot as plt

    (y_min, y_max), (x_min, x_max) = bounding(image)
    dimy, dimx = y_max-y_min+1, x_max-x_min+1

    X = np.ones((dimy, dimx)) * np.nan

    for y, x in image:
        X[y - y_min, x - x_min] = 1
    plt.imshow(X, cmap="tab20b")
    plt.show()


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


algo_str, image_str = data.split("\n\n")
algo: list[int] = list(1 if c == "#" else 0 for c in algo_str)
image: Image = {(y, x) for y, row in enumerate(image_str.splitlines()) for x, c in enumerate(row) if c == "#"}

enhanced = enhance(image, algo, 2)
print("Part 1:", len(enhanced))

enhanced = enhance(enhanced, algo, 48)
print("Part 2:", len(enhanced))

e = timer()
print("time:", e - s)

plot_image(enhanced)
