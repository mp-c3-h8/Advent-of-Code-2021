import os.path
from timeit import default_timer as timer
import z3


start = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

'''
z3 solves without touching the input, but does so slowly

reduce the number of instructions by analyzing the input:
it consists of 14 identical blocks, where 7 can be simplified.
search for "add x _n_" where _n_ > 9
doing so cuts the runtime to ~1min


before                                                after
----------                                            ------------
inp w        first digit                              inp w            first digit    
mul x 0                                               add z w  
add x z                                               add z 8          z = w + 8
mod x 26                                                  
div z 1      does nothing                             inp w            second digit      
add x 14     x > 14                                     
eql x w      never true, since w <= 9                  
eql x 0      x is 1 here                              
mul y 0                                               
add y 25
mul y x      does nothing
add y 1
mul z y      z = 0 and stays 0
mul y 0
add y w
add y 8      y = w + 8
mul y x      does nothing
add z y      z = w + 8

inp w        second digit

'''

s = z3.Optimize()

# 14 input variables
digits = z3.IntVector("d", 14)

# restrict them to 1 <= d_i <= 9
for d in digits:
    s.add(d >= 1)
    s.add(d <= 9)

# initialize registers
reg = {r: 0 for r in "xyzw"}

digit_idx = 0
for i, line in enumerate(data):

    instr, a, *rest = line.split(" ")
    b = rest[0] if rest else 0

    if instr == "inp":
        reg[a] = digits[digit_idx]  # type: ignore
        digit_idx += 1
        continue

    # is b an register or int?
    b = reg[b] if b in reg else int(b)

    # additional variable since we cant assign "in place"
    extra = z3.Int(f't_{i}')

    match instr:
        case "add":
            s.add(extra == reg[a] + b)
        case "mul":
            s.add(extra == reg[a] * b)
        case "mod":
            s.add(reg[a] >= 0)
            s.add(b > 0)
            s.add(extra == reg[a] % b)
        case "div":
            s.add(b != 0)
            s.add(extra == reg[a] / b)
        case "eql":
            s.add(extra == z3.If(reg[a] == b, 1, 0))
        case _:
            raise ValueError(f"Instruction {instr} {a} {b} not valid")

    reg[a] = extra  # type: ignore

# serial number is valid if z == 0
s.add(reg['z'] == 0)

# we want a max/min decimal number
objective = sum((10 ** n) * d for n, d in enumerate(reversed(digits)))

# reuse solver state
s.push()

s.maximize(objective)
assert (repr(s.check()) == "sat"), f"Maximum could not be found"
model = s.model()
p1 = "".join(str(model[d]) for d in digits)
print("Part 1:", p1)

# reset state to last push
s.pop()

s.minimize(objective)
assert (repr(s.check()) == "sat"), f"Minimum could not be found"
model = s.model()
p2 = "".join(str(model[d]) for d in digits)
print("Part 2:", p2)


end = timer()
print("time:", end - start)
