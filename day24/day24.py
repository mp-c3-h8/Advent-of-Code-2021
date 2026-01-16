import os.path
from timeit import default_timer as timer


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

# this just runs the MONAD
idx = 0
w = x = y = z = 0
second = 0
numbers = [1] * 14
for instr in data.splitlines():
    com, first, *rest = instr.split(" ")
    if rest:
        second = rest[0]
    match com:
        case "inp":
            exec(f"{first} = {numbers[idx]}")
            idx += 1
        case "add":
            exec(f"{first} = {first} + {second}")
        case "mul":
            exec(f"{first} = {first} * {second}")
        case "div":
            # TODO: check for first/0
            exec(f"{first} = {first} // {second}")
        case "mod":
            if eval(f"{first} < 0") or eval(f"{second} <= 0"):
                raise ValueError(f"Bad mod: {first} % {second}")
            exec(f"{first} = {first} % {second}")
        case "eql":
            exec(f"{first} = {first} == {second}")

print(f"Result: (x,y,z) = {(x, y, z)}")

e = timer()
print("time:", e - s)
