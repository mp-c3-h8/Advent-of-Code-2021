import os.path
from timeit import default_timer as timer
from math import sqrt, ceil
import re

type Pos = tuple[int, int]


# computes the timestep at wich we hit y_star with inital w0 (y-axis)
def test(w0: float, y_star: float) -> float:
    assert w0 > 0
    assert y_star < 0
    a = (2*w0+1)
    b = sqrt(a**2-8*y_star)/2
    return a/2 + b


def f1(w0: float, y_min: float, y_max: float) -> float:
    # maximum reached when ceil( test(w0, y_max) ) > floor( test(w0, y_min) )
    return abs(test(w0, y_max) - test(w0, y_min)) - 0.4


def newton(y_min: float, y_max: float, start: float) -> float:
    eps = 1e-4
    for _ in range(10**3):
        f_start = f1(start, y_min, y_max)
        f_prime = (f1(start+eps, y_min, y_max)-f_start)/eps
        new = start - f_start/f_prime
        if abs(start-new) < 1e-3:
            return new
        start = new
    raise ValueError("Reached max iterations")


def is_hit_in_y(w: int, y_min: int, y_max) -> bool:
    target = range(y_min, y_max+1)
    y = 0
    for _ in range(10**3):
        y += w
        w -= 1
        if y in target:
            return True
        if y < y_min:
            return False
    raise ValueError("Reached max iterations")


def is_hit(u: int, w: int, x_min: int, x_max: int, y_min: int, y_max) -> bool:
    target_y = range(y_min, y_max+1)
    target_x = range(x_min, x_max+1)
    x, y = 0, 0
    for _ in range(10**3):
        x += u
        y += w
        w -= 1
        if u > 0:
            u -= 1
        if y in target_y and x in target_x:
            return True
        if y < y_min or x > x_max:
            return False
    raise ValueError("Reached max iterations")


def max_y(w: int) -> int:
    return int(w*w - (w-1)*w/2)


def part2(x_min: int, x_max: int, y_min: int, y_max, w_star: int) -> int:
    # brute force
    return sum(is_hit(u, w, x_min, x_max, y_min, y_max)
               for w in range(y_min, w_star+1)
               for u in range(1, x_max+1))


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

x_min, x_max, y_min, y_max = map(int, re.findall(r"-?\d+", data))
w_start = ceil(newton(y_min, y_max, 10))

assert w_start > 0
assert is_hit_in_y(w_start, y_min, y_max) == False

w_star = 0
for i in range(w_start+5, 0, -1):
    if is_hit_in_y(i, y_min, y_max):
        w_star = i
        break

print(f"Part 1: Shooting with w={w_star} and reaching a height of {max_y(w_star)}")

print("Part 2:", part2(x_min, x_max, y_min, y_max, w_star))

e = timer()
print("time:", e - s)
