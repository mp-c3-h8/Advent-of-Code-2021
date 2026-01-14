import os.path
import numpy as np
from scipy.ndimage import convolve
from timeit import default_timer as timer
from numpy.typing import NDArray


def enhance(image: NDArray, algo: NDArray, steps: int) -> NDArray:
    # pad the image beforehand to take
    # completely lit background (every odd step) into account
    # we calculate too much before reaching steps though
    padded = np.pad(image, (steps+1, steps+1))
    kernel = np.array([2**i for i in range(9)]).reshape(3, 3)

    for _ in range(steps):
        # convolve
        convolve(padded, kernel, output=padded)
        # replace with values in algo
        padded = algo[padded]
    return padded


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()


algo_str, image_str = data.split("\n\n")
image_split = image_str.splitlines()

# mask for pixel (1 = lit)
algo = np.array([1 if c == "#" else 0 for c in algo_str])
image = np.array([[1 if c == "#" else 0 for c in row] for row in image_split])

enhanced = enhance(image, algo, 2)
print("Part 1:", enhanced.sum())

enhanced = enhance(enhanced, algo, 48)
print("Part 2:", enhanced.sum())


e = timer()
print("time:", e - s)
