import os.path
from math import copysign
from typing import Callable

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

# list of y_i
y: list[int] = sorted([*map(int, data.split(","))])


def f1(b: float) -> float:
    return sum(abs(b-i) for i in y)


def f1_prime(b: float) -> float:
    return sum(copysign(1, b-i) for i in y)


def f2(b: float) -> float:
    return sum(abs(b-i)*(abs(b-i)+1) for i in y) / 2


def f2_prime(b: float) -> float:
    return sum(2*(b-i) + copysign(1, b-i) for i in y) / 2


def bisection(f: Callable[[float], float], left: float, right: float) -> float:
    middle = (left+right)/2
    if abs(left-right) < 1e-2:
        return middle
    f_m = f(middle)
    if f(left) * f_m < 0:
        return bisection(f, left, middle)
    else:
        return bisection(f, middle, right)


def gradient_descent(f: Callable[[float], float], f_prime: Callable[[float], float], start: float) -> float:
    for _ in range(10**3):
        grad = -f_prime(start)
        f_start = f(start)

        a = 1  # backtracking
        r = 0.5
        s = 0.001
        for _ in range(10**3):
            if f(start+a*grad) <= f_start + s*a * -grad*grad:
                break
            a *= r
        else:
            raise ValueError("Reached max iterations for alpha")

        new = start + a*grad
        if abs(f_start-f(new)) < 1:
            return new
        start = new
    raise ValueError("Reached max iterations")


def newton(f: Callable[[float], float], start: float) -> float:
    eps = 1e-3
    for _ in range(10**3):
        f_start = f(start)
        f_prime = (f(start+eps)-f_start)/eps
        new = start - f_start/f_prime
        if abs(start-new) < eps:
            return new
        start = new
    raise ValueError("Reached max iterations")


m = len(y)//2
if len(y) % 2 == 1:
    y_median = y[m]
else:
    y_median = (y[m-1] + y[m]) // 2

y_min = y[0]
y_max = y[-1]
start = (y_min + y_max)/2

b1_bisec = round(bisection(f1_prime, y_min, y_max))
f1_bisec = round(f1(b1_bisec))
b1_descent = round(gradient_descent(f1, f1_prime, start))
f1_descent = round(f1(b1_descent))

print(f"Part 1: y_median = {y_median}, f1(y_median) = {f1(y_median)}")
print(f"Part 1 (bisection): b = {b1_bisec}, f1(b) = {f1_bisec}")
print(f"Part 1 (newton): doesnt work, f1' isnt differentiable")
print(f"Part 1 (gradient descent): b = {b1_descent}, f1(b) = {f1_descent}")

y_mean = round(sum(y)/len(y))
candidates = [round(f2(m)) for m in range(y_mean-10, y_mean+3)]
b2_bisec = round(bisection(f2_prime, y_min, y_max))
f2_bisec = round(f2(b2_bisec))
b2_newton = round(newton(f2_prime, start))
f2_newton = round(f2(b2_newton))
b2_descent = round(gradient_descent(f2, f2_prime, start))
f2_descent = round(f2(b2_descent))

print(f"\nPart 2: y_mean = {y_mean}, f2_min = {min(candidates)}")
print(f"Part 2 (bisection): b = {b2_bisec}, f2(b) = {f2_bisec}")
print(f"Part 2 (newton): b = {b2_newton}, f2(b) = {f2_newton}")
print(f"Part 2 (gradient descent slow): b = {b2_descent}, f1(b) = {f2_descent}")
